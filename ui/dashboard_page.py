import tkinter as tk
from tkinter import ttk
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.doctor_service import DoctorService
from services.billing_service import BillingService

class DashboardPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.controller = kwargs.pop('controller', None)
        super().__init__(parent, *args, **kwargs)

        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()
        self.doctor_service = DoctorService()
        self.billing_service = BillingService()

        self.create_widgets()
        self.load_summary()

    def create_widgets(self):
        # Top-center title using grid
        title_frame = ttk.Frame(self)
        title_frame.pack(fill="x", pady=(20, 10))

        title_label = tk.Label(title_frame, text="Clinic Dashboard", font=("Arial", 18, "bold"))
        title_label.pack(anchor="center")

        # Summary cards
        summary_frame = ttk.Frame(self)
        summary_frame.pack(padx=20, pady=10, fill="x")

        summary_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.patient_count_label = self._create_summary_card(summary_frame, "Total Patients", 0)
        self.appointment_count_label = self._create_summary_card(summary_frame, "Total Appointments", 1)
        self.doctor_count_label = self._create_summary_card(summary_frame, "Total Doctors", 2)
        self.billing_count_label = self._create_summary_card(summary_frame, "Total Billings", 3)

    def _create_summary_card(self, parent, title, column):
        frame = ttk.Frame(parent, relief="ridge", borderwidth=2, padding=10)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame, text=title, font=("Arial", 12)).pack()
        count_label = ttk.Label(frame, text="0", font=("Arial", 24, "bold"), foreground="blue")
        count_label.pack()
        return count_label

    def load_summary(self):
        patient_count = len(self.patient_service.get_all_patients())
        appointment_count = len(self.appointment_service.get_all_appointments())
        doctor_count = len(self.doctor_service.get_all_doctors())
        billing_count = len(self.billing_service.get_all_billings())

        self.patient_count_label.config(text=str(patient_count))
        self.appointment_count_label.config(text=str(appointment_count))
        self.doctor_count_label.config(text=str(doctor_count))
        self.billing_count_label.config(text=str(billing_count))
