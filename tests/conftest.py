import os

# The catalog is chosen when github_monitor.i18n is imported, so pin the test
# session to the English source strings before any test module imports it.
os.environ["LANGUAGE"] = "en"

# Render Qt pixmaps without a display server.
os.environ["QT_QPA_PLATFORM"] = "offscreen"
