import logging

# Create a logger object
logger = logging.getLogger(__name__)

# Set the log level for the logger
logger.setLevel(logging.DEBUG)  # This should capture all levels including ERROR

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app_logs.log", mode="a", encoding="utf-8")

# Create a formatter and set it for the handlers
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Set log level for the handlers
console_handler.setLevel(logging.DEBUG)  # This should capture DEBUG and above
file_handler.setLevel(logging.DEBUG)  # This should capture DEBUG and above

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Optional: Add a filter to show only DEBUG messages in the console
def show_only_debug(record):
    return record.levelname == "DEBUG"

console_handler.addFilter(show_only_debug)
