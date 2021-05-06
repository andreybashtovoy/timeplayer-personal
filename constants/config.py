from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
API_PORT = env.str("API_PORT")

POSTGRES_URI = "postgresql://postgres:kpi@localhost:5432/time_player"
