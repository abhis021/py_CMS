from dao.doctor_dao import DoctorDAO
from models.doctor import Doctor
from typing import List, Optional

class DoctorService:
    @staticmethod
    def add_doctor(doctor: Doctor) -> bool:
        # Basic validation: name required
        if not doctor.name.strip():
            raise ValueError("Doctor name cannot be empty.")
        
        # Additional business rules can be added here

        return DoctorDAO.insert_doctor(doctor)

    @staticmethod
    def update_doctor(doctor: Doctor) -> bool:
        if not doctor.name.strip():
            raise ValueError("Doctor name cannot be empty.")
        
        return DoctorDAO.update_doctor(doctor)

    @staticmethod
    def delete_doctor(doctor_id: int) -> bool:
        return DoctorDAO.delete_doctor(doctor_id)

    @staticmethod
    def get_doctor_by_id(doctor_id: int) -> Optional[Doctor]:
        return DoctorDAO.get_doctor_by_id(doctor_id)

    @staticmethod
    def get_all_doctors() -> List[Doctor]:
        return DoctorDAO.get_all_doctors()
