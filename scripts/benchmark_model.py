"""Application main."""
from datetime import datetime

import xgboost
from sklearn.metrics import log_loss, roc_auc_score

from patient_no_show.data_adapter import load_patients_appointment_data
from patient_no_show.prepare import engineer_features
from patient_no_show.train import train_no_show_model

# DATA LOADING
# first appointment day: 2016-04-29 00:00:00+00:00
# last appointment day: 2016-06-08 00:00:00+00:00
patient_appointments = load_patients_appointment_data()

train_start = datetime.fromisoformat("2016-04-29T00:00:00+00:00")
validation_start = datetime.fromisoformat("2016-05-28T00:00:00+00:00")
test_end = datetime.fromisoformat("2016-06-08T00:00:00+00:00")

# FEATURE ENGINEERING
patient_appointments_features = engineer_features(patient_appointments=patient_appointments)

# MODEL TRAINING
model, patient_appointments_predictions = train_no_show_model(
    patient_appointments=patient_appointments_features,
    validation_start=validation_start,
)

# EVALUATION
xgboost.plot_importance(booster=model, importance_type="gain", show_values=False)

# metrics
y_true = patient_appointments_predictions.no_show
y_pred = patient_appointments_predictions.no_show_probability_prediction
model_log_loss = round(number=log_loss(y_true=y_true, y_pred=y_pred), ndigits=4)
model_auc = round(roc_auc_score(y_true=y_true, y_score=y_pred), ndigits=4)

print(f"Model performance: log_loss={model_log_loss}, AUC={model_auc}")
# without feature engineering Model performance: log_loss=0.4671, AUC=0.6339
# with feature engineering Model performance: log_loss=0.4269, AUC=0.7236
