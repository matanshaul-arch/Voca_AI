# Approved dataset release lock

Date: 2026-09-04  
Owner approval: granted in the project session before download  
Storage: local `data/raw/` only; raw audio and archives are Git-ignored

| Dataset | Exact artifact | Bytes | License status | Integrity |
|---|---|---:|---|---|
| LibriSpeech SLR12 | `train-clean-100.tar.gz` | 6,387,309,499 | CC BY 4.0; attribution required; owner-approved | official MD5 `2a93770f6d5c6c964bc36631d331a522`; SHA-256 `d4ddd1d5a6ab303066f14971d768ee43278a5f2a0aa43dc716b0e64ecbbbf6e2` |
| LibriSpeech SLR12 | `dev-clean.tar.gz` | 337,926,286 | CC BY 4.0; attribution required; owner-approved | official MD5 `42e2234ba48799c1f50f24a7926300a1`; SHA-256 `76f87d090650617fca0cac8f88b9416e0ebf80350acb97b343a85fa903728ab3` |
| LibriSpeech SLR12 | `test-clean.tar.gz` | 346,663,984 | CC BY 4.0; attribution required; owner-approved | official MD5 `32fa31d27d2e1cad72775fee3f4849a9`; SHA-256 `39fde525e59672dc6d1551919b1478f724438a95aa55f874b576be21967e6c23` |
| MUSAN SLR17 | `musan.tar.gz` | 11,086,114,085 | OpenSLR lists CC BY 4.0; Voca baseline restricts noise selection to MUSAN `free-sound`, whose bundled license marks selected recordings Public Domain | SHA-256 `86d1061c7e15b5c9e906777685c519701df51bfde3001e1070dcc9ffac955ee1` |
| RIRS_NOISES SLR28 | `rirs_noises.zip` | 1,311,166,223 | OpenSLR lists Apache 2.0; owner-approved | SHA-256 `3b50cfde915b3984738169b4beb341e9f6b8062ae4c2076146c5db71c2c05dc7` |

All gzip/zip integrity checks passed before extraction. This record is engineering provenance, not independent legal advice.

## Baseline derivation

`scripts/prepare_real_baseline.py` creates `voca_real_v1` from LibriSpeech speech, the Public Domain MUSAN FreeSound subset, and SLR28 simulated RIRs. Generated WAV files stay ignored; deterministic JSONL manifests are retained in Git.

Attribution sources:

- LibriSpeech: Vassil Panayotov, Guoguo Chen, Daniel Povey and Sanjeev Khudanpur, *LibriSpeech: An ASR Corpus Based on Public Domain Audio Books*.
- MUSAN: David Snyder, Guoguo Chen and Daniel Povey, *MUSAN: A Music, Speech, and Noise Corpus*.
- SLR28: Tom Ko et al., *A Study on Data Augmentation of Reverberant Speech for Robust Speech Recognition*.
