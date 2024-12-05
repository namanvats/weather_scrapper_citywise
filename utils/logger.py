import logging


class ConsoleFilter(logging.Filter):
    """
    Custom filter to control what gets logged to the console.
    Only log messages with a specific condition.
    """

    def filter(self, record):
        # Example condition: Only log WARNING and ERROR to console
        return record.levelno >= logging.WARNING

def setup_logger(name, log_file, level=logging.INFO, console_output=True):
    """
    Set up a logger with the given name, log file, and log level.

    Args:
        name (str): The name of the logger.
        log_file (str): The path to the log file.
        level (int, optional): The log level (e.g. logging.INFO, logging.DEBUG). Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger.
    """
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

        # Optionally add a console handler with selective logging
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            # Add the custom filter for selective logging
            console_handler.addFilter(ConsoleFilter())
            
            logger.addHandler(console_handler)

    return logger
