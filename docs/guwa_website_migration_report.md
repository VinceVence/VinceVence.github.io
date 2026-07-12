# Guwa Website Migration Report

Audited on 2026-07-12. Status: **READY FOR VISUAL WEBSITE REVIEW**.

## Repository State

- Repository: `VinceVence/VinceVence.github.io`
- Branch: `feature/guwa-website-rebrand`
- Starting HEAD: `48c8ff2bf4f3756b5bf60ac3f3090f10a2de5de8`
- Starting `origin/main`: `e7882795da09ed46784e9014023f2ab42da87ab4`
- CNAME: exactly `guwa.app`
- Application reference: `feature/guwa-rebrand` at `5fce026`
- No push, merge, deploy, DNS, Firebase, RevenueCat, or Play action occurred

## Live Versus Local Audit

Production still serves the Questle title, navigation, hero, screenshots,
product terminology, Pro copy, footer, Privacy, Support, deletion copy, and old
support address. The exact replacement matrix is in
`docs/guwa_live_vs_local_audit.md`. The local branch is complete but undeployed.

## Current Product Inventory

The website was checked against onboarding, Home, daily/catalog activities,
reroll, lock, completion, notes, moods, local photos, Trail views, statistics,
badges, streaks, goals, custom activities, monthly Big Quest, Pro, auth, backup,
restore, Founder Pass, Profile, and legal/support actions. Production-ready,
limited, removed, and intentionally absent features are classified in
`docs/guwa_current_product_inventory.md`.

No planned or removed feature is advertised. Limited features explicitly state
their Pro, sign-in, Play billing, App Check, or local-only conditions.

## Approved Logo and Production References

The approved transparent mark, light wordmark, favicon, store icon, splash mark,
monochrome mark, Home greeting, onboarding poses, profile pose, Trail art, and
badge art came directly from the application repository. Paths, dimensions,
alpha status, hashes, and website uses are recorded in
`docs/website/guwa-brand-asset-manifest.md`.

No approved logo or production sprite binary was edited, recolored, regenerated,
or replaced. Website delivery copies are resized derivatives only.

## ImageGen Illustration System

The built-in ImageGen tool generated six website-exclusive marketing concepts:

1. Hero doorway
2. Find an activity
3. Go experience it
4. Keep the memory
5. Progress your way
6. Founder Pass

Each used three to five approved production references and the Guwa palette. The
source PNGs remain under `assets/guwa-site/source/`. Chroma-key removal created
transparent masters under `assets/guwa-site/optimized/`; responsive 1200, 900,
640, and 400 WebP derivatives plus required PNG fallbacks are preserved.

`assets/guwa-site/guwa-generated-assets.json` records every concept, source
reference, dimension, format, SHA-256, section, alt text, and derivative hash.
The visual review and scoring are:

- `docs/website/preview/guwa-imagegen-review.png`
- `docs/website/guwa-imagegen-evaluation.md`

All six were accepted for sprite consistency, palette, mobile readability,
simplicity, warmth, and non-essential accessible use.

## Homepage Redesign

- Approved Guwa mark and light wordmark in a deep-purple first viewport.
- Generated doorway art and a real current Guwa Home screenshot in the hero.
- Three illustrated “How Guwa works” steps.
- Actual current Home, Trail, Badges, and Profile screens.
- Separate catalog, memory, progress, Guwa Pro, Founder Pass, trust, and CTA
  sections.
- Solid palette bands, Sora typography, restrained borders, and no heavy UI
  framework, fake app screen, or unsupported feature.
- Mobile navigation with accessible expanded state and automatic close behavior.

## Founder Pass

The page shows `GUWAFOUNDERPASS2026`, the readable equivalent, 60-day duration,
30-day account-age limit, 2,000-redemption capacity, October 12, 2026 cutoff,
and in-app eligibility confirmation. Copy interaction changes to `Copied` and
announces `Founder Pass code copied.` through a live region.

## Privacy, Support, and Deletion

- Privacy accurately covers local activities, notes/moods, local photos, Google
  authentication, optional progress-only backup, Firebase, RevenueCat, Google
  Play Billing, App Check, promotions, support, retention, and deletion.
- Support covers app issues, Google Sign-In, Account Backup, Guwa Pro, purchases,
  restore, Founder Pass, photos, privacy, and deletion without requesting secrets.
- Deletion separately covers local app data, cloud backup, authentication access,
  support records, and Google Play subscription cancellation.
- All pages use `support@guwa.app`, current canonical URLs, and July 12, 2026 copy.

## SEO and Platform Assets

All active pages use Guwa titles, descriptions, canonical URLs, Open Graph and
Twitter metadata, favicon, Apple touch icon, manifest, sitemap, robots, theme
color, and accessible alt text. JSON-LD retains Questle only as the transition
`alternateName`; the Play URL intentionally retains package
`com.vincevence.questle`.

New code-rendered assets:

- `assets/brand/guwa-open-graph-1200x630.png`
- `assets/brand/guwa-website-feature-1024x500.png`

