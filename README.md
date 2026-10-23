# Madhava for Android

A personal Android companion with WhatsApp-inspired chat, a local 3D Krishna avatar, Gemini text conversations, and bidirectional Gemini Live audio with optional camera frames.

## Install

Install `Madhava-v1.35.apk` on Android 8 or newer. Open Settings and paste your own Google AI Studio API key. Tap Save key, then Test & refresh models. Return to chat, or use the phone / video button. The video button opens the 3D avatar call screen. Turn the camera on explicitly to send camera frames to Gemini. Preview 3D avatar works offline without a key.

The APK is a universal Android package, not a React Native build. It uses a small Java Android shell and an entirely bundled HTML/JS/Three.js UI. No server or external model-download service is required. Gemini API access and quota are required for real responses.

## Features

- Local message and call-transcript history.
- Android Keystore AES-GCM encryption for the personal API key; Android backup disabled.
- Gemini text model selection and bounded fallback on unavailable / quota / transient server errors.
- Live WebSocket audio, microphone capture, PCM streaming, queued audio playback and interruption handling.
- Callbacks for open, setup, audio, transcripts, turn completion, interruption, session resumption, go-away, model fallback, error, close and fatal failure.
- Session-resumption handles and bounded reconnect; hang-up cancels pending retries.
- Microphone mute, output mute, optional front camera sharing at less than one frame per second, and local self preview.
- Camera and microphone permission prompts; calls end when the app moves to the background.
- Articulated local 3D Krishna model with automatic arm and wrist gestures, subtle head motion, breathing, blinking and audio-reactive mouth opening. Gestures follow the actual playback amplitude; this is stylized animation, not phoneme lip sync or photorealism. Ask during a call to see Vishwaroopa; ask to return to Krishna to restore the normal form. No automatic random form changes.
- Telugu, Hindi and English preference; five selectable Gemini voices.

## Version 1.6 Rama and Vamana

Rama reuses the detailed Krishna sculpted clothing, garlands, ornaments, face and crown, with the peacock feather and flute removed, a curved gold bow held at its central grip, an arrow and a back quiver. Vamana is rebuilt as a tiny youthful figure with a round face, larger eyes, soft cheeks, short limbs, a small umbrella and water pot. Both retain conversational head movement, blinking and mouth animation. 

## Version 1.4 Dashavatara forms

Bundled local models (replaced in 1.23 by realistic textured GLBs): Matsya, Kurma, Varaha, Narasimha, Vamana, Parashurama, Rama, Krishna, Buddha and Kalki. This list uses Buddha as the ninth form; Vishwaroopa remains separate. Each of the nine additions has distinct modeled features and props. Kalki is seated astride a white horse, with bent thighs, hanging boots and stirrups, reins and a raised sword. Narasimha has a broader muscular torso, sculpted chest and abdominal muscles, larger mane, narrowed amber eyes, exposed fangs and claws. These are stylized devotional figures, not photorealistic sculptures.

During a call ask, for example, "Show Narasimha", "నరసింహ రూపం చూపించు", or "राम रूप दिखाओ". A Gemini Live form tool handles broader requests, and a local transcript matcher handles explicit names. The call waits for an asset to load before confirming display; errors leave the preceding form visible. The Form picker also works in offline preview. Forms persist until requested again or the call ends. The conversation retains the disclosed devotional portrayal rather than claiming literal divine transformation. Head motion, blinking and audio-reactive mouth opening continue on each new model.

## Version 1.3 visual correction

Restores a visible gold flute held by both articulated hands in front of the shawl. Speech motion is restrained to preserve the flute grip. Universal-form artwork now contains ten varied side faces, sixteen additional arms with different held objects, a serpent canopy, ornate necklaces, sun/moon and a star field. It is a stylized interpretation of the user reference, not a photorealistic reproduction. English is the default greeting unless the user chooses or speaks another language.

## Version 1.2 additions

The shared text/voice persona uses a warm first-person devotional portrayal with natural Telugu, Hindi or English. The UI retains AI disclosure; direct identity questions receive an honest answer. Local lexical Gita retrieval includes 701 Sanskrit verse records and 313 public-domain Edwin Arnold poetic passages. Exact Sanskrit verses carry chapter/verse references; the English poetic rendering carries chapter-only references. Authored reading aids are labeled paraphrases. Gemini Live can invoke lookup_gita and set_avatar_form callbacks. No modern copyrighted commentaries are bundled. See sources/GITA-SOURCES.md.

## Models researched on 1 October 2026

Defaults: `gemini-3.8-flash` for text and `gemini-3.8-live` for calls.
Text fallbacks: `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`.
Live fallbacks: `gemini-3.1-flash-live-preview`, `gemini-2.5-flash-native-audio-preview-12-2025`.
The final legacy Live fallback may require preexisting account access. The app can refresh Google's models list using your key. A listed model is not a guarantee of available quota. Fallback can use different model pricing.

Official references:
- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket
- https://ai.google.dev/gemini-api/docs/live-api/capabilities
- https://ai.google.dev/api/live

## Build

Node.js, JDK 17, Android build tools 35.0.0 and Android platform 35 are required. Set `JAVA_HOME`, `ANDROID_BUILD_TOOLS` (directory with aapt2/d8/apksigner/zipalign), and `ANDROID_JAR` (full android.jar path). Run `npm ci`, `npm test`, then `bash build-local.sh`.

`development.jks` is a development-only signing key (password `android`) included so future personal builds can replace this app without losing local data. Do not use this key for a public production release.

## Verification and limits

The APK compiles, packages and verifies its v2/v3 signatures. Automated tests cover PCM encoding/decoding, REST fallback/auth failure handling, thought-part filtering, Live setup/audio/transcripts/interruptions, session resumption and cancelling reconnect when a call ends. Desktop UI checks were attempted but Chromium was blocked by workspace socket restrictions, so those checks did not complete. No real Gemini credential was provided, so authenticated Gemini replies, actual microphone/camera hardware, device-specific echo cancellation, Android runtime permission prompts and on-device performance have not been verified. This is a personal-use first build.

The avatar represents an AI companion inspired by Krishna's teachings; it does not claim to be the deity. Camera output shown on the call screen is the local avatar, not generated Gemini video. Optional user camera images go to Gemini for visual understanding. Chat, microphone and camera data are sent only to Google's API when the corresponding feature is used.
