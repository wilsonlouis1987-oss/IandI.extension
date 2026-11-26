# I&I BIM Tools for Revit

I&I BIM Tools is a pyRevit extension that runs Dynamo automation graphs for Revit workflows.

- **Website / Store:** https://wilsonlouis1987-oss.github.io/IandI.extension/store.html
- **Latest installer release:** https://github.com/wilsonlouis1987-oss/IandI.extension/releases/latest
- **License API source:** [license_server](license_server/)
- **License deployment guide:** [DEPLOY_RENDER.md](license_server/DEPLOY_RENDER.md)

## Free tools

The current 10 no-license tool IDs are A02, A07, B01, B12, B15, B16, B22, C03, D09 and D13.

## Pro licensing status

The integrated source package has online guards in the main Python node of all 59 Dynamo graphs (10 Free + 49 Pro), plus a pyRevit License Manager. The license API source supports issue, activate, validate, device deactivate and revoke. API unit tests run in GitHub Actions.

**Release is not production-ready yet:** the live HTTPS API has not been deployed because the configured persistent database service requires Render billing setup; Revit/Dynamo runtime QA and a refreshed installer are pending; no official checkout or automated key delivery is connected. Please do not purchase Pro until the website announces a tested release.

An updated integrated source ZIP has been prepared for the owner, but it has not yet been attached as a public GitHub release asset.