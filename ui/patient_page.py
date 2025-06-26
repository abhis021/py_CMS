import tkinter as tk
from tkinter import ttk, messagebox
from models.patient import Patient
from services.patient_service import PatientService
from datetime import datetime

class PatientPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.controller = kwargs.pop('controller', None )
        super().__init__(parent, *args, **kwargs)

        self.patient_service = PatientService()

        self.create_widgets()
        self.load_patients()

    def create_widgets(self):
        tk.Label(self, text="Patient Management", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Form Labels and Inputs
        tk.Label(self, text="Name:").grid(row=1, column=0, sticky="e")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="DOB (YYYY-MM-DD):").grid(row=1, column=2, sticky="e")
        self.dob_entry = tk.Entry(self)
        self.dob_entry.grid(row=1, column=3, sticky="w")

        tk.Label(self, text="Gender:").grid(row=2, column=0, sticky="e")
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(self, textvariable=self.gender_var, state="readonly")
        self.gender_combo['values'] = ("Male", "Female", "Other")
        self.gender_combo.grid(row=2, column=1, sticky="w")
        self.gender_combo.current(0)

        tk.Label(self, text="Contact Info:").grid(row=2, column=2, sticky="e")
        self.contact_entry = tk.Entry(self)
        self.contact_entry.grid(row=2, column=3, sticky="w")

        tk.Label(self, text="Address:").grid(row=3, column=0, sticky="ne")
        self.address_text = tk.Text(self, width=40, height=4)
        self.address_text.grid(row=3, column=1, columnspan=3, sticky="w")

        # Buttons
        self.add_btn = tk.Button(self, text="Add Patient", command=self.add_patient)
        self.add_btn.grid(row=4, column=0, pady=10)

        self.refresh_btn = tk.Button(self, text="Refresh List", command=self.load_patients)
        self.refresh_btn.grid(row=4, column=1, pady=10)

        # Patient List Treeview
        columns = ("id", "name", "dob", "gender", "contact", "address")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=5, column=0, columnspan=4, sticky="nsew", pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=5, column=4, sticky="ns")

        # Configure grid weights for resizing
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def load_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        patients = self.patient_service.get_all_patients()
        for p in patients:
            self.tree.insert(
                "",
                "end",
                values=(
                    p.id,
                    p.name,
                    p.dob,
                    p.gender,
                    p.contact_info,
                    p.address,
                )
            )

    def add_patient(self):
        try:
            name = self.name_entry.get().strip()
            dob = self.dob_entry.get().strip()
            gender = self.gender_var.get()
            contact = self.contact_entry.get().strip()
            address = self.address_text.get("1.0", tk.END).strip()

            # Basic UI validation
            if not name:
                raise ValueError("Name is required.")
            if not dob:
                raise ValueError("Date of Birth is required.")
            # Validate date format
            datetime.strptime(dob, "%Y-%m-%d")

            new_patient = Patient(
                name=name,
                dob=dob,
                gender=gender,
                contact_info=contact,
                address=address
            )

            success = self.patient_service.add_patient(new_patient)
            if success:
                messagebox.showinfo("Success", "Patient added successfully!")
                self.clear_form()
                self.load_patients()
            else:
                messagebox.showerror("Error", "Failed to add patient.")

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.gender_combo.current(0)
        self.contact_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
