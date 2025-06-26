import tkinter as tk
from tkinter import ttk
from ui.dashboard_page import DashboardPage
from ui.patient_page import PatientPage
from ui.appointment_page import AppointmentPage
from ui.billing_page import BillingPage

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clinic Management System")
        self.geometry("900x600")

        # Create container frame for pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize pages
        for F in (DashboardPage, PatientPage, AppointmentPage, BillingPage):
            page_name = F.__name__
            frame = F(container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show default page
        self.show_frame("DashboardPage")

        # Setup menu bar
        self.create_menu()

        # Configure resizing
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def create_menu(self):
        menubar = tk.Menu(self)
        
        navigate_menu = tk.Menu(menubar, tearoff=0)
        navigate_menu.add_command(label="Dashboard", command=lambda: self.show_frame("DashboardPage"))
        navigate_menu.add_command(label="Patients", command=lambda: self.show_frame("PatientPage"))
        navigate_menu.add_command(label="Appointments", command=lambda: self.show_frame("AppointmentPage"))
        navigate_menu.add_command(label="Billing", command=lambda: self.show_frame("BillingPage"))
        menubar.add_cascade(label="Navigate", menu=navigate_menu)

        self.config(menu=menubar)

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
        else:
            print(f"Page '{page_name}' not found.")
