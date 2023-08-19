import os
# install as python-dotenv
from dotenv import load_dotenv


load_dotenv()

DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
MY_EMAIL_PASSWORD = os.getenv('MY_EMAIL_PASSWORD')
DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

MAX_PRODUCTS_PER_PAGE = 3
THRESHOLD_VIEW_FOR_EMAIL = 10

EMAIL_SENDING_SIMULATION_MODE = True

