import os
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from ui.patient_page import PatientPage
from ui.appointment_page import AppointmentPage
from ui.billing_page import BillingPage
from ui.dashboard_page import DashboardPage
from ui.doctor_page import DoctorPage
from database import Database
WINDOW_TITLE = "Clinic Management System"
WINDOW_SIZE = "1000x600"

# Initialize the database connection
db = Database()
db.initialize_schema()

class ClinicApp(ttkb.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Options: darkly, cyborg, superhero, etc.

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(True, True)

        # Set custom window icon
        try:
            icon_path = os.path.join("resources", "pyCMS_icon.png")
            icon = ttkb.PhotoImage(file=icon_path)
            self.iconphoto(False, icon)
        except Exception as e:
            print(f"[ICON ERROR] Could not load window icon: {e}")

        # Container to stack all pages
        container = ttkb.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Define all pages
        for F in (DashboardPage, PatientPage, AppointmentPage, BillingPage, DoctorPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menu()
        self.show_frame("DashboardPage")

    def create_menu(self):
        menubar = ttkb.Menu(self)
        
        navigation_menu = ttkb.Menu(menubar, tearoff=0)
        navigation_menu.add_command(label="Dashboard", command=lambda: self.show_frame("DashboardPage"))
        navigation_menu.add_command(label="Patients", command=lambda: self.show_frame("PatientPage"))
        navigation_menu.add_command(label="Doctors", command=lambda: self.show_frame("DoctorPage"))
        navigation_menu.add_command(label="Appointments", command=lambda: self.show_frame("AppointmentPage"))
        navigation_menu.add_command(label="Billing", command=lambda: self.show_frame("BillingPage"))
        navigation_menu.add_separator()
        navigation_menu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="Navigation", menu=navigation_menu)
        self.config(menu=menubar)

    def show_frame(self, page_name):
        """Raise the frame with the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()
        # Refresh data if the page supports it
        if hasattr(frame, "load_summary"):
            frame.load_summary()
        if hasattr(frame, "load_doctor_data"):
            frame.load_doctor_data()
        if hasattr(frame, "load_patient_data"):
            frame.load_patient_data()

if __name__ == "__main__":
    app = ClinicApp()
    app.mainloop()
