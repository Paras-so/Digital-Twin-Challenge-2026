# Submission and runtime audit - 18 October 2026

## Conclusion

The technical PoC and required written/PDF documentation are prepared. The minimum 20-minute demonstration video is **pending by the team's instruction**. Submission-platform entry has not been performed. Do not describe the package as a completed final submission until those steps are done.

## Verification performed

| Check | Result |
|---|---|
| Full training pipeline | Completed again without exceptions |
| Reproduced headline model choices and MAE | Same selected models; MAE difference 0.0 mg/dL |
| Browser/Python inference agreement | All 4,416 predictions and event probabilities match within 1e-6 |
| Past-only inference | Future mutations leave features unchanged |
| Synthetic source integrity | 90 EHR rows and 207,360 ordered wearable events checked |
| Actual future labels | All 4,416 labels equal the +24-tick observed value |
| Event confusion counts | 211 correct alerts, 386 false alarms, 85 misses, 3,444 correct non-alerts reconciled |
| Artifact hashes | Verified against research/sha256.json |
| Syntax and compilation | JavaScript syntax and Python compilation checks passed |
| All four UI outcome examples | Correct result labels; revealing future does not change the issued forecast |
| Replay boundary | Day 8 21:55 forecast targets the last observation at 23:55; no out-of-bounds read |
| Sensor-gap control | Past available reading used; payload reports zero future inputs |
| Downloaded snapshot and report | Actual browser downloads parsed as valid JSON; no unrevealed outcome in snapshot |
| Browser console | No runtime errors observed in tested flows |
| Architecture and presentation PDFs | All 16 pages rendered and visually inspected |

## Corrections made

- Disable controls until model and patient JSON finish loading, preventing an early interaction from disagreeing with initialized state.
- Extend the replay to all eight days while preserving the full 120-minute target horizon.
- Plot the actual perturbed/available sensor stream when quality controls are used, rather than silently showing the original clean history.
- Clear the curated-example label when time, patient or quality changes.
- Expand automated browser/Python comparison from three demo patients to all 12 test patients.
- Add license, data provenance, submission checklist, project presentation, architecture diagram and recording guide.
- Add a submission validator that intentionally reports the missing video instead of returning a false readiness result.

## Remaining limitations

Synthetic precision is 35.3%; false alarms are substantial. This is a technical demonstration, not clinical validation. Event counts are correlated forecast windows, not independent episodes. Sensor stress and subgroup tables evaluate the regressor, not robustness of the separate event classifier. Empirical uncertainty coverage is not a formal independent-sample guarantee. Treatment personalization, real EHR/device integration and patient-specific calibration are not implemented.

## Outstanding submission actions

Record an explanation and demonstration lasting at least 20 minutes, add the accessible URL to README.md and submission.json, verify actual duration/access, and submit only the leader's name, phone, email and public GitHub URL on the platform. A guide or presentation is not a video. The leader contact file is kept outside the public repository.

This audit records checks actually performed; it is not a guarantee that every possible runtime, network or browser configuration is error-free. GitHub Actions status should be checked on the repository after publication.
