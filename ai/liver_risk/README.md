

\# MediMind AI — Liver Health ML Prototype



\## 1. Objective



Develop an experimental machine-learning pipeline to investigate

classification of liver-disease status using the UCI Indian Liver

Patient Dataset (ILPD).



This is a research prototype, not a diagnostic tool.



\## 2. Dataset



\- Source: UCI Machine Learning Repository — ILPD

\- Original records: 583

\- Input features: 10

\- Target: Selector

\- Selector = 1: liver patient

\- Selector = 2: non-liver patient

\- Exact duplicate rows identified: 13

\- Records after exact deduplication: 570

\- Missing values: 4 in A/G Ratio


### Dataset attribution

The Indian Liver Patient Dataset (ILPD) is provided by the UCI Machine Learning Repository.

- **Dataset:** Indian Liver Patient Dataset (ILPD)
- **Source:** https://archive.ics.uci.edu/dataset/225/ilpd+indian+liver+patient+dataset
- **DOI:** https://doi.org/10.24432/C5D02C
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0), as identified for this dataset.
- **Modifications:** Exact duplicate rows were removed, missing values were handled in the model preprocessing pipeline, and the target was mapped to a binary classification label.

The dataset is used for academic experimentation. This project does not claim ownership of the original dataset.

\## 3. Exploratory Data Analysis



The EDA script generates:

\- Target and gender distributions

\- Numerical feature distributions

\- Boxplots for outlier investigation

\- A numerical correlation matrix

\- Feature-versus-target boxplots

\- Gender-versus-target analysis



Plots are stored in `eda\_plots/`.



\## 4. Preprocessing



\- Exact duplicate records are removed.

\- The dataset is split into training and test sets using stratification.

\- Test size: 20%.

\- Random state: 42.

\- Numerical missing values are imputed using the median.

\- Gender is imputed using the most frequent category.

\- Gender is one-hot encoded.

\- Numerical variables are standardized for Logistic Regression.

\- Preprocessing is fitted within a scikit-learn Pipeline to reduce

&#x20; data leakage.



\## 5. Models



\### Logistic Regression

Baseline linear classifier with balanced class weights.



\### Random Forest

Tree-based comparison model with 300 trees and balanced class weights.



\## 6. Evaluation



The training set is evaluated using 5-fold stratified cross-validation.

Final reported holdout metrics use a separate 20% test split.



Metrics:

\- Accuracy

\- Precision

\- Recall

\- F1-score

\- ROC-AUC

\- Confusion matrix



Cross-validation mean F1:

\- Logistic Regression: 0.6873

\- Random Forest: 0.7445



Holdout F1:

\- Logistic Regression: 0.7801

\- Random Forest: 0.7975



These results are preliminary and depend on the dataset and split.

The models have not been externally or clinically validated.



\## 7. Artifacts



\- `data/ilpd\_raw.csv`: downloaded dataset

\- `src/`: dataset inspection, EDA, training and evaluation scripts

\- `eda\_plots/`: EDA figures

\- `models/`: serialized model pipelines

\- `results/`: metrics and experiment metadata



\## 8. Limitations and Safety



\- The dataset is small and historical.

\- The target distribution is imbalanced.

\- Performance may vary across splits and populations.

\- No clinical validation has been performed.

\- The model must not be used to diagnose, rule out disease,

&#x20; recommend treatment, or replace a clinician.

\- Any future deployment requires appropriate validation, privacy

&#x20; controls, clinical oversight and monitoring.



\## 9. Reproduction



From the repository root:



```powershell

python ai\\liver\_risk\\src\\inspect\_dataset.py

python ai\\liver\_risk\\src\\eda.py

python ai\\liver\_risk\\src\\train\_model.py

python ai\\liver\_risk\\src\\evaluate\_models.py

```
