# Deploy I&I BIM Tools License API on Render

## Deployment
1. Sign in to Render and choose New → Blueprint.
2. Connect `wilsonlouis1987-oss/IandI.extension` and select the `main` branch.
3. Render reads `render.yaml` and proposes the API service plus a persistent disk.
4. Set `IANDI_ADMIN_TOKEN` to a long random secret in Render Environment; never commit it or share it in chat.
5. Deploy only after reviewing the plan and price. The current persistent-disk service is a paid plan and this account's Blueprint attempt stopped at the billing-information requirement.
6. Verify `/health` returns `{"ok":true,"service":"I&I BIM Tools License API","version":"1.1.0"}`.
7. Copy the HTTPS service URL into License Manager and activate a test key.

## Safety
- Do not use ephemeral filesystem storage for the SQLite database; keys/activations would be lost on restart.
- Keep database backups and the admin token private.
- Create keys only after confirmed payment. No checkout or automatic purchase-to-key delivery is configured.
- The 59 Dynamo graph guards are integrated in the source package, but do not distribute the refreshed paid installer until the live API and Revit/Dynamo runtime tests pass.

## Admin issue/revoke
Create a key with `POST /v1/admin/licenses`, JSON `{"plan":"pro","days":365,"max_devices":1}`, header `Authorization: <IANDI_ADMIN_TOKEN>`. The raw key is returned once.
Revoke with `POST /v1/admin/licenses/revoke`, JSON `{"license_key":"IIBIM-..."}`, same Authorization header.