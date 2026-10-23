# Madhava release readiness

Reviewed 3 October 2026. This is an implementation checklist, not a claim of Play approval or a deployed service.

## Current release blockers

| Blocker | Evidence / required outcome |
|---|---|
| Target SDK | Manifest now targets 36; Android 16 behavior remains unverified on hardware. Google's current policy requires new mobile apps and updates to target API 36 from 31 August 2026; an account-specific extension may be available until 1 November. Verify Android 16 behavior before submission. |
| Production package and signing | Current local build produces an APK with a publicly included development key. Produce an AAB, use Play App Signing with a protected upload key, and exclude development.jks from public distribution. A new signing identity cannot replace the personal build without a migration/reinstall plan. |
| Managed AI access | Current client uses each user's API key directly. Do not embed a shared Gemini key or the scaffold service bearer token in the public app. Add per-user/installation authentication, attestation, quotas, billing limits, and server-side model allowlists. |
| Actual content reporting | Local saving/export helps capture feedback but does not deliver reports to the developer. Connect an authenticated report endpoint, provide delivery/pending/error states, and operate a real review/remediation process. |
| Privacy and Data Safety | Publish an active public privacy-policy URL and accurate Data Safety answers covering Google AI processing, microphone/camera frames, local transcripts, reports, retention and deletion. Determine paid/free Gemini data handling for the actual account. Permission disclosure must precede unexpected collection. |
| Accounts, if introduced | Account creation triggers in-app and external-web deletion requirements. Implement deletion of associated server data and document any necessary retention. |
| Device and Gemini validation | No authenticated Gemini or Android hardware calls were previously verified. Test actual voice/camera permissions, denial/regrant, interruption, echo, Bluetooth, weak networks, background hangup, heat/battery and all form transitions on multiple real devices. |
| Scripture quality and rights | Existing Sanskrit + chapter-level Arnold poetic rendering is not a reviewed verse-aligned modern translation. Keep labels accurate, review retrieval errors, license new Telugu/Hindi translations and record asset/audio rights. |
| Store setup and testing | Finish app access instructions, target audience/content rating, contact details, screenshots and declarations. Personal developer accounts created after 13 November 2023 require at least 12 opted-in testers continuously for 14 days before applying for production access. |

## Runnable development backend

`server/server.mjs` runs with Node 22+, no dependencies:

```sh
MADHAVA_ACCESS_TOKEN='a-long-development-secret' GEMINI_API_KEY='server-only-key' REPORT_DIR='/private/persistent/madhava-reports' node server/server.mjs
node --test server/server.test.mjs
```

It binds loopback, requires a bearer token on POSTs, limits JSON bodies to 40 KB, limits requests per direct peer to 20/minute, writes reports to restricted-permission JSONL, calls Gemini with a server-side key in a header, bounds upstream timeouts and returns generic upstream errors. It never logs content or keys. Do not expose it publicly as-is. A fixed bearer token is a development gate, not mobile authentication; IP limiting alone is not abuse protection. No CORS is deliberately configured; integrate an authenticated native client or approved origin policy explicitly.

| Endpoint | Request | Response |
|---|---|---|
| `GET /health` | none | `{ok:true}` |
| `POST /v1/reports` | `{id,category,content,comment?}`; category `incorrect_scripture`, `offensive`, `unsafe`, `other`; id <=80 safe chars; content 1–6000 chars; comment <=1000 | HTTP 202 `{id,status:"pending_review"}` only after durable append; does not mean reviewed |
| `POST /v1/chat` | `{messages:[{role:"user" or "assistant",text}]}`; 1–30 messages, <=6000 chars each | `{id,text,model}`; model and persona selected by server |
| `POST /v1/live-token` | `{language?:"Auto" or "English" or "Hindi" or "Telugu"}` | `{token,model,expiresAt}`; one-use short-lived Gemini Live token |

`GEMINI_TEXT_MODEL` and `GEMINI_LIVE_MODEL` override server defaults `gemini-3.8-flash` and `gemini-3.8-live`, verified against official model documentation on the review date. Actual project quota/access remains unverified. Live token minting uses the documented alpha REST resource and must be credential-tested before use. The existing WebSocket client uses the beta service and a permanent-key query; it must explicitly adopt the documented alpha token flow and matching server constraints. Token support is Live-only, not a text proxy substitute.

The scaffold intentionally has no deployment, user database, billing integration, full scripture retrieval or moderation dashboard. Its text persona is a conservative placeholder. Before managed mode ships, move reviewed scripture retrieval and source identity to the server, constrain tool declarations/voice/persona in Live token minting, and keep public clients from replacing those constraints. Server report processing must have an assigned reviewer, secure access, retention/deletion policy and actions on harmful output.

For strict cost ceilings, use a metered server WebSocket relay or a verified provider-side session limit. A client timer and token TTL alone are not authoritative spend controls. Add per-user quotas, concurrency limits, token issuance budgets, key rotation, secret management, HTTPS ingress, trusted proxy configuration, durable encrypted storage, idempotent report IDs, redacted operational metrics and alerting before production. Do not log raw audio, camera frames, prompts, tokens or scripture-linked private journal entries.

## Official sources

- AI content and in-app reporting: https://support.google.com/googleplay/android-developer/answer/13985936
- User data/privacy/account deletion: https://support.google.com/googleplay/android-developer/answer/10144311
- Target API deadlines: https://support.google.com/googleplay/android-developer/answer/11926878
- Personal-account closed testing: https://support.google.com/googleplay/android-developer/answer/14151465
- Android App Bundles: https://developer.android.com/guide/app-bundle
- Gemini models: https://ai.google.dev/gemini-api/docs/models
- Live ephemeral tokens: https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens

Recheck requirements in the actual Play Console account before uploading. Policy compliance does not guarantee approval.
