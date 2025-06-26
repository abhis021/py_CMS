import tkinter as tk
from tkinter import ttk
from datetime import datetime

class LabeledEntry(ttk.Frame):
    """A compound widget combining a label and an entry field."""

    def __init__(self, parent, label_text="", entry_width=20, **kwargs):
        super().__init__(parent, **kwargs)
        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self, width=entry_width)

        self.label.pack(side="left", padx=(0, 5))
        self.entry.pack(side="left", fill="x", expand=True)

    def get(self) -> str:
        return self.entry.get()

    def set(self, text: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def clear(self):
        self.entry.delete(0, tk.END)


class DateEntry(ttk.Frame):
    """A very simple date entry widget with placeholder and basic validation."""

    def __init__(self, parent, date_format="%Y-%m-%d", **kwargs):
        super().__init__(parent, **kwargs)
        self.date_format = date_format

        self.entry = ttk.Entry(self, width=12)
        self.entry.pack(side="left")

        self.entry.insert(0, self.date_format)  # Placeholder text

        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, event):
        current = self.entry.get()
        if current == self.date_format:
            self.entry.delete(0, tk.END)

    def _add_placeholder(self, event):
        current = self.entry.get()
        if not current:
            self.entry.insert(0, self.date_format)

    def get_date(self):
        date_str = self.entry.get()
        try:
            date_obj = datetime.strptime(date_str, self.date_format)
            return date_obj.date()
        except ValueError:
            return None

    def set_date(self, date_obj):
        if isinstance(date_obj, (datetime,)):
            date_str = date_obj.strftime(self.date_format)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, date_str)

    def clear(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.date_format)
