# Twinlab v2 — working Digital Twin PoC

**Condition:** Type 2 Diabetes. **Prediction:** glucose and new elevated-glucose risk exactly 120 minutes ahead. A new event is current glucose <=180 mg/dL and future glucose >180 mg/dL. This does not claim to detect every crossing during the interval.

## Run the dashboard

Serve `dist/`, for example: `python -m http.server 4173 --directory dist`. Open http://localhost:4173. The browser loads fitted model artifacts; it does not retrain. There are no frontend build dependencies.

Choose a virtual patient and forecast time. Click **Reveal actual outcome** to compare a saved forecast with the actual observation two hours later. Advance, replay, change sensor quality, inspect input streams, compare model benchmarks, and export snapshots/revealed forecasts. Future data is present for replay but never passed into the inference feature extractor.

## Requirements addressed

1. Static stream: simulated demographics, prior diagnosis duration, HbA1c, BMI and a hypothetical genetic risk marker.
2. Dynamic stream: chronological 5-minute CGM glucose, sleep, step counts, heart rate and HRV. Values update with replay.
3. Fusion: patient IDs join baseline records with past-only sensor windows, producing 18 features.
4. ML: Python trains ridge, random forest and gradient boosting regressors, and logistic/random forest event classifiers. Browser inference uses the exported fitted trees/coefficients.
5. Adverse-event forecast: separate classifier flags elevated endpoint risk 120 minutes ahead. Alert cutoff prioritizes recall (validation F2), with precision and false alarms exposed.
6. Outcome proof: replay actual future observations and export the prediction/result pair.
7. Clinician UI: patient history, wearable signals, forecasts, risk alerts, uncertainty, sensitivity explanations and evaluation.

## Reproduce training and benchmarking

Python 3.13.6, NumPy 2.3.2 and scikit-learn 1.9.0 were used. Install NumPy and scikit-learn in your chosen environment, then run `python train.py`. To reproduce the delivered environment exactly use `pip install -r requirements.txt`.

Generator seed: **20261018**, frozen for this final experiment after a pilot with seed 20261017. The pilot identified poor event recall from regression-only alerts; the final design added a dedicated event classifier before generating the final cohort. No final test scores are used for model or cutoff selection.

90 synthetic patients have eight complete days of sensor observations each. The generator combines varied meals, nonlinear post-meal responses, circadian rhythms, patient differences, activity, sleep and correlated noise. Future meal timing/size and future readings are not input features. The simulated profiles are labeled with Indian cities; the generator is not an epidemiological model of India.

**Split by patient:** 54 train / 12 validation / 12 calibration / 12 test. Regression selection uses validation MAE. Classifier and raw alert cutoff selection use validation F2, favouring recall. Calibration uses separate patients for the residual interval and probability mapping. Final test contains 4,416 rolling forecasts spaced 30 minutes apart. All labels come from readings exactly 24 five-minute ticks later. Event scoring excludes origins already above 180.

Benchmarks include persistence, linear trend, ridge, random forest and gradient boosting; logistic and random forest event classifiers; three-fold grouped cross-validation; an embargoed chronological holdout; EHR-only/wearable-only regression ablations; 30-minute CGM gaps with past-only carry-forward; Gaussian sensor noise; age/sex regression subgroups; 500 patient-bootstrap MAE resamples; and test interval coverage. Regression benchmark event columns use the fixed point-forecast threshold of 180; the dedicated classifier drives dashboard alerts and is scored separately.

The gap/noise and subgroup tables evaluate the selected **regressor**; they are not classifier robustness results. The live noisy-sensor control uses a deterministic sine perturbation for illustration, whereas the benchmark uses Gaussian noise. The residual interval is empirically calibrated, but overlapping windows violate independent-sample assumptions, so formal coverage is not asserted. The line between current and forecast glucose is interpolation, not a multi-step trajectory model. Sensitivity controls and reference-value explanations are not causal intervention models.

## Artifacts

- `dist/trained-model.json`: fitted regression + event classifier + calibration parameters.
- `dist/benchmark.json`: complete measured benchmark report and experiment metadata.
- `dist/patients.json`: three test-cohort timelines for the clinician replay.
- `research/ehr.csv`, `research/wearables.csv`: separate complete synthetic input streams.
- `research/heldout-predictions.csv`: every final test prediction, actual outcome and event risk.
- `research/sha256.json`: artifact integrity hashes.
- `train.py`: full generator, training, model selection, calibration, evaluation and export pipeline.
- `check-model.cjs`: regression/classifier parity between Python and JavaScript, future isolation, outcome integrity and reconciled test metrics. Run `node check-model.cjs`.

The browser is a research demonstration, not clinical software. All people and data are fictional. The genetic marker is hypothetical and makes no real genotype association claim. Synthetic performance is not clinical accuracy. Real-data and prospective clinical validation remain outside this PoC.

Method references: https://scikit-learn.org/stable/modules/cross_validation.html and https://scikit-learn.org/stable/modules/calibration.html
