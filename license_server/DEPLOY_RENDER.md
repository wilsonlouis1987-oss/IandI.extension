# Deploy I&I BIM Tools License API on Render

The repository now contains a Render Blueprint (`render.yaml`) and Docker image. This prepares deployment; it does not create a live service until you connect your Render account and confirm the deployment.

## Deploy
1. Sign in to Render and choose **New → Blueprint**.
2. Connect GitHub and select `wilsonlouis1987-oss/IandI.extension`.
3. Render reads `render.yaml` and creates the web service with a persistent disk.
4. When prompted for `IANDI_ADMIN_TOKEN`, create a long random secret (at least 32 random bytes). Set it only in Render Environment; never commit it or paste it into public chat.
5. Deploy. Confirm `/health` returns `{"ok":true,"service":"I&I BIM Tools License API"}`.
6. Copy the service's HTTPS URL and configure the Revit extension's `IANDI_LICENSE_API` to that URL.

## Important limitations before selling
- The API is a starter implementation, not yet production audited.
- No payment provider or automated purchase-to-license delivery is connected.
- Pro validation helper still needs to be wired into every Pro tool and tested inside supported Revit/pyRevit versions.
- The current API uses SQLite; the Blueprint provisions a persistent disk. Keep the disk mounted at `/data`.
- The existing website HTML needs to be uploaded to the actual website host to publish the updated Store section.
- Do not announce that Pro locks are active until the Revit integration and installer have been tested.

## Admin license creation
After deployment, create licenses through the protected admin endpoint:
`POST /v1/admin/licenses` with JSON such as `{"plan":"pro","days":365,"max_devices":1}` and header `Authorization: <IANDI_ADMIN_TOKEN>`.
The response includes the license key. Deliver keys privately only after payment confirmation. Keep admin token and keys secret.
