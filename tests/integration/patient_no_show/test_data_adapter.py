"""Integration tests for data adapter."""
from patient_no_show.data_adapter import load_patients_appointment_data


def test_load_patients_appointment_data():
    """Test data integrity."""
    data = load_patients_appointment_data()
    assert not data.empty
