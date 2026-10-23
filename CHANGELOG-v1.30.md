# Madhava 1.30

- Interactive explanations: when a concept is clearer as something to touch or watch (diagram, step-through, slider, timeline, breathing pacer, quiz), Krishna can add one Gemini-written interactive page under his text answer. It appears as a "Krishna explains" card with an expand button.
- Safety design: generated code runs in a sandboxed frame served from its own address with a strict Content-Security-Policy (no network, no storage, no access to the app page). The native bridge now requires a one-time secret that only the app's own script knows, so generated code cannot read the saved API key. Widgets that mention the bridge or embed other content are rejected.
- Only the latest interactive card loads automatically; older ones open on tap. Widget code is kept only for the 6 most recent messages.
- Persona prompt extended with widget design rules (phone-sized, offline, calm).
