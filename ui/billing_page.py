import tkinter as tk
from tkinter import ttk, messagebox
from models.billing import Billing
from services.billing_service import BillingService
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from datetime import datetime

class BillingPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.controller = kwargs.pop("controller", None)
        super().__init__(parent, *args, **kwargs)

        # Services
        self.billing_service = BillingService()
        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()

        # UI Setup
        self.create_widgets()
        self.load_billings()
        self.load_patients()
        self.load_appointments()

    def create_widgets(self):
        tk.Label(self, text="Billing Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Patient Selection
        tk.Label(self, text="Patient:").grid(row=1, column=0, sticky="e")
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(self, textvariable=self.patient_var, state="readonly")
        self.patient_combo.grid(row=1, column=1, sticky="w")
        self.patient_combo.bind("<<ComboboxSelected>>", self.on_patient_selected)

        # Appointment Selection
        tk.Label(self, text="Appointment:").grid(row=1, column=2, sticky="e")
        self.appointment_var = tk.StringVar()
        self.appointment_combo = ttk.Combobox(self, textvariable=self.appointment_var, state="readonly")
        self.appointment_combo.grid(row=1, column=3, sticky="w")

        # Amount
        tk.Label(self, text="Amount:").grid(row=2, column=0, sticky="e")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=2, column=1, sticky="w")

        # Status
        tk.Label(self, text="Status:").grid(row=2, column=2, sticky="e")
        self.status_var = tk.StringVar(value="Pending")
        self.status_combo = ttk.Combobox(self, textvariable=self.status_var, state="readonly")
        self.status_combo['values'] = ["Pending", "Paid", "Cancelled"]
        self.status_combo.grid(row=2, column=3, sticky="w")

        # Services Rendered
        tk.Label(self, text="Services Rendered:").grid(row=3, column=0, sticky="ne")
        self.services_text = tk.Text(self, height=4, width=50)
        self.services_text.grid(row=3, column=1, columnspan=3, sticky="w")

        # Buttons
        self.add_btn = tk.Button(self, text="Add Billing", command=self.add_billing)
        self.add_btn.grid(row=4, column=0, pady=10)

        self.refresh_btn = tk.Button(self, text="Refresh List", command=self.load_billings)
        self.refresh_btn.grid(row=4, column=1, pady=10)

        # Billing List (Treeview)
        columns = ("id", "patient", "appointment", "amount", "date", "status", "services_rendered")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=5, column=4, sticky="ns")

        # Grid weights for resizing
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def load_patients(self):
        patients = self.patient_service.get_all_patients()
        self.patients_map = {p.get_summary(): p.id for p in patients}
        self.patient_combo['values'] = list(self.patients_map.keys())
        if patients:
            self.patient_combo.current(0)
            self.load_appointments()  # Load appointments for first patient

    def on_patient_selected(self, event):
        self.load_appointments()

    def load_appointments(self):
        patient_name = self.patient_var.get()
        if not patient_name or patient_name not in self.patients_map:
            self.appointment_combo['values'] = []
            return
        patient_id = self.patients_map[patient_name]
        appointments = self.appointment_service.get_appointments_by_patient(patient_id)
        self.appointments_map = {f"{appt.date} {appt.time} (ID:{appt.id})": appt.id for appt in appointments}
        self.appointment_combo['values'] = list(self.appointments_map.keys())
        if appointments:
            self.appointment_combo.current(0)
        else:
            self.appointment_combo.set('')

    def load_billings(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        billings = self.billing_service.get_all_billings()
        patients = self.patient_service.get_all_patients()
        patient_dict = {p.id: p.get_summary() for p in patients}

        appointments = self.appointment_service.get_all_appointments()
        appointment_dict = {a.id: f"{a.date} {a.time}" for a in appointments}

        for bill in billings:
            self.tree.insert(
                "",
                "end",
                values=(
                    bill.id,
                    patient_dict.get(bill.patient_id, "Unknown"),
                    appointment_dict.get(bill.appointment_id, "Unknown"),
                    f"{bill.amount:.2f}",
                    bill.date,
                    bill.status,
                    bill.services_rendered,
                )
            )

    def add_billing(self):
        try:
            patient_name = self.patient_var.get()
            appointment_desc = self.appointment_var.get()
            amount_str = self.amount_entry.get().strip()
            status = self.status_var.get()
            services = self.services_text.get("1.0", tk.END).strip()
            date_str = datetime.today().strftime("%Y-%m-%d")

            if not patient_name or patient_name not in self.patients_map:
                raise ValueError("Please select a valid patient.")
            if not appointment_desc or appointment_desc not in self.appointments_map:
                raise ValueError("Please select a valid appointment.")
            if not amount_str:
                raise ValueError("Please enter the billing amount.")
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")

            new_billing = Billing(
                patient_id=self.patients_map[patient_name],
                appointment_id=self.appointments_map[appointment_desc],
                amount=amount,
                date=date_str,
                status=status,
                services_rendered=services
            )

            success = self.billing_service.add_billing(new_billing)
            if success:
                messagebox.showinfo("Success", "Billing record added successfully!")
                self.clear_form()
                self.load_billings()
            else:
                messagebox.showerror("Error", "Failed to add billing record.")

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def clear_form(self):
        if self.patient_combo['values']:
            self.patient_combo.current(0)
        self.load_appointments()
        self.amount_entry.delete(0, tk.END)
        self.status_combo.set("Pending")
        self.services_text.delete("1.0", tk.END)
