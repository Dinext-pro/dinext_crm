# Dinext source upgrade

Selected upstream release: [v1.88.0](https://github.com/frappe/crm/releases/tag/v1.88.0).
Immutable upstream commit: `0baa1e8ea462b92d2920bcfdc7a532a730329b6c`.
Dinext integration line: `main/v15`.

## Preserved company changes

Keep the existing form-script extension and unit-test contracts. The selected release uses a pinned MIT-licensed @framework/ui client package under frontend/vendor/framework-ui from frappe/frappe 4515014c87ece6cb20ee91d2cfb121c5cbd1ff4a. This follows upstream CRM frontend builds against version-16 client components while retaining the Frappe 15 server. Node 20.19+ or 22.12+ is required.

## Verification and activation

Use the existing Dinext validation workflow and the tests/build commands declared by the application. Browser and migration checks must use an isolated Frappe 15 test site with synthetic data. Upstream publication workflows remain disabled.

This source update does not change a running site or deployment manifest. A runtime cutover requires verified backups, the exact accepted fork commit and matching release evidence. Keep the preceding source line available for rollback.

## Verification record — 2026-10-18

On the isolated Frappe **15.119.0** site, 294 frontend unit tests and 62 server tests (forms and utilities) passed. Frozen frontend installation, the production frontend build and `bench build --apps crm,wiki,insights` passed with Node 22.23.2. The Cypress scenario opens a synthetic lead, executes its stored Form Script action and verifies the resulting notification.

The pinned `@framework/ui` package contains 352 regular upstream UI source files verified against Git blob IDs, plus the upstream MIT license and `DINEXT-SOURCE.json`. The Frappe server itself is unchanged.

The repeatable Cypress project lives in this application. Its synthetic-fixture endpoints check `allow_tests`, development/test context and the System Manager role on every call; fixture data uses only reserved test identities. Run it only on a disposable test site.
