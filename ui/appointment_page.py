import tkinter as tk
from tkinter import ttk, messagebox
from models.appointment import Appointment
from services.appointment_service import AppointmentService
from services.patient_service import PatientService
from services.doctor_service import DoctorService
from datetime import datetime

class AppointmentPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.controller = kwargs.pop("controller", None)
        super().__init__(parent, *args, **kwargs)

        self.appointment_service = AppointmentService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()

        self.create_widgets()
        self.load_appointments()
        self.load_doctors_and_patients()
        self.clear_form()
        self.bind("<FocusIn>", self.on_focus)

    def create_widgets(self):
        tk.Label(self, text="Appointment Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self, text="Patient:").grid(row=1, column=0, sticky="e")
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(self, textvariable=self.patient_var, state="readonly")
        self.patient_combo.grid(row=1, column=1, sticky="w")
        self.patient_combo.bind("<<ComboboxSelected>>", self.update_dob_label)

        tk.Label(self, text="Doctor:").grid(row=1, column=2, sticky="e")
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(self, textvariable=self.doctor_var, state="readonly")
        self.doctor_combo.grid(row=1, column=3, sticky="w")

        tk.Label(self, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
        self.date_entry = tk.Entry(self, width=20)
        self.date_entry.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Time (HH:MM):").grid(row=2, column=2, sticky="e")
        self.time_entry = tk.Entry(self, width=20)
        self.time_entry.grid(row=2, column=3, sticky="w")

        tk.Label(self, text="DOB:").grid(row=3, column=0, sticky="e")
        self.dob_label = tk.Label(self, text="", anchor="w")
        self.dob_label.grid(row=3, column=1, sticky="w")

        tk.Label(self, text="Reason:").grid(row=4, column=0, sticky="e")
        self.reason_entry = tk.Entry(self, width=50)
        self.reason_entry.grid(row=4, column=1, columnspan=3, sticky="w")

        self.add_btn = tk.Button(self, text="Add Appointment", command=self.add_appointment)
        self.add_btn.grid(row=5, column=0, pady=10)

        self.refresh_btn = tk.Button(self, text="Refresh List", command=self.load_appointments)
        self.refresh_btn.grid(row=5, column=1, pady=10)

        columns = ("id", "patient", "doctor", "date", "time", "reason", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100, anchor="center")
        self.tree.grid(row=6, column=0, columnspan=4, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=4, sticky="ns")

        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def load_patients(self):
        patients = self.patient_service.get_all_patients()
        self.patients_map = {p.get_summary(): p for p in patients}
        self.patient_combo['values'] = list(self.patients_map.keys())
        if patients:
            self.patient_combo.current(0)
            self.update_dob_label()

    def load_doctors(self):
        doctors = self.doctor_service.get_all_doctors()
        self.doctors_map = {d.get_display_name(): d.id for d in doctors}
        self.doctor_combo['values'] = list(self.doctors_map.keys())
        if doctors:
            self.doctor_combo.current(0)

    def load_doctors_and_patients(self):
        self.load_patients()
        self.load_doctors()

    def load_appointments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        appointments = self.appointment_service.get_all_appointments()
        patients = self.patient_service.get_all_patients()
        doctors = self.doctor_service.get_all_doctors()

        patient_dict = {p.id: p.get_summary() for p in patients}
        doctor_dict = {d.id: d.get_display_name() for d in doctors}

        for appt in appointments:
            self.tree.insert(
                "",
                "end",
                values=(
                    appt.id,
                    patient_dict.get(appt.patient_id, "Unknown"),
                    doctor_dict.get(appt.doctor_id, "Unknown"),
                    appt.date,
                    appt.time,
                    appt.reason,
                    appt.status
                )
            )

    def update_dob_label(self, event=None):
        selected_summary = self.patient_var.get()
        patient = self.patients_map.get(selected_summary)
        self.dob_label.config(text=patient.dob if patient else "")

    def add_appointment(self):
        try:
            patient_name = self.patient_var.get()
            doctor_name = self.doctor_var.get()
            date_str = self.date_entry.get().strip()
            time_str = self.time_entry.get().strip()
            reason = self.reason_entry.get().strip()

            if not patient_name or patient_name not in self.patients_map:
                raise ValueError("Please select a valid patient.")
            if not doctor_name or doctor_name not in self.doctors_map:
                raise ValueError("Please select a valid doctor.")
            if not date_str:
                raise ValueError("Please enter the appointment date.")
            if not time_str:
                raise ValueError("Please enter the appointment time.")

            datetime.strptime(date_str, "%Y-%m-%d")
            datetime.strptime(time_str, "%H:%M")

            new_appointment = Appointment(
                patient_id=self.patients_map[patient_name].id,
                doctor_id=self.doctors_map[doctor_name],
                date=date_str,
                time=time_str,
                reason=reason,
                status="Scheduled"
            )

            success = self.appointment_service.add_appointment(new_appointment)
            if success:
                messagebox.showinfo("Success", "Appointment added successfully!")
                self.clear_form()
                self.load_appointments()
                self.refresh_dropdowns()
            else:
                messagebox.showerror("Error", "Failed to add appointment.")

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def clear_form(self):
        if self.patient_combo['values']:
            self.patient_combo.current(0)
            self.update_dob_label()
        if self.doctor_combo['values']:
            self.doctor_combo.current(0)
        now = datetime.now()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, now.strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, now.strftime("%H:%M"))
        self.reason_entry.delete(0, tk.END)

    def refresh_dropdowns(self):
        self.load_doctors_and_patients()
        self.update_dob_label()

    def on_focus(self, event):
        self.refresh_dropdowns()