# I&I BIM Tools License API

FastAPI + SQLite Pro licensing backend. It issues keys, activates keys on devices, validates each Pro tool, deactivates a device, and revokes keys. Only SHA-256 key hashes are stored; the raw key is returned once at issuance.

## Local run

```bash
pip install -r requirements.txt
export IANDI_ADMIN_TOKEN='use-a-long-random-secret'
export LICENSE_DB='./licenses.db'
uvicorn app:app --host 127.0.0.1 --port 8000
```

## Routes

- `GET /health`
- `POST /v1/license/activate`
- `POST /v1/license/validate`
- `POST /v1/license/deactivate`
- `POST /v1/admin/licenses` (Authorization header)
- `POST /v1/admin/licenses/revoke` (Authorization header, JSON body `{"license_key":"..."}`)

The updated source package integrates the client guard into all 59 Dynamo graphs: 10 selected Free IDs bypass validation and 49 Pro IDs fail closed unless the HTTPS API returns valid=true. License Manager supports activate/check/deactivate.

## Production status

The source and automated tests are prepared. The Render Blueprint uses a persistent disk and requires billing information in this account; no live service has been deployed. Revit/Dynamo runtime QA, official checkout, and automatic key delivery are not yet complete. Do not sell Pro until these are completed.