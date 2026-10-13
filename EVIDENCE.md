# Evidence

Paste the real terminal output below as the system is exercised. The acceptance matrix is included so each Section 6 requirement has a named proof.

| Requirement | Proof command / check |
|---|---|
| Authenticated CRUD | `POST /widgets` without bearer returns 401; authenticated create/list/update/delete succeeds |
| Tenant isolation | Create two users/tenants; token A requests widget ID owned by B and receives 404 |
| Embed snippet | `GET /widgets/{id}/snippet` returns one script line |
| Cached config | `curl -i /widgets/{id}/config` shows `Cache-Control: public, max-age=60` |
| Versioned widget JS | `curl -i /widget.js?id={id}` shows `Cache-Control: public, max-age=31536000, immutable` |
| Cross-origin submission | Demo on port 5500 submits to API on 8000; browser accepts CORS response |
| Invalid payload | Malformed JSON / missing required fields returns 4xx JSON, not 500 |
| Oversized payload | Body over 65536 bytes returns 413 |
| Rate limiting | Rapid requests produce 429; later legitimate request succeeds after the window |
| Spam control | Non-empty `honeypot` returns 202 with `dropped` and no stored row |
| Geo fallback | `MOCK_GEO_A_DOWN=1` causes provider B attempt; both mock-down stores with `geo: null` |
| Safe side effect | Force confirmation failure; stored submission still returns 201 |
| Dashboard | `GET /dashboard/submissions` and `/dashboard/stats` show tenant-scoped data |
| Idempotency | Repeat same `Idempotency-Key` returns duplicate result instead of another row |
