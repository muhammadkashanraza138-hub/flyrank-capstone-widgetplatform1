# FlyRank Capstone — Embeddable Widget & Lead-Capture Platform

A small multi-tenant FastAPI platform that lets an authenticated owner create widgets, generate an embed snippet, serve cached widget assets/configuration, accept cross-origin public submissions, rate-limit and spam-filter them, enrich IPs through a provider fallback chain, persist leads in PostgreSQL, run a non-critical confirmation side effect, and expose dashboard analytics.

## Architecture

```text
Owner -> Authenticated API -> PostgreSQL
                    |
                    +-> Widget CRUD -> embed snippet

Customer site (origin :5500)
      |
      +-> GET /widget.js -> long cache
      +-> GET /widgets/{id}/config -> short cache
      +-> POST /submissions -> CORS -> validation -> rate limit/honeypot
                                      -> Geo A -> Geo B -> no-geo fallback
                                      -> PostgreSQL
                                      -> background confirmation side effect

Owner -> Dashboard API -> tenant-scoped submissions + stats
```

## Run

1. Copy `.env.example` to `.env` and change `JWT_SECRET` for non-demo use.
2. Run:

```bash
docker compose up --build
```

3. Register a demo owner:

```bash
curl -X POST http://localhost:8000/auth/register -H 'Content-Type: application/json' -d '{"email":"demo@example.com","password":"password123"}'
```

Use the returned bearer token to create a widget:

```bash
curl -X POST http://localhost:8000/widgets -H "Authorization: Bearer TOKEN" -H 'Content-Type: application/json' -d '{"type":"signup","title":"Join us","description":"Leave your details","fields":[{"name":"name","label":"Name","required":true},{"name":"email","label":"Email","required":true}],"button_text":"Subscribe","display_options":{}}'
```

Then request `/widgets/{id}/snippet`. Paste the returned script into `demo/index.html`, replace `PASTE_WIDGET_ID`, and serve the demo from a second origin:

```bash
python -m http.server 5500 --directory demo
```

Open `http://localhost:5500`.

## API

- `POST /auth/register`, `POST /auth/login`
- Authenticated widget CRUD: `POST/GET /widgets`, `GET/PUT/DELETE /widgets/{id}`
- `GET /widgets/{id}/snippet`
- Public `GET /widgets/{id}/config`
- Public `POST /submissions?widget_id={id}`
- Authenticated `GET /dashboard/submissions`, `GET /dashboard/stats`
- `GET /health`

## Security and resilience

- JWT authentication for owner APIs.
- Every widget/submission query is tenant-scoped.
- Pydantic boundary validation plus a 64 KiB request limit.
- CORS and explicit OPTIONS handling.
- In-memory per-IP and per-widget rate limiting with 429 responses.
- Honeypot spam field.
- Idempotency-Key prevents duplicate submissions.
- Geo provider A -> provider B -> no-geo fallback.
- Geo failures never fail the submission.
- Confirmation is a background side effect with retry attempts and an alert log; its failure does not roll back the stored lead.
- PostgreSQL persistence and Alembic migration.
- Secrets are environment variables; `.env` is ignored.

## Tests

```bash
pytest -q
```

## Explicit non-goal

No production hosting, real CDN, visual form builder, or real email delivery is included. The customer site is a local second-origin HTML page, and confirmation email is represented by a local/logged side effect.

## Limitations

The rate limiter is process-local rather than Redis-backed, so multiple API replicas would need a shared limiter. The demo uses SHA-256 password hashing rather than a production password-hashing service; this is intentionally small for the capstone demonstration. Geo APIs can change availability or response shape, which is why the fallback and no-geo path exist.
