from database import Database
from models.patient import Patient

db = Database()

class PatientDAO:
    @staticmethod
    def insert_patient(patient: Patient) -> bool:
        query = """
            INSERT INTO patients (name, dob, gender, contact_info, address)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (patient.name, patient.dob, patient.gender, patient.contact_info, patient.address)
        return db.execute_query(query, params)

    @staticmethod
    def update_patient(patient: Patient) -> bool:
        query = """
            UPDATE patients
            SET name = ?, dob = ?, gender = ?, contact_info = ?, address = ?
            WHERE id = ?
        """
        params = (patient.name, patient.dob, patient.gender, patient.contact_info, patient.address, patient.id)
        return db.execute_query(query, params)

    @staticmethod
    def delete_patient(patient_id: int) -> bool:
        query = "DELETE FROM patients WHERE id = ?"
        return db.execute_query(query, (patient_id,))

    @staticmethod
    def get_patient_by_id(patient_id: int) -> Patient | None:
        query = "SELECT * FROM patients WHERE id = ?"
        row = db.fetch_one(query, (patient_id,))
        if row:
            return Patient(*row)
        return None

    @staticmethod
    def get_all_patients() -> list[Patient]:
        query = "SELECT * FROM patients ORDER BY name"
        rows = db.fetch_all(query)
        return [Patient(*row) for row in rows]
