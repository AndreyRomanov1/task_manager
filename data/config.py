import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    int(os.getenv("ADMIN_ID"))
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

DATABASE_USERNAME = str(os.getenv("DATABASE_USERNAME"))
DATABASE_PASSWORD = str(os.getenv("DATABASE_PASSWORD"))
DATABASE_HOST = str(os.getenv("DATABASE_HOST"))
DATABASE_NAME = str(os.getenv("DATABASE_NAME"))
