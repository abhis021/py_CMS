import os

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "clinic.db")

# UI configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
APP_TITLE = "Clinic Management System"

# Default values (can be used throughout the app)
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M"

# Logging config (optional - if using logging)
LOG_FILE = os.path.join(BASE_DIR, "clinic_app.log")

# Misc
APP_ICON_PATH = os.path.join(BASE_DIR, "resources", "icon.png")  # optional
