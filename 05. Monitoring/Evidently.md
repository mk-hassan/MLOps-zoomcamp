# Evidently

Pythong library used to evaluate, test, and monitor metrics related to ML/LLM models. 

## Main WF
1. Pass Input data 
2. choose the best metrics set depending on the preoblem type
  - 🔡 Text qualities	Length, sentiment, special symbols, pattern matches, etc.
  - 📝 LLM outputs	Semantic similarity, relevance, faithfulness, custom LLM judges, etc.
  - 🛢 Data quality	Missing values, duplicates, min-max ranges, correlations, etc.
  - 📊 Data drift	20+ tests and distance metrics to detect distribution drift.
  - 🎯 Classification	Accuracy, precision, recall, ROC AUC, confusion matrix, bias, etc.
  - 📈 Regression	MAE, ME, RMSE, error distribution, error normality, error bias, etc.
  - 🗂 Ranking (inc. RAG)	NDCG, MAP, MRR, Hit Rate, etc.
  - 🛒 Recommenders	Serendipity, novelty, diversity, popularity bias, etc.
3. View (jupyter), Export (json, HTML, pandas dataframe), or Upload the result to Evidently platform

## Concepts
1. Dataset \
Create Dateset object containing the defintion of your data, besides its meta data.

2. Reports and Metrics \
Report is the main object that you register the wanted metrics within its constructor then you `run` it and with your data and get the resulted metrics.

3. Presets \
Pre-defined group of metrics i.e. for classification problms use this group of metrics and so on.


> [!NOTE]
> To run evaluations, you must create a Dataset object with a DataDefinition, which maps:
> - Column types (e.g., categorical, numerical, text).
> - Column roles (e.g., id, prediction, target).




