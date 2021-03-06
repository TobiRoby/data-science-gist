"""Data adapters."""
from pathlib import Path

import pandas as pd
from pandera.decorators import check_types
from pandera.typing.pandas import DataFrame

from patient_no_show.schema import PatientsAppointment


@check_types
def load_patients_appointment_data() -> DataFrame[PatientsAppointment]:
    """Load and return appointments data.

    Returns:
        DataFrame[PatientsAppointment]: patients appointment data
    """
    # link: https://www.kaggle.com/datasets/joniarroba/noshowappointments
    file_path = Path("artifacts/KaggleV2-May-2016.csv")
    appointments = pd.read_csv(file_path)

    # more pythonic column names
    appointments_renamed = appointments.rename(
        columns={
            "PatientId": "patient_id",
            "AppointmentID": "appointment_id",
            "Gender": "gender",
            "ScheduledDay": "appointment_scheduled_datetime",
            "AppointmentDay": "appointment_day",
            "Age": "age",
            "Neighbourhood": "neighborhood",
            "Scholarship": "scholarship",
            "Hipertension": "hipertension",
            "Diabetes": "diabetes",
            "Alcoholism": "alcoholism",
            "Handcap": "handcap",
            "SMS_received": "sms_received",
            "No-show": "no_show",
        }
    )

    # fix data types
    appointments_types = appointments_renamed.assign(
        patient_id=lambda df: df.patient_id.astype("int"),
        gender=lambda df: df.gender.astype(pd.CategoricalDtype(categories=["F", "M"])),
        appointment_scheduled_datetime=lambda df: pd.to_datetime(df.appointment_scheduled_datetime),
        appointment_day=lambda df: pd.to_datetime(df.appointment_day),
        # Optional: better deterministic category encoding required for model hosting
        neighborhood=lambda df: df.neighborhood.astype("category"),
        scholarship=lambda df: df.scholarship.astype("bool"),
        hipertension=lambda df: df.hipertension.astype("bool"),
        diabetes=lambda df: df.diabetes.astype("bool"),
        alcoholism=lambda df: df.alcoholism.astype("bool"),
        handcap=lambda df: df.handcap.astype("bool"),
        sms_received=lambda df: df.sms_received.astype("bool"),
        no_show=lambda df: (df.no_show == "Yes"),
    )
    return appointments_types
