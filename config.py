import os
import sys

# Base directory for development
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# For bundled apps (PyInstaller), use _MEIPASS path
def resource_path(relative_path):
    """Return absolute path for bundled and dev environments"""
    base = getattr(sys, '_MEIPASS', BASE_DIR)
    return os.path.join(base, relative_path)

# Read-only database path bundled inside the app (.exe)
BUNDLED_DB_PATH = resource_path("clinic.db")

# UI configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
APP_TITLE = "Clinic Management System"

# Formatting
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M"

# Logging (optional)
LOG_FILE = os.path.join(BASE_DIR, "clinic_app.log")

# Icon path for PyInstaller-compatible builds
APP_ICON_PATH = resource_path(os.path.join("resources", "icon.png"))

APP_VERSION = "1.0.0"
BUILD_DATE = "2025-06-26"