from datetime import datetime

class Appointment:
    def __init__(self, id=None, patient_id=None, doctor_id=None, date=None, time=None, reason="", status="Scheduled"):
        self.id = id  # primary key in the database
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date  # string in YYYY-MM-DD format
        self.time = time  # string in HH:MM format
        self.reason = reason
        self.status = status  # Scheduled, Completed, Cancelled, etc.

    def __repr__(self):
        return f"<Appointment id={self.id} patient_id={self.patient_id} doctor_id={self.doctor_id} date={self.date} time={self.time}>"

    def get_datetime(self):
        """Returns a combined datetime object from date and time."""
        try:
            return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        except Exception:
            return None

    def is_in_past(self):
        """Checks if the appointment is scheduled in the past."""
        dt = self.get_datetime()
        return dt is not None and dt < datetime.now()
