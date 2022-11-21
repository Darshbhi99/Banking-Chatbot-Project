from config import app_config
from exception import SystemError
import sys

try:
    appdata = app_config()
    df = appdata.initialise_process()
    print(f'Data has been retrieved successfully in {appdata.path}')
except Exception as e:
    raise SystemError(e, sys)