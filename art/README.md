# Engine assembly render source

`engine_render.py` builds the illustrative inline-four engine, its six component groups, lighting, and the opening sequence in Blender. It renders 25 transparent PNG frames in `art/assembly` with:

```bash
ENGINE_MODE=sequence blender -b -noaudio -t 8 --python art/engine_render.py
```

The website uses optimized WebP copies in `dist/assets/engine/assembly/`. The control in `dist/script.js` scrubs these rendered 3D positions forward to open the engine and backward to assemble it. Component markers and descriptions are mapped to the final opened view.
