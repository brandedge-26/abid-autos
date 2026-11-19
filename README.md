# Abid Autos Workshop website

Responsive static website for Abid Autos Workshop, Lahore. No package installation or build step is required.

## Run locally

```bash
python3 -m http.server 4173 --directory dist
```

Open `http://localhost:4173` in a browser. Deploy the contents of `dist/` to any static web host.

## Source layout

- `dist/index.html` — content, SEO metadata, service and package sections
- `dist/styles.css` — desktop and mobile layouts, transitions, stacked service scenes
- `dist/script.js` — navigation, scroll effects, pricing toggle, engine assembly controls
- `dist/assets/engine/assembly/` — 25 optimized frames of the 3D-rendered opening sequence
- `art/engine_render.py` — Blender source that creates the illustrative engine and its six component groups
- `.openai/hosting.json` — configuration for the existing ChatGPT Site

The engine can open and reassemble by button, slider, keyboard, or horizontal drag. Numbered markers reveal six component descriptions when fully open. The service photography loads from Unsplash and the fonts load from Google Fonts, so those visuals require an internet connection. Calls, WhatsApp booking links, and Google directions point to Abid Autos' supplied contact details.
