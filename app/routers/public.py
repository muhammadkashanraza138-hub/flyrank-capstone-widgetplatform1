
from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from app.db import get_db
from app.models.models import Widget, Submission
from app.schemas.schemas import SubmissionIn
from app.services.rate_limit import limiter
from app.services.geo import enrich
from app.services.side_effects import send_confirmation
import uuid

router = APIRouter(tags=["public"])


@router.get("/widgets/{widget_id}/config")
def config(widget_id, request: Request, db: Session = Depends(get_db)):
    w = db.get(Widget, widget_id)
    if not w:
        raise HTTPException(404, "Widget not found")
    return JSONResponse(
        {
            "id": w.id,
            "type": w.type,
            "title": w.title,
            "description": w.description,
            "fields": w.fields,
            "button_text": w.button_text,
            "display_options": w.display_options,
            "version": w.version,
        },
        headers={"Cache-Control": "public, max-age=60",
                 "Access-Control-Allow-Origin": "*"},
    )


@router.options("/submissions")
def preflight():
    return JSONResponse(
        {},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers":
                "Content-Type, Authorization, Idempotency-Key",
        },
    )


@router.post("/submissions")
async def submit(
    widget_id: str,
    body: SubmissionIn,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if len(await request.body()) > 65536:
        raise HTTPException(413, "Payload too large")

    ip = request.client.host if request.client else "unknown"

    if not limiter.allow(f"ip:{ip}") or not limiter.allow(f"widget:{widget_id}"):
        raise HTTPException(429, "Rate limit exceeded")

    if body.honeypot:
        return JSONResponse(
            {"status": "dropped"},
            status_code=202,
            headers={"Access-Control-Allow-Origin": "*"},
        )

    w = db.get(Widget, widget_id)
    if not w:
        raise HTTPException(404, "Widget not found")

    if not isinstance(body.data, dict):
        raise HTTPException(422, "Submission data must be an object")

    fields = w.fields or []
    allowed = {f.get("name") or f.get("key"): f for f in fields}
    allowed.pop(None, None)

    unknown = set(body.data) - set(allowed)
    if unknown:
        raise HTTPException(
            422,
            detail={
                "message": "Unexpected submission fields",
                "fields": sorted(unknown),
            },
        )

    for name, field in allowed.items():
        value = body.data.get(name)

        if field.get("required") and (
            value is None or (isinstance(value, str) and not value.strip())
        ):
            raise HTTPException(422, f"Field '{name}' is required")

        if value is None:
            continue

        field_type = str(field.get("type", "string")).lower()

        if field_type == "email":
            if not isinstance(value, str):
                raise HTTPException(422, f"Field '{name}' must be an email")
            try:
                validate_email(value, check_deliverability=False)
            except EmailNotValidError:
                raise HTTPException(422, f"Field '{name}' must be a valid email")

        elif field_type in ("string", "text"):
            if not isinstance(value, str):
                raise HTTPException(422, f"Field '{name}' must be a string")

        elif field_type in ("number", "integer"):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise HTTPException(422, f"Field '{name}' must be a number")

        elif field_type == "boolean":
            if not isinstance(value, bool):
                raise HTTPException(422, f"Field '{name}' must be a boolean")

    key = request.headers.get("Idempotency-Key")
    if key:
        existing = db.query(Submission).filter_by(
            widget_id=widget_id, idempotency_key=key
        ).first()
        if existing:
            return {
                "id": existing.id,
                "status": "duplicate",
                "geo": existing.geo,
            }

    geo = await enrich(ip)

    s = Submission(
        id=str(uuid.uuid4()),
        widget_id=w.id,
        tenant_id=w.tenant_id,
        data=body.data,
        ip_address=ip,
        geo=geo,
        user_agent=request.headers.get("user-agent"),
        idempotency_key=key,
    )
    db.add(s)
    db.commit()
    db.refresh(s)

    background_tasks.add_task(send_confirmation, s.id, body.data.get("email"))

    return JSONResponse(
        {"id": s.id, "status": "stored", "geo": geo},
        status_code=201,
        headers={"Access-Control-Allow-Origin": "*"},
    )
