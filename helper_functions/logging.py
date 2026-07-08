from utils.logger import get_logger

logger = get_logger(__name__)

def log_step(step_no: int, description: str):
    logger.info(f"[STEP {step_no}] {description}")

def log_pass(message: str):
    logger.info(f"✅ PASS - {message}")

def log_fail(message: str):
    logger.error(f"❌ FAIL - {message}")

def log_info(description: str):
    logger.info(description)

def log_debug(description: str):
    logger.debug(description)
