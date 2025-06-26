from database import Database
from models.appointment import Appointment

db = Database()

class AppointmentDAO:
    @staticmethod
    def insert_appointment(appointment: Appointment) -> bool:
        query = """
            INSERT INTO appointments (patient_id, doctor_id, date, time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            appointment.patient_id,
            appointment.doctor_id,
            appointment.date,
            appointment.time,
            appointment.reason,
            appointment.status,
        )
        return db.execute_query(query, params)

    @staticmethod
    def update_appointment(appointment: Appointment) -> bool:
        query = """
            UPDATE appointments
            SET patient_id = ?, doctor_id = ?, date = ?, time = ?, reason = ?, status = ?
            WHERE id = ?
        """
        params = (
            appointment.patient_id,
            appointment.doctor_id,
            appointment.date,
            appointment.time,
            appointment.reason,
            appointment.status,
            appointment.id,
        )
        return db.execute_query(query, params)

    @staticmethod
    def delete_appointment(appointment_id: int) -> bool:
        query = "DELETE FROM appointments WHERE id = ?"
        return db.execute_query(query, (appointment_id,))

    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Appointment | None:
        query = "SELECT * FROM appointments WHERE id = ?"
        row = db.fetch_one(query, (appointment_id,))
        if row:
            return Appointment(*row)
        return None

    @staticmethod
    def get_appointments_by_patient(patient_id: int) -> list[Appointment]:
        query = "SELECT * FROM appointments WHERE patient_id = ? ORDER BY date, time"
        rows = db.fetch_all(query, (patient_id,))
        return [Appointment(*row) for row in rows]

    @staticmethod
    def get_all_appointments() -> list[Appointment]:
        query = "SELECT * FROM appointments ORDER BY date, time"
        rows = db.fetch_all(query)
        return [Appointment(*row) for row in rows]
