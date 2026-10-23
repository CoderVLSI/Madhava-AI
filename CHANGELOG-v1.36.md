# Madhava 1.36

- Krishna can now show real 3D models in his interactive cards, built on the spot from code: a spinning Earth with clouds, the Moon, a lotus, a clay pot or diya, a chariot wheel, a temple, a molecule. The person can drag to turn the model and use the card's own controls.
- A three.js toolkit ships inside the app (assets/widget3d.js) and is loaded only by cards that use it. It offers `Madhava3D.stage` (renderer, lights, drag to rotate, resize, calm motion), `Madhava3D.canvasTexture` for painted procedural surfaces and `Madhava3D.rng` for repeatable shapes. If the device cannot draw 3D, the card falls back to a short text explanation.
- Safety is unchanged: cards still run in the network-less sandboxed frame. The only new allowance is loading the app's own bundled script (`script-src 'self'`).
- Persona and tool prompts teach Krishna when a 3D model beats a flat picture and how to build one.
- Dev tools: tools/samples/earth-widget.html and tests/widget3d-check.cjs (real-browser check).
