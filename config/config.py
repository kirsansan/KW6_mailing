import os
# install as python-dotenv
from dotenv import load_dotenv


load_dotenv()

DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
MY_EMAIL = os.getenv('MY_EMAIL')
MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')
MY_EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
MY_EMAIL_PORT = int(os.getenv('MY_EMAIL_PORT'))
if os.getenv('EMAIL_SENDING_SIMULATION_MODE') == 'False':
    EMAIL_SENDING_SIMULATION_MODE = False
else:
    EMAIL_SENDING_SIMULATION_MODE = True



DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

MAX_PRODUCTS_PER_PAGE = 3
THRESHOLD_VIEW_FOR_EMAIL = 10

