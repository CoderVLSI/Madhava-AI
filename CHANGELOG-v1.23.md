# Madhava 1.23

- New realistic textured 3D models for all forms (`Imported-Krishna.glb`, `forms/*.glb`, including a new Vishwaroopa). The older toy-style Krishna/Vishwaroopa models and their Blender masters were removed.
- Models were optimised for phones: simplified meshes (500k to 80-245k triangles for the heaviest), 1024px WebP textures (2048px for Krishna). Facial Talk/Blink morph targets are preserved.
- Avatar: morph-target mouth and blink, WebView-safe texture loading, per-form lighting/exposure, bounded model cache, lower joint motion on realistic models.
- Persona: dignified, jnani-inspired Krishna with everyday-conversation guidance; default voice Orus (Schedar and Algieba added).
- UI redesigned ("Yamuna at dusk": indigo, peacock teal, marigold). Form picker on the call screen is now voice-driven only.
- GitHub Actions workflow builds a signed APK on every push (`.github/workflows/build-apk.yml`).
