"""Train patient's appointment no show model."""
import multiprocessing
from datetime import datetime

from pandera.decorators import check_types
from pandera.typing import DataFrame
from xgboost import XGBClassifier

from project.schema import (
    PatientsAppointmentFeaturesLabel,
    PatientsAppointmentFeaturesLabelPrediction,
)


@check_types
def train_no_show_model(
    *,
    patient_appointments: DataFrame[PatientsAppointmentFeaturesLabel],
    validation_start: datetime,
) -> tuple[XGBClassifier, DataFrame[PatientsAppointmentFeaturesLabelPrediction]]:
    """Train no_show model on provided data and time slice.

    Model is trained in a two step approach:
    1. Train early stopping on data before validation_start. Predict on validation data and return.
    2. Retrain with early stopping results (n_estimators) and return model.

    Args:
        patient_appointments (DataFrame[PatientsAppointmentFeaturesLabel]): features with label
        validation_start (datetime): timestamp for splitting into train and validation data

    Returns:
        tuple[XGBClassifier, DataFrame[PatientsAppointmentFeaturesLabelPrediction]]: model and
            artificial model prediction with early stopping model on all data.
    """
    # train/validation split
    train_data = patient_appointments.query(f"appointment_day <= '{validation_start}'")
    validation_data = patient_appointments.query(f"'{validation_start}' < appointment_day")

    # feature definition
    PATIENT_NO_SHOW_MODEL_FEATURES = [
        "gender",
        "age",
        "neighborhood",
        "scholarship",
        "hipertension",
        "diabetes",
        "alcoholism",
        "handcap",
        "sms_received",
        "days_between_scheduling_and_appointment",
        "appointment_scheduling_dayofweek",
        "appointment_scheduling_hour",
    ]

    # first model training with early stopping on training set only
    model = XGBClassifier(
        **{
            "booster": "gbtree",
            "objective": "binary:logistic",
            "tree_method": "approx",
            "enable_categorical": True,
            "n_estimators": 5000,
            "colsample_bytree": 0.9,
            "learning_rate": 0.2,
            "max_depth": 6,
            "min_child_weight": 5,
            "eval_metric": "logloss",
            "early_stopping_rounds": 100,
            "n_jobs": int(multiprocessing.cpu_count() / 2),
        }
    )

    eval_set = [
        (
            train_data.filter(items=PATIENT_NO_SHOW_MODEL_FEATURES),
            train_data.no_show,
        ),
        (
            validation_data.filter(items=PATIENT_NO_SHOW_MODEL_FEATURES),
            validation_data.no_show,
        ),
    ]

    model.fit(
        X=train_data.filter(items=PATIENT_NO_SHOW_MODEL_FEATURES),
        y=train_data.no_show,
        eval_set=eval_set,
        verbose=10,
    )

    # artificial model prediction on validation data
    validation_data_prediction = validation_data.assign(
        no_show_probability_prediction=lambda df: model.predict_proba(
            X=df.filter(items=PATIENT_NO_SHOW_MODEL_FEATURES)
        )[:, 0],
        no_show_class_prediction=lambda df: df.no_show_probability_prediction > 0.5,
    )

    # retrain model on all data
    # OPTIONAL: cleaner distinction between phase 1 and phase 2 models
    model.n_estimators = round(model.best_ntree_limit * 1.2)  # train 20% longer, due to more data
    model.early_stopping_rounds = None  # remove early stopping
    model.fit(
        X=patient_appointments.filter(items=PATIENT_NO_SHOW_MODEL_FEATURES),
        y=patient_appointments.no_show,
    )
    return model, validation_data_prediction
