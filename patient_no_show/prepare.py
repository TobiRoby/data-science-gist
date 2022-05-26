"""Data preparation."""
from pandera.typing.pandas import DataFrame

from patient_no_show.schema import PatientsAppointment, PatientsAppointmentFeaturesLabel


def engineer_features(
    *,
    patient_appointments: DataFrame[PatientsAppointment],
) -> DataFrame[PatientsAppointmentFeaturesLabel]:
    """Engineer new features.

    Args:
        patient_appointments (DataFrame[PatientsAppointment]): patients appointment data

    Returns:
        DataFrame[PatientsAppointmentFeaturesLabel]: patients appointment data with added features
    """
    patient_appointments_features = patient_appointments.assign(
        days_between_scheduling_and_appointment=lambda df: (
            df.appointment_day - df.appointment_scheduled_datetime
        )
        .dt.total_seconds()
        .div(60)
        .div(60)
        .div(24)
        .clip(lower=0),
        appointment_scheduling_dayofweek=lambda df: df.appointment_scheduled_datetime.dt.dayofweek,
        appointment_scheduling_hour=lambda df: df.appointment_scheduled_datetime.dt.hour,
    )

    return patient_appointments_features
