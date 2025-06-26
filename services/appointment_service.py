from dao.appointment_dao import AppointmentDAO
from models.appointment import Appointment
from typing import List, Optional

class AppointmentService:
    @staticmethod
    def add_appointment(appointment: Appointment) -> bool:
        # Business rule: Appointment date/time cannot be in the past
        if appointment.is_in_past():
            raise ValueError("Cannot schedule an appointment in the past.")

        # More business logic can be added here

        return AppointmentDAO.insert_appointment(appointment)

    @staticmethod
    def update_appointment(appointment: Appointment) -> bool:
        # Business rule validations before updating
        if appointment.is_in_past():
            raise ValueError("Cannot update an appointment to a past date/time.")

        return AppointmentDAO.update_appointment(appointment)

    @staticmethod
    def delete_appointment(appointment_id: int) -> bool:
        return AppointmentDAO.delete_appointment(appointment_id)

    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Optional[Appointment]:
        return AppointmentDAO.get_appointment_by_id(appointment_id)

    @staticmethod
    def get_appointments_by_patient(patient_id: int) -> List[Appointment]:
        return AppointmentDAO.get_appointments_by_patient(patient_id)

    @staticmethod
    def get_all_appointments() -> List[Appointment]:
        return AppointmentDAO.get_all_appointments()
