import re
from tkinter import messagebox
from datetime import datetime

def validate_date(date_str, date_format="%Y-%m-%d"):
    """
    Validates if a string matches the given date format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def is_valid_phone_number(phone):
    """
    Simple phone number validation (digits only, length between 7 and 15).
    Adjust the regex as per your locale requirements.
    """
    pattern = re.compile(r"^\+?\d{7,15}$")
    return bool(pattern.match(phone))

def show_info(message, title="Info"):
    """
    Wrapper to show an informational messagebox.
    """
    messagebox.showinfo(title, message)

def show_error(message, title="Error"):
    """
    Wrapper to show an error messagebox.
    """
    messagebox.showerror(title, message)

def show_warning(message, title="Warning"):
    """
    Wrapper to show a warning messagebox.
    """
    messagebox.showwarning(title, message)
