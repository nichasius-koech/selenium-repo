import logging

def setup_logger(log_level: int = logging.INFO) -> None:
    """Configure global logging."""

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] [%(name)s] - %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Reusable logger instance."""
    return logging.getLogger(name)
