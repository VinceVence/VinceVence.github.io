# Guwa Website Migration Report

Audited on 2026-07-12.

## Repository State

- Repository: `VinceVence/VinceVence.github.io`
- Branch: `feature/guwa-website-rebrand`
- Starting HEAD and `origin/main`: `e7882795da09ed46784e9014023f2ab42da87ab4`
- Starting divergence: 0 behind, 0 ahead
- CNAME: exactly `guwa.app`
- No push, deployment, DNS change, email change, or external publication was performed

## Migration Completed Locally

- Replaced active Questle branding with Guwa and Guwa Pro.
- Rebuilt the homepage around implemented application features only.
- Used the approved Guwa mark, palette, Sora font, production sprites, and
  current application screenshots from the Flutter repository.
- Added the public Founder Pass code, eligibility/capacity/cutoff copy, and an
  accessible copy control.
- Rewrote Privacy, Support, Account and Data Deletion, 404, Play Assets, and the
  old in-site privacy redirect page.
- Added Guwa canonical URLs, Open Graph/Twitter metadata, JSON-LD, favicon,
  Apple touch icon, web manifest, robots file, and sitemap.
- Removed directly addressable stale Questle screenshots, marketing graphics,
  CSS/JS, icon, illustrations, and the obsolete generator.

## Accurate Privacy and Support Claims

- Activity progress, notes, moods, custom activities, and photo memories are
  local-first.
- Photo files and local paths are not uploaded by Account Backup.
- Google Sign-In and Firebase authentication are optional.
- Account Backup stores progress only and is scoped to the authenticated owner.
- Google Play Billing and RevenueCat provide purchase/entitlement behavior.
- App Check and Play Integrity protect eligible Firebase requests.
- Promotion eligibility and capacity are verified securely in the app.
- There is no claim of a complete in-app deletion control.
- Deleting local/backup data does not cancel a Google Play subscription.

## QA Results

- Static verifier: 5 active pages passed.
- `html-validate`: 7 HTML documents passed with no errors or warnings.
- JavaScript syntax, manifest JSON, and sitemap XML: passed.
- Local HTTP routes: homepage, privacy, support, account deletion, and Play
  assets returned 200; an invalid route returned 404.
- Founder Pass copy interaction: button changed to `Copied` and announced
  `Founder Pass code copied.` through the live region.
- Responsive widths: 320, 375, 390, 768, 1024, and 1440 pixels passed with
  document width equal to viewport width.
- Rendered homepage inventory: 1 font, 1 stylesheet, 1 script, and 8 images.
- Observed homepage resources: approximately 2,339,096 bytes before transport
  compression and browser caching.
- Repository blobs before migration: 21,910,509 bytes across 92 files. The
  working tree after migration and QA previews is approximately 12.8 MB.

Screenshots are stored under `docs/website/preview/`.

## Intentional Questle References

- `Questle is now Guwa` and `formerly known as Questle`: transition context.
- JSON-LD `alternateName`: search transition metadata.
- `com.vincevence.questle`: unchanged Google Play package ID.
- Verification-script forbidden-pattern assertions: regression protection.

## Not Yet Production

The migration exists only on the local feature branch. `guwa.app` will continue
to serve stale production content until this branch is reviewed, pushed, merged,
and GitHub Pages completes deployment. Legacy `questle.org` redirects and email
delivery are separate blockers documented in the app release repository.
