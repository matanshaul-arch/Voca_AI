# Market positioning — 2026-09-05

## Observed market

- Krisp and LiveKit position background voice cancellation and voice isolation for calls, agents and headset/earbud users; controls include bypass and adjustable suppression.
- Descript positions one-click voice cleanup, echo/noise reduction, intensity control and before/after preview for creators.
- Generic cleanup and nearby-voice suppression are table stakes, not a sufficient Voca differentiator.

## Voca differentiation hypothesis

1. **Consent-based Teacher Lock:** explicit enrollment of the instructor, not merely a presumed primary speaker.
2. **Explainable quality:** target-retention, overlap and microphone-distance warnings, with a clear bypass instead of silently damaging speech.
3. **Teaching workflow:** class interruption timeline, private local capture review, and teacher-specific quality summary.
4. **Privacy posture:** local-first processing; embeddings rather than retained enrollment audio; explicit deletion.
5. **Evidence before claims:** a consented classroom challenge set plus blinded listening and WER tests.

## Product implications

- Add a preservation-versus-suppression control only after a confidence/quality monitor exists.
- Make before/after listening and per-clip failure feedback part of Teach Mode.
- Keep WebRTC/AEC as an integration layer, rather than competing with generic call filters.
- Do not claim reliable equal-level single-mic overlap isolation until the Chen capture and fresh challenge set support it.

## Sources

- [Krisp AI Voice SDK](https://sdk-docs.krisp.ai/)
- [Krisp BVC/NC documentation](https://sdk-docs.krisp.ai/docs/krisp-rtc-bvc-nc)
- [LiveKit voice isolation documentation](https://docs.livekit.io/cloud/noise-cancellation/)
- [Descript Studio Sound](https://www.descript.com/studio-sound-2)
