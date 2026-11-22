# Data Availability and Suitability Assessment

## 1. Data Acquisition

The two BPI Challenge 2014 CSV datasets have been obtained
and are available as local copies before the start of the thesis.

The original datasets are not currently stored in this repository.

## 2. Accessibility

Both CSV files were successfully loaded using Python.
Permanent source references are provided in the README.

Link: https://pa.win.tue.nl/download_event_logs/

## 3. Data Quality Assessment

Preliminary findings:
- 46,809 imported incident rows
- 466,737 activity records
- 202 duplicate Incident ID detections, pending validation
- 203 rows with missing Priority and Category
- 44,826 valid calculated resolution durations
- Several small context groups

Further cleaning and validation will be performed
during the master's thesis.

## 4. Suitability for Research Questions

RQ1 – Context Definition:
Priority and Category enable different reference group
configurations, including global evaluation.

RQ2 – Training Sample Size:
Several groups contain sufficient records for
controlled subsampling experiments.

RQ3 – Reference Group Homogeneity:
Available temporal attributes enable the investigation
of behavioral variability within reference groups.

## 5. Evaluation Limitation

The dataset does not provide reliable labels for
temporal anomalies.

Controlled synthetic anomaly injection is planned.
The evaluation will focus on detecting injected
irregularities rather than claiming validated
real-world anomaly detection accuracy.

## 6. Status

Data acquisition: Completed
Initial feasibility assessment: Completed
Final data validation: Pending
Model development and experiments: Not yet started
