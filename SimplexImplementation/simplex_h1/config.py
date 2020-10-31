import logging
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
FORMAT = '[%(asctime)s] [%(module)s] [%(funcName)s:%(lineno)d] %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)
