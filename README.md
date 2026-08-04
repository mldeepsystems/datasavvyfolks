# Data Savvy Folks 📊

The landing page for **Data Savvy Folks** — a vibrant community for analysts, data engineers, data scientists, ML/AI & GenAI builders, and everyone aspiring to break into data.

🔗 **Live site:** https://mldeepsystems.github.io/datasavvyfolks/

## What's here

A single, self-contained `index.html` (no build step, no dependencies) that covers:

- Hero with animated member counter (260 → 1,000 goal)
- Featured upcoming event (currently the Aug 6 "Breaking Into Data" session)
- Mission, Vision & Values
- Why join / member benefits
- The disciplines inside the community
- The vetted join flow (LinkedIn → review → WhatsApp invite)
- Sponsor credit for **MLDeep Systems**

## Editing

Everything lives in `index.html`. The most common edits are near the top of the file:

| What | Where |
|------|-------|
| Brand colors | `:root { ... }` CSS variables |
| Member count / progress bar | search `data-count="260"` and `bar.style.width = '26%'` (260 / 1000) |
| Next event | the `▼ EDIT THIS BLOCK ▼` marker in the Event section |
| Join link | `https://www.linkedin.com/in/anmol01` |
| Event link | `https://luma.com/riabx20e` |

## Assets

- `og-image.png` — 1200×630 social share card
- `favicon.svg`, `favicon-32.png`, `favicon.ico`, `apple-touch-icon.png` — site icons

Regenerate the images with the script in the project history (Pillow-based).

## Deploy

Hosted via **GitHub Pages** from the `main` branch root. Any push to `main` updates the live site.

---

Sponsored by [MLDeep Systems](https://www.mldeep.io) · Built with 💜 for the community.
