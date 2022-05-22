"""Application main."""
from datetime import datetime

import xgboost

from project.data_adapter import load_patients_appointment_data
from project.train import train_no_show_model

if __name__ == "__main__":
    # first appointment day: 2016-04-29 00:00:00+00:00
    # last appointment day: 2016-06-08 00:00:00+00:00
    patient_appointments = load_patients_appointment_data()

    train_start = datetime.fromisoformat("2016-04-29T00:00:00+00:00")
    validation_start = datetime.fromisoformat("2016-05-28T00:00:00+00:00")
    test_end = datetime.fromisoformat("2016-06-08T00:00:00+00:00")

    model, patient_appointments_predictions = train_no_show_model(
        patient_appointments=patient_appointments,
        validation_start=validation_start,
    )
    xgboost.plot_importance(booster=model, importance_type="gain", show_values=False)
