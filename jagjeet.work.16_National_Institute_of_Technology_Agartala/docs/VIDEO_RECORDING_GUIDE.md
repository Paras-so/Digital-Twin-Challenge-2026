# Minimum 20-minute video - recording guide

**PENDING. This guide is not a recording.** Target 22 minutes to allow for edits. Use project-presentation.pdf with narrated screen recording and show the working dashboard. Upload an accessible recording, add its link to README.md and submission.json, measure its actual duration (at least 20:00), and test viewing without requesting access.

| Time | Explanation and demonstration |
|---|---|
| 00:00-01:00 | Introduce jagjeet.work.16, NIT Agartala, Jagjeet Singh and Shivay Saurya. State the title and synthetic-data scope. |
| 01:00-03:00 | Explain the healthcare use case, why both streams matter, and the limited patient-state twin. Avoid whole-body or clinical-efficacy claims. |
| 03:00-04:00 | Define the event: <=180 now and >180 mg/dL exactly 120 minutes later. Distinguish this from any spike inside an interval. |
| 04:00-06:00 | Show CSV schemas, patient ID join and changing sensor values. Explain previous-night sleep and the hypothetical marker. |
| 06:00-08:00 | Trace the architecture PDF: streams, past-only features, fitted models, calibration, dashboard and future-outcome reveal. |
| 08:00-10:00 | Show train.py, the 18 features, five forecasters and two classifier candidates. Explain offline training and JSON inference. |
| 10:00-12:00 | Explain disjoint patient cohorts, future observations as labels and grouped/chronological tests. |
| 12:00-14:00 | Explain 10.04 mg/dL MAE, 71.3% recall and 35.3% precision. Discuss false alarms and misses openly. |
| 14:00-16:00 | Live demo: select patients/time, play and pause, inspect sources, then choose the correctly predicted spike. Note the issued forecast before revealing. |
| 16:00-18:00 | Reveal the actual outcome. Show false-alarm and missed-spike examples, explain risk versus point forecast, and export the ledger. |
| 18:00-19:30 | Test gaps/noise. Show benchmark tables, empirical uncertainty and sensitivity controls. They do not simulate treatment effects. |
| 19:30-21:00 | Run node check-model.cjs and python verify-data.py. Show 4,416 comparisons and actual-outcome checks passing. |
| 21:00-22:00 | Summarize limitations, future research, MIT license, repository structure and documentation. |

Rehearse and measure the actual final recording. The timed plan does not prove video duration. Do not pad the recording with silence or claim this guide satisfies the video requirement.
