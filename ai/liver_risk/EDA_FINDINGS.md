

\# MediMind AI — Initial EDA Findings



\## Dataset overview



The original dataset contains 583 records and 10 predictive features.

The target column is `Selector`.



\## Data quality



\- Four missing values were found in `A/G Ratio`.

\- Thirteen exact duplicate rows were identified.

\- After exact deduplication, 570 records remained.

\- Missing numerical values are handled within the model pipeline.



\## Class distribution



Original dataset:

\- Selector 1: 416 records (71.36%)

\- Selector 2: 167 records (28.64%)



After deduplication:

\- Liver-patient-labelled records: 406

\- Non-liver-patient-labelled records: 164



The imbalance makes accuracy alone insufficient for evaluation.



\## Feature observations



The initial statistical summary showed wide ranges in bilirubin,

alkaline phosphatase and enzyme measurements.



These observations motivated distribution plots and boxplots.

Extreme values were not automatically removed because they may

represent meaningful clinical measurements.



\## Evaluation approach



Two models were compared:

1\. Logistic Regression

2\. Random Forest



Evaluation includes stratified cross-validation, a stratified holdout

split, precision, recall, F1-score, ROC-AUC and confusion matrices.



\## Limitations



The EDA describes this dataset only. It does not establish that

features cause disease or that the models generalize to other

populations. Results are experimental and are not clinically validated.
