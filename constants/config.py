from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
API_PORT = env.str("API_PORT")

DB_NAME = env.str("DB_NAME")
DB_LOGIN = env.str("DB_LOGIN")
DB_PASSWORD = env.str("DB_PASSWORD")

POSTGRES_URI = f"postgresql://{DB_LOGIN}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
