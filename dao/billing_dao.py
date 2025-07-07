from database import Database, get_writable_db_path
from models.billing import Billing

db = Database(get_writable_db_path())

class BillingDAO:
    @staticmethod
    def insert_billing(billing: Billing) -> bool:
        query = """
            INSERT INTO billing (patient_id, appointment_id, amount, date, status, services_rendered)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            billing.patient_id,
            billing.appointment_id,
            billing.amount,
            billing.date,
            billing.status,
            billing.services_rendered,
        )
        return db.execute_query(query, params)

    @staticmethod
    def update_billing(billing: Billing) -> bool:
        query = """
            UPDATE billing
            SET patient_id = ?, appointment_id = ?, amount = ?, date = ?, status = ?, services_rendered = ?
            WHERE id = ?
        """
        params = (
            billing.patient_id,
            billing.appointment_id,
            billing.amount,
            billing.date,
            billing.status,
            billing.services_rendered,
            billing.id,
        )
        return db.execute_query(query, params)

    @staticmethod
    def delete_billing(billing_id: int) -> bool:
        query = "DELETE FROM billing WHERE id = ?"
        return db.execute_query(query, (billing_id,))

    @staticmethod
    def get_billing_by_id(billing_id: int) -> Billing | None:
        query = "SELECT * FROM billing WHERE id = ?"
        row = db.fetch_one(query, (billing_id,))
        if row:
            return Billing(*row)
        return None

    @staticmethod
    def get_billings_by_patient(patient_id: int) -> list[Billing]:
        query = "SELECT * FROM billing WHERE patient_id = ? ORDER BY date DESC"
        rows = db.fetch_all(query, (patient_id,))
        return [Billing(*row) for row in rows]

    @staticmethod
    def get_all_billings() -> list[Billing]:
        query = "SELECT * FROM billing ORDER BY date DESC"
        rows = db.fetch_all(query)
        return [Billing(*row) for row in rows]