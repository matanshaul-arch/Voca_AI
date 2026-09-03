# Voca AI — Dataset inventory and acquisition plan

Date: 2026-09-03  
Scope: T02 — real-data preparation  
Policy: no audio archives or unreviewed metadata are committed to Git.

## Recommended acquisition order

| Dataset | Role | License/access signal | Decision |
|---|---|---|---|
| LibriSpeech | clean target/interferer speech baseline | OpenSLR lists CC BY 4.0 | Candidate for research baseline; retain attribution |
| LibriTTS | more varied read speech | Derived from LibriSpeech; confirm current terms | Candidate after license verification |
| VoxCeleb1/2 | speaker embedding and in-the-wild speech | Official site requires following dataset privacy/access terms | Use only after access and commercial-use review |
| VCTK | accent and speaker diversity | CSTR distributes corpus; verify current corpus license | Candidate for validation and accent coverage |
| DNS Challenge data | environmental noise and enhancement robustness | Terms vary by release and source material | Use only selected release after license audit |
| WHAM! | urban noise | Published research benchmark; verify non-commercial restrictions | Research-only candidate until cleared |
| LibriMix | reproducible speech separation benchmark | Derived dataset; follow repository/data terms | Benchmark candidate, not product-training default |
| Consented Voca recordings | product acceptance and domain adaptation | First-party consent and usage agreement | Required before production claims |

## Required acquisition record

For every downloaded asset, record in a local manifest (not in Git if sensitive):

```json
{
  "dataset": "LibriSpeech",
  "release": "dev-clean",
  "source_url": "https://us.openslr.org/12/",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "license_review": "pending",
  "checksum": "sha256-or-md5",
  "downloaded_at": "YYYY-MM-DD",
  "allowed_use": "research|commercial|unknown",
  "notes": ""
}
```

## Data preparation contract

All prepared records must be 16 kHz, mono, PCM16 WAV or a documented lossless equivalent. The manifest must include:

```text
mixture, target, interferer, target_speaker_id,
interferer_speaker_id, source_dataset, split,
snr_db, overlap_ratio, rir_id, license_status
```

The split is assigned by target speaker and then checked against interferer IDs. A speaker appearing in evaluation must not appear in training. A fixed challenge set is kept immutable.

## 360 research notes

OpenSLR lists LibriSpeech as approximately 1,000 hours of 16 kHz read English speech and CC BY 4.0. The VoxCeleb official page describes more than 6,000 speakers and in-the-wild interview speech, but its access/privacy conditions must be treated separately from a simple download link. CSTR provides VCTK access information but the exact current terms must be captured at download time. Challenge rules demonstrate why source-specific restrictions matter: WHAM/LibriMix and challenge data can carry different usage constraints.

Sources:

- [OpenSLR LibriSpeech](https://us.openslr.org/12/)
- [VoxCeleb official dataset page](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/index.html)
- [CSTR downloads / VCTK](https://www.cstr.ed.ac.uk/downloads/)
- [LibriMix paper](https://arxiv.org/abs/2005.11262)
- [WHAM! paper](https://arxiv.org/abs/1907.01160)
- [CHiME challenge data rules](https://www.chimechallenge.org/challenges/chime7/task2/rules)

## Approval gate

This document is an acquisition plan, not a license clearance. Before product training, the project owner must approve each dataset's exact release, terms, intended use, and attribution requirements.
