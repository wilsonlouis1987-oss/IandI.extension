# I&I BIM Tools License API

Starter FastAPI + SQLite service for Pro license issue, activation, device limits, validation, deactivation and revocation.

Run: pip install -r requirements.txt; set IANDI_ADMIN_TOKEN to a long secret; then run uvicorn app:app --host 0.0.0.0 --port 8000.

Endpoints: GET /health; POST /v1/license/activate; POST /v1/license/validate; POST /v1/license/deactivate; POST /v1/admin/licenses (Authorization header is admin token); POST /v1/admin/licenses/revoke?license_key=... (Authorization header is admin token).

Only SHA-256 license hashes are stored. Deploy behind HTTPS with persistent database backups. This API is a backend starter and is NOT yet integrated with the Dynamo graphs or payment checkout. Feature gating must be enforced by the launcher/online validation, not by hiding ribbon buttons alone.
