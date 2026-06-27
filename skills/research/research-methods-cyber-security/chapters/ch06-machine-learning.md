# Chapter 6: Machine Learning

## Core Idea
Machine learning is a research method — not just an engineering tool — that automates discovery of behavioral models from large cyber security datasets. This chapter frames ML as an observational research technique, introduces the key algorithm categories, and covers model validation to ensure findings are scientifically defensible.

## Frameworks Introduced

- **ML Learning Style Selection**: Three styles determined by data labeling:
  - **Supervised** — labeled data available; train on known outcomes; use when ground truth exists (e.g., known malware vs. benign samples)
  - **Unsupervised** — no labels; discovers structure; use for preliminary exploration, clustering unknown behaviors
  - **Semi-supervised** — partial labels; hybrid approach; use when only some data is labeled (common in cyber where labeling is expensive)
  - When to use: Pick style before picking algorithm — if you have labels, supervised; if you don't, unsupervised; if you have few labels, semi-supervised.

- **ML Problem Type Selection**: Four output types:
  - **Classification** — assign new data to learned categories (malware family ID, intrusion type)
  - **Clustering** — group similar items without predefined categories (behavioral grouping of threat actors)
  - **Regression** — predict continuous values (attack probability over time, traffic volume)
  - **Anomaly Detection** — model "normal," flag deviations (network baseline violation, lateral movement detection)
  - When to use: Match to your research question — "what category is this?" → Classification; "what groups exist?" → Clustering; "what will happen?" → Regression; "is this unusual?" → Anomaly Detection.

- **Cross-Validation Protocol**: Standard process to validate generalizability of a learned model:
  1. Split dataset: 60% training / 20% cross-validation / 20% test
  2. Train model on training set
  3. Tune parameters using cross-validation set
  4. Measure final generalizability on test set (never used for tuning)
  - When to use: Any time you develop a ML-based model for research (mandatory, not optional).
  - How: Never use the test set for tuning; the test set's role is to measure generalizability only.

- **Bayesian Networks (BNs) for Cyber Risk**: Probabilistic directed acyclic graphs that model dependencies between variables (e.g., vulnerability exposure, attacker capability, patch status) and enable inference about unobserved factors. Can be updated as new data arrives.
  - When to use: When you need to quantify and update cyber risk estimates dynamically; when expert judgment must be combined with observational data.
  - How: Define nodes (random variables), edges (conditional dependencies), prior probabilities from data or expert elicitation; run inference to estimate posterior probabilities given observed evidence.

