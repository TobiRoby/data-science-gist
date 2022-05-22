"""Data(frame) schemas."""
import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


class StrictModel(SchemaModel):
    """Strict model schema: no differences from specified columns allowed."""

    class Config:
        """Schema configuration."""

        strict = True


class DataAdapterModel(StrictModel):
    """Data adapter model schema: coerce incoming data to expected."""

    class Config:
        """Schema configuration."""

        coerce = True


class PatientsAppointment(DataAdapterModel):
    """Patient appointment data."""

    patient_id: Series[int] = Field(ge=0, description="patient id")
    appointment_id: Series[int] = Field(ge=0, description="appointment id")
    gender: Series[pd.CategoricalDtype] = Field(
        dtype_kwargs={"categories": ["F", "M"], "ordered": False}, description="patient's gender"
    )
    scheduled_datetime: Series[pd.DatetimeTZDtype] = Field(
        dtype_kwargs={"unit": "ns", "tz": "UTC"},
        description="datetime when an appointment is booked",
    )
    appointment_day: Series[pd.DatetimeTZDtype] = Field(
        dtype_kwargs={"unit": "ns", "tz": "UTC"}, description="day when an appointment is scheduled"
    )
    age: Series[int] = Field(description="patient's age")
    neighborhood: Series[pd.CategoricalDtype] = Field(description="patient's neighborhood")
    scholarship: Series[bool] = Field(description="True, if patient has a scholarship.")
    hipertension: Series[bool] = Field(description="True, if patient has hipertension.")
    diabetes: Series[bool] = Field(description="True, if patient has diabetes.")
    alcoholism: Series[bool] = Field(description="True, if patient has alcoholism.")
    handcap: Series[bool] = Field(description="True, if patient has a handicap.")
    sms_received: Series[bool] = Field(description="True, if patient has received a sms.")
    no_show: Series[bool] = Field(description="True, if patient showed up to the appointment.")


class PatientsAppointmentFeaturesLabel(PatientsAppointment):
    """Features and label for model training of appointment no_show."""


class PatientsAppointmentFeaturesLabelPrediction(PatientsAppointmentFeaturesLabel):
    """Features, label and prediction for model training of appointment no_show."""

    no_show_probability_prediction: Series[float] = Field(
        description="model no_show probability prediction"
    )
