import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox

from models.doctor import Doctor
from services.doctor_service import DoctorService

class DoctorPage(ttkb.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.controller = kwargs.pop('controller', None)
        super().__init__(parent, *args, **kwargs)

        self.doctor_service = DoctorService()
        self.selected_id = None

        self.create_widgets()
        self.load_doctor_data()

    def create_widgets(self):
        # Title
        ttkb.Label(self, text="Manage Doctors", font=("Arial", 18, "bold")).pack(pady=15)

        form_frame = ttkb.Frame(self)
        form_frame.pack(pady=10)

        # Name
        ttkb.Label(form_frame, text="Name").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = ttkb.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Specialty
        ttkb.Label(form_frame, text="Specialty").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.specialty_entry = ttkb.Entry(form_frame, width=30)
        self.specialty_entry.grid(row=1, column=1, padx=5, pady=5)

        # Contact
        ttkb.Label(form_frame, text="Contact Info").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.contact_entry = ttkb.Entry(form_frame, width=30)
        self.contact_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttkb.Frame(self)
        button_frame.pack(pady=10)

        ttkb.Button(button_frame, text="Add / Update", command=self.save_doctor, bootstyle="success").grid(row=0, column=0, padx=10)
        ttkb.Button(button_frame, text="Clear", command=self.clear_form).grid(row=0, column=1, padx=10)
        ttkb.Button(button_frame, text="Delete", command=self.delete_doctor, bootstyle="danger").grid(row=0, column=2, padx=10)

        # Doctor list
        self.tree = ttkb.Treeview(self, columns=("ID", "Name", "Specialty", "Contact"), show="headings", height=8, bootstyle="info")
        for col in ("ID", "Name", "Specialty", "Contact"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10, fill="x", padx=20)

        self.tree.bind("<<TreeviewSelect>>", self.on_doctor_select)

    def load_doctor_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for doctor in self.doctor_service.get_all_doctors():
            self.tree.insert("", "end", values=(doctor.id, doctor.name, doctor.specialty, doctor.contact_info))

    def save_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        contact = self.contact_entry.get().strip()

        try:
            if self.selected_id:
                doctor = Doctor(id=self.selected_id, name=name, specialty=specialty, contact_info=contact)
                success = self.doctor_service.update_doctor(doctor)
            else:
                doctor = Doctor(name=name, specialty=specialty, contact_info=contact)
                success = self.doctor_service.add_doctor(doctor)

            if success:
                self.clear_form()
                self.load_doctor_data()
            else:
                messagebox.showerror("Error", "Operation failed.")
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def delete_doctor(self):
        if self.selected_id:
            confirmed = messagebox.askyesno("Delete Doctor", "Are you sure you want to delete this doctor?")
            if confirmed:
                if self.doctor_service.delete_doctor(self.selected_id):
                    self.clear_form()
                    self.load_doctor_data()

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.specialty_entry.delete(0, "end")
        self.contact_entry.delete(0, "end")
        self.selected_id = None
        self.tree.selection_remove(self.tree.selection())

    def on_doctor_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.selected_id = int(values[0])
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, values[1])
            self.specialty_entry.delete(0, "end")
            self.specialty_entry.insert(0, values[2])
            self.contact_entry.delete(0, "end")
            self.contact_entry.insert(0, values[3])
