# Dinext source upgrade

Selected upstream release: [v1.88.0](https://github.com/frappe/crm/releases/tag/v1.88.0).
Immutable upstream commit: `0baa1e8ea462b92d2920bcfdc7a532a730329b6c`.
Dinext integration line: `main/v15`.

## Preserved company changes

Keep the existing form-script extension and unit-test contracts. The selected release uses the shared @framework/ui package from the adjacent Frappe repository and requires Node 20.19+ or 22.12+.

## Verification and activation

Use the existing Dinext validation workflow and the tests/build commands declared by the application. Browser and migration checks must use an isolated Frappe 15 test site with synthetic data. Upstream publication workflows remain disabled.

This source update does not change a running site or deployment manifest. A runtime cutover requires verified backups, the exact accepted fork commit and matching release evidence. Keep the preceding source line available for rollback.