Both use approved brand assets and Sora-rendered text; neither contains generated
text or fabricated UI.

## Performance Before and After

| Measure | Before local migration | Final redesigned site |
| --- | ---: | ---: |
| Selected homepage payload | ~2,339,096 B | ~510,421 B |
| Selected image payload | ~2.2 MB | ~378,751 B |
| CSS | one stylesheet | 18,781 B |
| JavaScript | one script | 1,489 B |
| Browser-observed first-view requests | 11 | 16 |
| Largest selected asset | large PNG marketing art | Sora font, 111,400 B |

The request count increases because the page now has real section-specific art,
but responsive WebP delivery reduces selected bytes by roughly 78%. Lazy images
do not block the first view. The six original generated sources are archived for
future design work but are not referenced by page markup.

## Accessibility and Responsive QA

- Semantic heading order, landmarks, skip links, descriptive alt text, focus
  rings, touch targets, legal readability, and live copy status verified.
- Illustrations repeat equivalent HTML meaning and never carry essential text.
- Reduced motion disables smooth scrolling and menu transitions.
- Mobile menu announces Open/Close state and is keyboard-operable.
- Widths 320, 375, 390, 768, 1024, and 1440 were visually tested without
  clipping or incoherent overlap.
- The hero leaves a visible hint of the following highlight band on compact and
  wide viewports.

## Flutter Public Links and Product Capture

The app remains unchanged and clean at `5fce026`. `AppBrand` centralizes:

- `https://guwa.app/`
- `https://guwa.app/privacy/`
- `https://guwa.app/support/`
- `https://guwa.app/account-deletion/`
- `support@guwa.app`

Current app captures under `assets/screens/current/` cover onboarding, Home,
completion/memory, calendar, statistics, Profile/Pro/backup, and Founder Pass
sign-in behavior. Production Android captures supply Home, Trail, Badges, and
Profile images used by the site. ImageGen was never used for app UI.

## Validation Results

- Static page/link/image/canonical verifier: 5 active pages passed
- HTML validation: 7 documents passed
- CSS syntax validation: passed
- JavaScript syntax: passed
- Manifest JSON and sitemap XML: passed
- Local routes: `/`, Privacy, Support, deletion, and Play assets returned 200;
  invalid route returned 404
- Founder Pass copy and mobile navigation interactions: passed
- Secret scan: zero tracked sensitive files and zero high-risk pattern files
- Flutter format: 84 files, 0 changed
- Flutter analyzer: passed
- Flutter tests: 130 passed
- Flutter web/APK/AAB source builds: passed and intentionally unsigned for Android
- Guwa branding, Firebase Auth configuration, and backup-scope verifiers: passed
- `git diff --check`: passed before focused commits

## Remaining Questle References

- `Questle is now Guwa` and `Guwa, formerly known as Questle`: public transition
  context; remove after the migration period.
- JSON-LD `alternateName`: search transition metadata; remove after reindexing.
- `com.vincevence.questle`: immutable Play package identity; retain.
- Audit/redirect documentation: historical and operational context; retain until
  legacy redirects and release migration are closed.
- Verification-script forbidden-pattern checks: regression protection; retain.

No unexplained public Questle branding remains on the local site.

## Preview Files

- `docs/website/preview/guwa-imagegen-review.png`
- `docs/website/preview/final/desktop-homepage.png`
- `docs/website/preview/final/mobile-homepage.png`
- `docs/website/preview/final/hero.png`
- `docs/website/preview/final/activity-section.png`
- `docs/website/preview/final/memories-section.png`
- `docs/website/preview/final/founder-pass.png`
- `docs/website/preview/final/privacy-page.png`
- `docs/website/preview/final/support-page.png`
- `docs/website/preview/final/account-deletion-page.png`

## Focused Commits

- `2e93067` `feat: add Guwa website illustration system`
- `4b93238` `feat: redesign public website for Guwa`
- `f8973b9` `feat: update Guwa privacy support and deletion pages`
- `dbdcea3` `perf: optimize Guwa marketing assets`
- `docs: finalize Guwa website migration report` (this report and QA evidence)

## Deployment and Rollback

After visual approval only:

```bash
cd /private/tmp/guwa-website
git push origin feature/guwa-website-rebrand
```

Open a pull request into `main`, review the exact asset size and page diff, merge,
then wait for GitHub Pages to publish `guwa.app`. Verify all routes, metadata,
Founder Pass copy, email links, responsive widths, and TLS in production.

Rollback by reverting the merge commit on `main` and allowing GitHub Pages to
republish the previous known-good site. Do not alter `CNAME`, DNS, Firebase,
RevenueCat, or the Android package as part of website rollback.

## Remaining Blockers

1. Human visual approval of the six illustrations and final screenshots.
2. Authorized push, pull request, merge, and GitHub Pages deployment.
3. Post-deployment live-route and social-preview verification.
4. Separate `questle.org` path-preserving redirects and support-email delivery
   verification remain release-operation tasks outside this branch.

No local website implementation blocker remains.
