"""Application main."""
from project.data_adapter import load_patients_appointment_data

if __name__ == "__main__":
    patient_appointments = load_patients_appointment_data()
    print(patient_appointments)
