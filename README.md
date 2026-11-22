# Master Thesis – IT Incident Management Anomaly Detection

## Research Topic

Evaluating the Impact of Context Definition and Reference Group Size on Unsupervised Temporal Anomaly Detection in IT Incident Management Event Logs.

## Data Sources

**Incident Details**
- File: `Detail_Incident.csv`
- DOI: https://doi.org/10.4121/uuid:3cfa2260-f5c5-44be-afe1-b70d35288d6d

**Incident Activity Log**
- File: `Detail_Incident_Activity.csv`
- DOI: https://doi.org/10.4121/uuid:86977bac-f874-49cf-8337-80f26bf5d2ef

## Data Availability

Both datasets have been obtained and are stored locally. The CSV files were successfully loaded and examined using Python.

## Preliminary Data Assessment

- 46,809 imported incident rows
- 466,737 imported activity rows
- Common identifier: Incident ID
- Available context attributes: Priority and Category
- 44,826 valid calculated resolution durations
- 11 Priority + Category groups
- 6 combined groups contain at least 500 records before final data cleaning and splitting

## Suitability for Research

The dataset supports the planned investigation of:
- Case-level behavioral features
- Domain-specific reference groups
- Global versus context-aware anomaly detection
- Different training sample sizes within fixed reference groups

## Known Limitations

- Missing or duplicate incident identifiers require verification.
- Some resolution durations are invalid or unavailable.
- Certain reference groups contain very few cases.
- Reliable ground-truth anomaly labels are unavailable.
- Synthetic anomalies will be used for controlled evaluation, with limited conclusions about real-world detection accuracy.

## Current Status

Data acquisition: Completed.

Preliminary data assessment: Completed.

Detailed preprocessing and experimental implementation: Planned for the master's thesis.

## Data Access

Original CSV files are stored locally and are not included in this repository. Redistribution permissions and fresh public download availability have not yet been verified.
