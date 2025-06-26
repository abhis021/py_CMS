from database import Database
from models.doctor import Doctor

db = Database()

class DoctorDAO:
    @staticmethod
    def insert_doctor(doctor: Doctor) -> bool:
        query = """
            INSERT INTO doctors (name, specialty, contact_info)
            VALUES (?, ?, ?)
        """
        params = (doctor.name, doctor.specialty, doctor.contact_info)
        return db.execute_query(query, params)

    @staticmethod
    def update_doctor(doctor: Doctor) -> bool:
        query = """
            UPDATE doctors
            SET name = ?, specialty = ?, contact_info = ?
            WHERE id = ?
        """
        params = (doctor.name, doctor.specialty, doctor.contact_info, doctor.id)
        return db.execute_query(query, params)

    @staticmethod
    def delete_doctor(doctor_id: int) -> bool:
        query = "DELETE FROM doctors WHERE id = ?"
        return db.execute_query(query, (doctor_id,))

    @staticmethod
    def get_doctor_by_id(doctor_id: int) -> Doctor | None:
        query = "SELECT * FROM doctors WHERE id = ?"
        row = db.fetch_one(query, (doctor_id,))
        if row:
            return Doctor(*row)
        return None

    @staticmethod
    def get_all_doctors() -> list[Doctor]:
        query = "SELECT * FROM doctors ORDER BY name"
        rows = db.fetch_all(query)
        return [Doctor(*row) for row in rows]
