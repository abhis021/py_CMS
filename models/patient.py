from datetime import datetime

class Patient:
    def __init__(self, id=None, name="", dob="", gender="", contact_info="", address=""):
        self.id = id  # Primary key
        self.name = name
        self.dob = dob  # Date of Birth in 'YYYY-MM-DD' format
        self.gender = gender
        self.contact_info = contact_info
        self.address = address

    def __repr__(self):
        return f"<Patient id={self.id} name={self.name} dob={self.dob}>"

    def calculate_age(self):
        """Calculates age based on DOB."""
        try:
            birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
            today = datetime.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except Exception:
            return None

    def get_summary(self):
        """Returns a short string summary of the patient."""
        age = self.calculate_age()
        return f"{self.name} ({self.gender}, {age} yrs)" if age is not None else f"{self.name} ({self.gender})"