- **Hidden Markov Models (HMMs)**: Sequence-based probabilistic models; widely used for behavior sequence modeling (network traffic patterns, multi-stage attack progressions, user behavior anomalies).
  - When to use: When the system under study moves through states over time and not all states are directly observable (e.g., attacker's hidden state during a multi-stage intrusion).

## Key Concepts
- **Machine Learning** — computational process to discover underlying behavioral models from empirical data; falls within observational research
- **Supervised Learning** — learns from labeled data; produces classifiers or regressors
- **Unsupervised Learning** — finds structure in unlabeled data; produces clusters or density models
- **Semi-supervised Learning** — hybrid; small labeled set guides learning over large unlabeled corpus
- **Classification** — assigns new inputs to predefined categories (HMMs, SVMs, Random Forests, Naïve Bayes, Neural Networks)
- **Clustering** — groups inputs by similarity without predefined categories (K-means, DBSCAN, Hierarchical)
- **Regression** — predicts continuous output values (Linear, Logistic, MARS)
- **Anomaly Detection** — models normality; flags statistical outliers (One-class SVM, FP-growth)
- **Overfitting (Variance)** — model fits training data but fails to generalize; fix by reducing features or regularization
- **Underfitting (Bias)** — model has high training error; fix by adding features or polynomial terms
- **Regularization** — technique to reduce magnitude of feature weights to combat overfitting
- **Cross-Validation** — systematic method to estimate model generalizability; uses three-way data split
- **Bayesian Network (BN)** — directed acyclic graph of random variables with probabilistic edges; enables probabilistic inference and dynamic updating
- **Hidden Markov Model (HMM)** — probabilistic sequence model; handles hidden states; widely used for cyber behavior modeling
- **Model Diagnostic** — test designed to identify why a model is failing and how to improve it

## Mental Models
- Think of ML learning style as "how much do I already know?": all labeled → supervised; none labeled → unsupervised; partially labeled → semi-supervised.
- Think of ML problem type as "what does my answer look like?": a category → classification; a group → clustering; a number → regression; a flag → anomaly detection.
- Overfitting is the "memorized the textbook, failed the novel question" problem — the fix is always less complexity or more data.
- A BN is a "probability flowchart" — it lets you propagate evidence through a system of uncertain dependencies.
- Always hold out your test set as a blind evaluator — touching it during development destroys its value as a generalizability measure.

## Anti-patterns
- **Using the test set for model tuning**: Invalidates the generalizability estimate; test set must remain blind until final evaluation.
- **Applying ML without sufficient data**: ML models require sufficient training data to avoid overfitting — sparse cyber datasets (rare attack events) frequently produce overfit models.
- **Treating ML output as ground truth**: ML models are probabilistic; false positive and false negative rates must be reported alongside accuracy.
- **Ignoring feature selection**: Heavily correlated features and irrelevant features degrade model performance; always analyze feature importance.
- **Confusing correlation with causation in ML outputs**: ML finds patterns; those patterns require scientific interpretation and validation (e.g., via hypothetico-deductive follow-up) before claiming causal relationships.

## Reference Tables

| Learning Style | When to Use | Example Algorithms |
|---|---|---|
| Supervised | Ground truth labels exist | Neural networks, SVM, Decision trees, Naïve Bayes |
| Unsupervised | No labels; explore structure | K-means, DBSCAN, PCA, hierarchical clustering |
| Semi-supervised | Few labels, large unlabeled corpus | EM, transductive SVM, Markov decision processes |

| Problem Type | Research Question Form | Example Algorithms |
|---|---|---|
| Classification | "What category is this?" | HMM, SVM, Random Forest, Naïve Bayes |
| Clustering | "What groups exist in this data?" | K-means, DBSCAN, hierarchical |
| Regression | "What value will this be?" | Linear regression, MARS, logistic regression |
| Anomaly Detection | "Is this unusual?" | One-class SVM, FP-growth, a priori |

| Problem | Symptom | Fix |
|---|---|---|
| Overfitting (high variance) | Low training error, high test error | Reduce features, add regularization, get more data |
| Underfitting (high bias) | High training error | Add features, add polynomial terms, tune parameters |

## Worked Example
**Anomaly Detection for Lateral Movement:**
A researcher wants to detect lateral movement in enterprise networks using only network flow data (unlabeled).

1. **Problem type**: Anomaly Detection (no labeled attack data available)
2. **Learning style**: Unsupervised (no ground truth labels)
3. **Algorithm**: One-class SVM trained on 30 days of normal intra-network flow (source IP, destination IP, port, bytes, duration)
4. **Model**: "Normal" user-to-server communication patterns
5. **Cross-validation**: 60/20/20 split of the 30-day dataset; tune SVM kernel and threshold on validation set
6. **Test**: Hold-out 20% evaluated; precision and recall reported against known-benign flows
7. **Research finding**: Model flags 0.3% of flows as anomalous; manual review of top-50 anomalies reveals 3 genuine lateral movement patterns and 2 backup jobs → generates hypothesis: "lateral movement produces statistically distinguishable flow signatures from backup traffic" → candidate for supervised classification follow-up once labeled dataset is built

## Key Takeaways
1. Select ML learning style first (supervised/unsupervised/semi-supervised) based on label availability, then select algorithm based on problem type (classification/clustering/regression/anomaly).
2. Always use a three-way split (60/20/20) for cross-validation; never touch the test set until final evaluation.
3. Overfitting is the dominant risk in cyber security ML due to small, imbalanced, or non-representative datasets — monitor training vs. validation error throughout.
4. Bayesian Networks are the right choice when you need dynamic, updatable risk models that combine data and expert judgment.
5. ML findings are pattern discoveries, not causal conclusions — follow up with hypothetico-deductive experiments (Ch 9) to establish causality.

## Connects To
- **Ch 4**: Exploratory Study — ML is classified within the observational research category; shares inductive framing
- **Ch 8**: Simulation — often combined with ML to generate synthetic training data for cyber scenarios
- **Ch 9**: Hypothetico-deductive — ML pattern findings become hypotheses for controlled experiments
- **Ch 13**: Instrumentation — data collection pipelines feed ML models
