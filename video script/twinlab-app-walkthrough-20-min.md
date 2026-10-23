# Twinlab: 20-minute app walkthrough

Presenter: Jagjeet Singh. Team: jagjeet.work.16. College: National Institute of Technology Agartala. Teammate: Shivay Saurya.

App: [Open Twinlab](https://twinlab-glucose-poc.pluckyiris4.chatgpt.site/)

## Before recording - do not read aloud

- This script follows the working app throughout the recording. You do not need to display the PPT. Use this version instead of the earlier slide-based narration.

- Read only SAY aloud. SHOW, DO and PAUSE are presenter instructions. Keep this script on a second screen, phone or printed page so it does not cover the app in the recording.

- Each section has a one-minute window. Aim for about 125-135 spoken words per minute. Continue explaining while clicking or scrolling, and use the marked pauses to show evidence. The app actions and pauses belong inside each window.

- Load the app before recording. Keep replay paused, choose a rehearsed patient and set Sensor quality to Complete stream. Rehearse the measured examples, reveal button, quality selector, sensitivity sliders and downloads.

- The plan totals 20:00, including meaningful app interaction. Rehearse with a stopwatch and measure the exported video. Keep a few seconds of margin beyond 20:00. If it is substantially short, record again at a calmer pace with clear demonstrations rather than adding a long silent ending.

- Use the numbers actually visible in the selected example. A measured-example selection may change patient and time. Click Reveal actual outcome once: clicking it again advances two hours. Restore Complete stream after the quality tests.

## Recording route

| Time | App feature / explanation |
|---|---|
| 00:00-01:00 | Introduce Twinlab |
| 01:00-02:00 | The problem and the focused Digital Twin |
| 02:00-03:00 | Patient selection and historical health information |
| 03:00-04:00 | Wearable measurements and model insights |
| 04:00-05:00 | Show the two data streams joining |
| 05:00-06:00 | The sensor event log and synthetic dataset |
| 06:00-07:00 | How the trained model works behind the app |
| 07:00-08:00 | Understand the forecast and warning definition |
| 08:00-09:00 | Read the glucose trajectory and uncertainty band |
| 09:00-10:00 | Replay and continuous state updates |
| 10:00-11:00 | Correct warning: prediction before outcome |
| 11:00-12:00 | False alarms and missed events |
| 12:00-13:00 | Sensor gaps and noisy input |
| 13:00-14:00 | Explore model sensitivity |
| 14:00-15:00 | Export predictions and revealed outcomes |
| 15:00-16:00 | Compare forecasting methods and results |
| 16:00-17:00 | Explain classifier performance honestly |
| 17:00-18:00 | Explain how the evaluation avoids patient overlap |
| 18:00-19:00 | Show fusion, robustness and reproducible evidence |
| 19:00-20:00 | Close with the contribution and limitations |

## 00:00-01:00 - Introduce Twinlab

**SHOW:** Patient overview, at the top of the page

**DO - not spoken:** Load the app before recording. Select Ananya Sharma or a rehearsed patient. Set Sensor quality to Complete stream and keep replay paused. Start the recording and stopwatch together.

**SAY:**

Hello everyone. I am Jagjeet Singh from the National Institute of Technology Agartala. Along with my teammate Shivay Saurya, I am presenting Twinlab, our Digital Twin proof of concept for Type 2 Diabetes. Our team name is jagjeet.work.16.

During this demonstration, I will use the working application to explain its features, the data behind it, and how its machine-learning models produce predictions. I will also show correct warnings, false alarms and missed events.

Every patient and measurement in this demonstration is synthetic. The project demonstrates a reproducible prediction system and a clinician-facing workflow. Its results do not establish clinical effectiveness in real patients.

**PAUSE / TIMING - not spoken:** Pause 2 seconds after the introduction. Point to the synthetic-data notice, then pause 2 seconds before continuing.

## 01:00-02:00 - The problem and the focused Digital Twin

**SHOW:** Patient overview: patient bar and the four summary cards

**DO - not spoken:** Point to the selected patient, Current glucose, Glucose in 2 hours and Patient data combined. Keep these cards visible while speaking.

**SAY:**

The problem we address is the gap between a patient's historical record and their changing condition. An electronic health record provides useful context, but it cannot show every change happening throughout the day. Wearable measurements add repeated observations.

Twinlab combines these sources into an evolving virtual patient state. The selected person has a historical profile, a recent sensor history and a forecast that updates as we move through simulated time.

We chose a narrow task: forecasting glucose exactly two hours ahead and estimating the risk of a newly elevated reading at that time. This focused scope makes the prototype practical to build and evaluate. A doctor can inspect the evidence before considering what further assessment is appropriate.

**PAUSE / TIMING - not spoken:** Pause 2 seconds on the forecast card and 2 seconds on the two-stream card.

## 02:00-03:00 - Patient selection and historical health information

**SHOW:** Patient selector, then Patient baseline lower on Patient overview

**DO - not spoken:** Choose a second fictional patient and point to the changed profile. Scroll to Patient baseline. Return to your rehearsed patient before the next minute.

**SAY:**

The patient selector lets us inspect different fictional people. Changing the selection loads that person's profile and simulated timeline, then calculates predictions for their available state. The name and city are presentation labels, not real patient identities.

In Patient baseline, we can inspect HbA1c, body mass index, diagnosis history and a hypothetical genetic marker. Age also contributes to the model's historical features. These variables provide context that the changing glucose measurements alone do not contain.

The genetic marker is deliberately simulated and has no asserted real-world association. This panel represents the historical side of our data fusion. It remains relatively stable while the wearable measurements and prediction time change.

**PAUSE / TIMING - not spoken:** Pause 2 seconds after changing patient. Allow a further 3 seconds to point out the baseline fields.

## 03:00-04:00 - Wearable measurements and model insights

**SHOW:** Wearable signals, then Twin insights and What changes this forecast

**DO - not spoken:** Point to sleep, steps and HRV / heart rate. Scroll up to Twin insights and its three sensitivity entries. Do not move the scenario sliders yet.

**SAY:**

The Wearable signals panel shows previous-night sleep duration, steps during the last hour, heart-rate variability and heart rate. Glucose readings come from the simulated continuous glucose monitor, with a new observation every five minutes.

These values describe recent observations rather than a lifetime average. The model combines them with historical features and summaries of the recent glucose trajectory.

Twin insights explains the current forecast and shows selected input sensitivities. The entries compare the fitted model's output when one feature changes to a reference value. They help us inspect model behaviour. They do not prove that changing sleep, activity or any other variable would cause the displayed glucose change in a real person.

**PAUSE / TIMING - not spoken:** Pause 2 seconds on the wearable values and 2 seconds on the sensitivity explanation.

## 04:00-05:00 - Show the two data streams joining

**SHOW:** Data streams: Historical EHR and Wearable window

**DO - not spoken:** Click Data streams. Point to patient_id in both payloads, then observed_through and future_readings_used_for_prediction in the wearable payload.

**SAY:**

I will now open Data streams so we can inspect the inputs directly. The left payload is the synthetic electronic health record. The right payload summarizes the current wearable window.

Both contain the same patient identifier. That identifier is how the system associates historical context with the correct chronological observations. The inputs become one feature vector before the models run.

Notice the observation cutoff in the wearable payload. It marks the latest information available to the predictor. The future-readings field is zero because inference uses current and past measurements only. This separation is essential: a forecast would not be meaningful if the model could inspect the later value that it is supposed to predict.

**PAUSE / TIMING - not spoken:** Pause 3 seconds while showing the matching patient IDs. Pause 2 seconds on the zero future-readings field.

## 05:00-06:00 - The sensor event log and synthetic dataset

**SHOW:** Data streams: Sensor event log

**DO - not spoken:** Scroll to Sensor event log. Point to time, patient ID, glucose, source and quality. Explain that this table is a short recent view, not the entire dataset.

**SAY:**

Below the payloads is the sensor event log. Each visible row includes a timestamp, patient identifier, glucose reading, simulated source and quality status. This makes the changing input stream inspectable.

The complete generated dataset contains ninety patient profiles and eight days of five-minute observations per person. That produces two hundred and seven thousand, three hundred and sixty wearable records. The table on this screen shows a recent excerpt, while the full files are in the repository.

The generator combines varying meals, daily rhythms, patient characteristics, sleep, activity and noise. Later readings on these timelines provide the prediction labels. The simulation supports engineering experiments, but it has not been validated as a physiological representation of Indian patients.

**PAUSE / TIMING - not spoken:** Pause 3 seconds while tracing a row across the event log. Pause 2 seconds before changing view.

## 06:00-07:00 - How the trained model works behind the app

**SHOW:** Patient overview: forecast cards and the current patient state

**DO - not spoken:** Return to Patient overview. Keep the forecast cards visible while explaining the pipeline. No terminal or training run is needed during the video.

**SAY:**

Behind this interface, feature extraction converts the two streams into eighteen numerical inputs. They include historical context, current glucose, earlier readings, recent averages and variability, a thirty-minute slope, wearable signals and time of day.

Python, NumPy and scikit-learn handle offline generation, training and evaluation. The selected models are a random forest regressor for the future glucose value and a separate random forest classifier for the event warning.

We export the fitted model parameters to JSON. JavaScript loads those parameters and evaluates the trees in the browser. Opening the page does not train a new model. The displayed predictions come from the fitted artifacts, and verification scripts compare browser inference with the corresponding Python outputs.

**PAUSE / TIMING - not spoken:** Pause 2 seconds after explaining the two models. Pause 2 seconds while pointing to their two different outputs.

## 07:00-08:00 - Understand the forecast and warning definition

**SHOW:** Current glucose, Glucose in 2 hours, New adverse event and Twin insights

**DO - not spoken:** Point to the current value, future forecast and warning. Read the selected time in Twin insights without inventing a fixed example value.

**SAY:**

The current-glucose card describes the value available at the forecast origin. The next card predicts glucose exactly one hundred and twenty minutes later. The event card is driven by a separate classifier.

For our experiment, a new event means glucose is at or below one hundred and eighty milligrams per decilitre now, and above that threshold exactly two hours later. A reading already elevated now is excluded from new-event scoring.

The warning can trigger even when the point forecast is below the threshold, because risk and a single numerical estimate are different outputs. This target does not detect every brief crossing inside the two-hour interval. It checks the specified endpoint, using a demonstration threshold rather than a treatment recommendation.

**PAUSE / TIMING - not spoken:** Pause 2 seconds between the current and future cards. Pause 2 seconds after distinguishing risk from the point forecast.

## 08:00-09:00 - Read the glucose trajectory and uncertainty band

**SHOW:** Glucose trajectory and its legend, before outcome reveal

**DO - not spoken:** Point to Observed history, Forecast interpolation and Residual band. Trace the forecast-issued boundary and +2 hours endpoint with the pointer.

**SAY:**

The trajectory chart places the forecast in context. The historical line shows available glucose observations. The forecast-issued boundary separates that history from the later period being predicted.

The connecting forecast line leads to the predicted two-hour endpoint. It is interpolation for visualization, not a separately trained forecast for every future minute. Keeping that distinction clear prevents us from overstating what the model produces.

The shaded residual band represents an empirical uncertainty range derived from separate calibration patients. It covered about eighty-nine point seven percent of final synthetic test outcomes. That coverage is a measured result, not a guarantee for every patient. We will reveal the actual future after first inspecting the prediction.

**PAUSE / TIMING - not spoken:** Pause 3 seconds while tracing the chart. Pause 2 seconds on the shaded band.

## 09:00-10:00 - Replay and continuous state updates

**SHOW:** Glucose trajectory, Play replay, Forecast time and Next 5 minutes

**DO - not spoken:** Click Play replay. Let it run for about 8 seconds while narrating, then click Pause replay. Scroll to the time control and click Next 5 minutes once. Move the time slider a short distance, then stop.

**SAY:**

I will start replay so we can see the virtual patient update. Replay advances through a prerecorded synthetic timeline. It demonstrates the update workflow without claiming a live connection to a physical wearable.

As observations arrive, feature extraction refreshes the patient state and the fitted models produce new outputs. The chart and observation time move with that state.

I can pause for inspection, advance by exactly five minutes, or choose another forecast time. Moving time clears the revealed outcome so that the next prediction starts with its future hidden. The numerical forecast may occasionally stay similar, even though the observation time and model inputs have changed.

**PAUSE / TIMING - not spoken:** Keep the 8-second replay inside this minute and continue narrating during it. Pause 2 seconds after the manual time update. Leave replay paused.

## 10:00-11:00 - Correct warning: prediction before outcome

**SHOW:** Jump to a measured example: Correctly predicted spike

**DO - not spoken:** Choose Correctly predicted spike. The selector may change the patient and time. Point to the issued forecast and warning before clicking Reveal actual outcome. Click reveal once, then point to the verdict, actual value and error.

**SAY:**

I am choosing a correctly predicted spike from the measured examples. This selector finds an illustrative test case; it may move us to a different patient and forecast time.

First, notice the issued prediction and event warning while the actual future is hidden. I will now reveal the later observation. The outcome panel compares the saved forecast with the glucose value exactly two hours later and reports the absolute error.

The warning is correct for the defined endpoint event in this example. Revealing the future does not change the issued prediction. A successful selected example demonstrates the interaction, while performance claims must come from the full test set, which we will inspect shortly.

**PAUSE / TIMING - not spoken:** Pause 3 seconds before reveal so viewers can read the issued outputs. Pause 3 seconds after reveal to inspect the verdict and numbers.

## 11:00-12:00 - False alarms and missed events

**SHOW:** Measured examples: False alarm, then Missed spike

**DO - not spoken:** Choose False alarm and reveal its outcome. After explaining it, choose Missed spike and reveal that outcome. Use the exact displayed verdicts. Do not click the reveal button twice on the same example.

**SAY:**

A complete demonstration should also expose mistakes. In this false-alarm example, the classifier warns, but the later observation does not meet our event definition. A clinician would receive a warning that does not correspond to the defined event.

Now I will select a missed spike. Here, the actual two-hour endpoint meets the event definition, but the classifier does not raise an alert. This is a different failure, and improving one kind of error can worsen the other.

These cases explain why we report both recall and precision. The example selector uses known outcomes to locate demonstrations. The aggregate evaluation includes all eligible test windows, rather than only the cases we choose to show.

**PAUSE / TIMING - not spoken:** Pause 3 seconds on the false-alarm verdict and 3 seconds on the missed-event verdict. Allow the remaining interaction time for the two selections and reveals.

## 12:00-13:00 - Sensor gaps and noisy input

**SHOW:** Sensor quality, forecast cards and Data streams event log

**DO - not spoken:** Choose Complete stream, then 30-minute CGM gap. Point to the forecast and inspect the missing readings in Data streams. Return to Patient overview, try Noisy CGM illustration, then restore Complete stream.

**SAY:**

Wearable inputs can be incomplete, so the prototype includes sensor-quality demonstrations. I will first select a thirty-minute CGM gap. The input preparation removes recent glucose observations and uses available past values when constructing features.

In Data streams, the event log identifies the missing readings. The underlying later outcome remains unchanged, so the demonstration perturbs past input rather than rewriting the future label.

The noisy-CGM option applies a repeatable disturbance to recent glucose history. It illustrates how the fitted predictor responds to altered measurements. It is different from the statistical noise experiment in the benchmark report. Neither control guarantees reliability with a real device. I will restore the complete stream before continuing.

**PAUSE / TIMING - not spoken:** Pause 2 seconds on the missing-reading labels and 2 seconds after restoring Complete stream. Continue speaking during view changes.

## 13:00-14:00 - Explore model sensitivity

**SHOW:** Patient overview: Explore model sensitivity

**DO - not spoken:** Scroll to Explore model sensitivity. Adjust Sleep duration, observe Scenario forecast, then adjust Steps in last hour. Point to the scenario value and difference. Do not present these sliders as treatment controls.

**SAY:**

This panel lets us explore the model's response to alternative feature values. I can change sleep duration or steps during the last hour and inspect the scenario forecast.

The app copies the current feature vector, substitutes these selected values and evaluates the same fitted regressor. It shows the resulting glucose estimate and its difference from the current forecast. Some small slider movements may leave the result unchanged because decision trees use thresholds.

The comparison is a sensitivity illustration. It does not predict the causal effect of sleeping longer or taking more steps, and it does not recommend a treatment. The main forecast and saved outcome experiment remain separate from this scenario display. That distinction matters when explaining this feature to a doctor.

**PAUSE / TIMING - not spoken:** Pause 3 seconds after each slider adjustment so viewers can compare the scenario output.

## 14:00-15:00 - Export predictions and revealed outcomes

**SHOW:** Export snapshot and Download revealed forecasts

**DO - not spoken:** Choose Correctly predicted spike and reveal once so the current snapshot has an actual outcome. Click Export snapshot. Click Download revealed forecasts. Show the download confirmation; opening the files is optional and not required for this minute.

**SAY:**

The prototype also exports evidence for inspection. I will reveal a measured example, then export its current snapshot. The JSON includes the synthetic profile, feature names and values, numerical forecast, interval, event-risk information and the actual value if it has been revealed.

The revealed-forecasts download produces a CSV containing the cases we have inspected in this browser session. It is a demonstration ledger, not the complete held-out evaluation dataset.

Keeping the issued prediction and later observation together makes individual outcomes easier to review. These downloads support transparency and debugging. They are not an authenticated medical record system, and this prototype does not claim hospital integration or permanent server-side storage of these interactions.

**PAUSE / TIMING - not spoken:** Pause 2 seconds after each download confirmation. Keep the app visible while downloads complete.

## 15:00-16:00 - Compare forecasting methods and results

**SHOW:** Model & benchmarks: summary cards and Five forecasting methods, tested on the same patients

**DO - not spoken:** Click Model & benchmarks. Point to Average forecast error, then the random forest row and baseline rows in the forecasting table. Use the Avg error and RMSE columns for this explanation.

**SAY:**

The Model and benchmarks view shows the evaluation evidence behind the demonstration. For glucose forecasting, we compare persistence, linear trend, ridge regression, random forest and gradient boosting.

Persistence predicts the latest reading, while linear trend extends the recent slope. The selected random forest has a test mean absolute error of ten point zero four milligrams per decilitre and a root mean squared error of fourteen point zero three.

Persistence has an average error of about twenty-five point six, while gradient boosting reaches about ten point three. Random forest also won the validation comparison. These results are specific to our synthetic timelines. The event columns in this forecasting table use a fixed point-forecast threshold, which is separate from the dashboard's dedicated warning classifier.

**PAUSE / TIMING - not spoken:** Pause 3 seconds on the deployed row and 2 seconds while comparing it with the baselines.

## 16:00-17:00 - Explain classifier performance honestly

**SHOW:** Dedicated two-hour spike-risk classifiers, then Every alert has an outcome

**DO - not spoken:** Scroll to the dedicated classifier table. Point to the deployed random forest row. Then scroll to the confusion counts, keeping them visible for the final paragraph.

**SAY:**

The separate classifier table evaluates the warnings that drive Patient overview. The selected random forest catches seventy-one point three percent of defined new events. Its precision is thirty-five point three percent, so roughly thirty-five of every hundred alerts are correct in this synthetic test.

The confusion counts make the trade-off concrete: two hundred and eleven correct alerts, three hundred and eighty-six false alarms, eighty-five missed events and three thousand, four hundred and forty-four correct non-alerts.

The model and raw cutoff were selected using validation F-two, which gives recall more weight than precision. Separate calibration maps the score to the displayed risk scale. The substantial false-alarm count remains a limitation and should be visible alongside any successful demonstration.

**PAUSE / TIMING - not spoken:** Pause 3 seconds on recall and precision, then 3 seconds on the false-alarm and missed-event counts.

## 17:00-18:00 - Explain how the evaluation avoids patient overlap

**SHOW:** Model & benchmarks: How the evaluation is protected

**DO - not spoken:** Find How the evaluation is protected. Point to Patient separation and Rolling evaluation, then the grouped and chronological checks. Keep the explanatory text readable.

**SAY:**

Evaluation separates people into four groups. Fifty-four patients train the models, twelve support validation and selection, twelve support calibration, and twelve form the final test cohort. No patient appears in two groups.

The final evaluation issues forecasts every thirty minutes and compares each with the actual observation one hundred and twenty minutes later. This produces four thousand, four hundred and sixteen forecasts on the held-out patients.

Patient separation reduces the risk of learning the same person's timeline in training and testing. We also run grouped cross-validation and a separate chronological experiment. Adjacent forecasting windows still overlap, so these observations are correlated. Our patient-bootstrap analysis resamples people rather than pretending that every forecast row is independent.

**PAUSE / TIMING - not spoken:** Pause 3 seconds on the four cohorts and 2 seconds on the rolling-evaluation description.

## 18:00-19:00 - Show fusion, robustness and reproducible evidence

**SHOW:** Does combining both streams help?, imperfect sensors, subgroup table and Download benchmark report

**DO - not spoken:** Scroll to the fusion table, then the sensor stress results. Briefly point out Performance across patient groups. Return to the forecasting table and click Download benchmark report.

**SAY:**

The fusion comparison retrains the regressor with different input sources. Both streams give an average error of ten point zero four, EHR alone gives nineteen point two five, and wearables alone gives ten point two five.

The improvement over wearables alone is modest. That is an important finding: recent glucose history supplies much of the predictive information in this simulation. The sensor-stress and subgroup sections provide additional regression diagnostics, not clinical reliability or fairness guarantees.

I can download the benchmark report to inspect the results outside the interface. The repository also contains training code, model artifacts and verification scripts that check data integrity, future-label alignment and agreement between Python and browser predictions.

**PAUSE / TIMING - not spoken:** Pause 3 seconds on the three fusion rows and 2 seconds after downloading the report.

## 19:00-20:00 - Close with the contribution and limitations

**SHOW:** Patient overview: forecast cards and research-prototype notice

**DO - not spoken:** Return to Patient overview and scroll to the top. Keep replay paused. End on the selected virtual patient and synthetic-data notice, rather than a blank screen.

**SAY:**

To conclude, Twinlab demonstrates the complete proof-of-concept workflow: historical and wearable data join into a changing patient state, trained models forecast a defined two-hour outcome, and a clinician-facing interface exposes predictions, later observations and benchmark evidence.

The project also makes its limitations visible. All data is synthetic, warnings include false alarms and misses, and the sensitivity controls do not simulate treatment effects. We have not established clinical benefit or deployed a real patient-monitoring service.

The next research step would require appropriately permitted longitudinal data and clinical evaluation. Our public repository provides the implementation and documentation under an MIT license for original project materials. Thank you for watching our Twinlab demonstration.

**PAUSE / TIMING - not spoken:** Pause 2 seconds before the final thank-you and 3 seconds afterwards. Check the stopwatch and end only after 20:00. Keep a few extra seconds as a recording margin.

## After recording - do not read aloud

Check audio and screen readability. Verify actual duration is at least 20 minutes. Upload an accessible video, then add its URL to the repository README and submission metadata.
