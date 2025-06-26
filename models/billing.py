from datetime import datetime

class Billing:
    def __init__(self, id=None, patient_id=None, appointment_id=None, amount=0.0, date=None, status="Unpaid", services_rendered=""):
        self.id = id  # primary key
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.date = date or datetime.today().strftime("%Y-%m-%d")  # default to today
        self.status = status  # Unpaid, Paid, Pending, etc.
        self.services_rendered = services_rendered

    def __repr__(self):
        return f"<Billing id={self.id} patient_id={self.patient_id} amount={self.amount} status={self.status}>"

    def mark_as_paid(self):
        self.status = "Paid"

    def is_overdue(self):
        """Check if billing date is older than today and still unpaid."""
        try:
            billing_date = datetime.strptime(self.date, "%Y-%m-%d")
            return billing_date < datetime.today() and self.status != "Paid"
        except ValueError:
            return False
