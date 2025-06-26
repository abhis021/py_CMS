class Doctor:
    def __init__(self, id=None, name="", specialty="", contact_info=""):
        self.id = id  # Primary key
        self.name = name
        self.specialty = specialty
        self.contact_info = contact_info

    def __repr__(self):
        return f"<Doctor id={self.id} name={self.name} specialty={self.specialty}>"

    def get_display_name(self):
        """Returns a display-friendly name for dropdowns or listings."""
        return f"Dr. {self.name} ({self.specialty})"
