# Deprecated Dragify imagery

`dragify-looks-*.webp` is a fourteen-up contact sheet in which **every tile already has
a rounded corner baked onto a white ground**. `dragify-look-{1..5}-*.webp` were cut out
of it by the old `tools/dragify-sheet.py` at each tile's bounding box, so those white
corner pixels shipped inside the files. Placed inside a second, differently-radiused CSS
frame, they showed as white triangles in the corners of every thumbnail on the homepage.
It was never a CSS bug — the white was in the image data.

Replaced by `tools/dragify-looks.py`, which exports full-bleed look images straight from
Dragify's own pack data (`Dragify 4.0/App/backend/data/packs/`). Those have no baked
corners, no white ground, and are 768-1024px rather than 422px.

Kept on disk rather than deleted because they are the only copies outside the Dragify
website repo. Nothing in the site references them. Do not reintroduce them.
