from dao.patient_dao import PatientDAO
from models.patient import Patient
from typing import List, Optional
from datetime import datetime

class PatientService:
    @staticmethod
    def add_patient(patient: Patient) -> bool:
        # Basic validation: name and dob required
        if not patient.name.strip():
            raise ValueError("Patient name cannot be empty.")
        if not patient.dob:
            raise ValueError("Patient date of birth is required.")
        # Validate DOB format and reasonable age
        try:
            dob_date = datetime.strptime(patient.dob, "%Y-%m-%d")
            age = (datetime.today() - dob_date).days // 365
            if age < 0 or age > 120:
                raise ValueError("Patient date of birth is not realistic.")
        except ValueError:
            raise ValueError("Patient date of birth must be in YYYY-MM-DD format.")
        
        # Additional validations can be added here

        return PatientDAO.insert_patient(patient)

    @staticmethod
    def update_patient(patient: Patient) -> bool:
        if not patient.name.strip():
            raise ValueError("Patient name cannot be empty.")
        if not patient.dob:
            raise ValueError("Patient date of birth is required.")
        try:
            dob_date = datetime.strptime(patient.dob, "%Y-%m-%d")
            age = (datetime.today() - dob_date).days // 365
            if age < 0 or age > 120:
                raise ValueError("Patient date of birth is not realistic.")
        except ValueError:
            raise ValueError("Patient date of birth must be in YYYY-MM-DD format.")

        return PatientDAO.update_patient(patient)

    @staticmethod
    def delete_patient(patient_id: int) -> bool:
        return PatientDAO.delete_patient(patient_id)

    @staticmethod
    def get_patient_by_id(patient_id: int) -> Optional[Patient]:
        return PatientDAO.get_patient_by_id(patient_id)

    @staticmethod
    def get_all_patients() -> List[Patient]:
        return PatientDAO.get_all_patients()
