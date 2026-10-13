# BUILDLOG

## AI assistance
AI was used to accelerate scaffolding, API design, documentation, and test planning.

## Human ownership
The implementation was reviewed against the capstone brief. The final owner must be able to explain authentication, tenant filters, CORS, rate limiting, cache headers, the geo fallback, idempotency, and background side-effect handling.

## Known AI-assisted tradeoffs
- The rate limiter is intentionally process-local for a $0 local capstone; production would use shared storage.
- Password hashing is intentionally minimal for the demo and should be replaced with Argon2/bcrypt in a production service.
- Geo responses are normalized defensively because free providers can vary.

## Verification discipline
No secret is placed in source. `.env.example` contains placeholders only. `EVIDENCE.md` is designed to hold real command output rather than invented claims.
