import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry as TkDateEntry

class SafeDateEntry(TkDateEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
