# Guwa Live Versus Local Audit

Audited on 2026-07-12. The live site is the deployed `origin/main` Questle site.
The replacement exists only on local branch `feature/guwa-website-rebrand`.

| Live page | Stale element | Current live content | Required Guwa replacement | Local status | Asset replacement | Deployment |
| --- | --- | --- | --- | --- | --- | --- |
| `/` | Browser title and metadata | Questle title, description, canonical/social URLs, and Questle feature graphic | Guwa title, `guwa.app` canonical/social metadata, approved Guwa OG art | Complete | Yes | Not deployed |
| `/` | Header and navigation | Questle wordmark, Catalog/Trail/Pro labels, old app CTA | Approved Guwa mark/wordmark, Features, Memories, Guwa Pro, Founder Pass, Privacy, Support | Complete | Yes | Not deployed |
| `/` | Hero | “Small quests for ordinary days,” Questle copy, rejected Questle marketing art | “Small adventures for ordinary days,” real Guwa Home, generated doorway cat | Complete | Yes | Not deployed |
| `/` | Product terminology | Today’s Questle, custom Questles, private Questle Trail | Today’s Quest, custom activities, Guwa Trail | Complete | No | Not deployed |
| `/` | Product screenshots | Questle-era marketing captures | Current Guwa Home, Trail, Badges, and Profile captures | Complete | Yes | Not deployed |
| `/` | Memory/progress art | Questle map and catalog artwork | Generated Guwa memory/progress illustrations based on production sprites | Complete | Yes | Not deployed |
| `/` | Pro and launch offer | Questle Pro and no Founder Pass section | Accurate Guwa Pro limits plus Founder Pass code/rules | Complete | Yes | Not deployed |
| `/` | Footer | Questle name and old-domain links | Guwa and current Privacy, Support, deletion, and email links | Complete | No | Not deployed |
| `/privacy/` | Title/header/body | Questle name throughout, custom Questles, July 3 date | “Guwa, formerly known as Questle,” current July 12 policy and implementation claims | Complete | Yes | Not deployed |
| `/privacy/` | Contact | `support@questle.org` | `support@guwa.app` | Complete | No | Not deployed |
| `/support/` | Title/header/help copy | Questle, Questle version, old support address | Guwa, current auth/backup/Pro/restore/Founder/photo guidance | Complete | Yes | Not deployed |
| `/account-deletion/` | Data instructions | Questle local/backup instructions and old email subjects | Separate Guwa local, backup, auth, support, and subscription instructions | Complete | Yes | Not deployed |
| All pages | Favicon/social/platform assets | Questle assets | Approved Guwa favicon, app icon, OG image, and feature graphic | Complete | Yes | Not deployed |

No live production file was changed. Deployment remains intentionally pending
visual approval, push, merge, and GitHub Pages publication.
