import os
from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/api/v1"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week

env_file_name_dict = {
    "dev": ".dev.env",
    "docker": ".docker.env",
    "pre": ".pre.env"
}

env = os.getenv("ENV", "dev")

print("ENV: " + env)

if env == "test":
    load_dotenv(".test.env")
if env == "docker":
    load_dotenv(".docker.env")
else:
    load_dotenv(".env")

load_dotenv("env/" + env_file_name_dict[env])

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "Cobe")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "markqiu")
    MONGO_DB = os.getenv("MONGO_DB", "demo")

    MONGODB_URL = DatabaseURL(
        # f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
        f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)
    MONGO_DB = os.getenv("MONGO_DB", "demo")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")
AWS_ACL = "public-read"

SMTP_USERNAME= os.getenv("SMTP_USERNAME")
SMTP_PASSWORD= os.getenv("SMTP_PASSWORD")
SMTP_HOSTNAME= os.getenv("SMTP_HOSTNAME")
SMTP_PORT= os.getenv("SMTP_PORT")

MSG91_API_KEY = os.getenv("MSG91_API_KEY")

database_name = MONGO_DB

path_list = os.getcwd().split('/')
PROJECT_BASE_DIR = '/'.join(path_list[:path_list.index('fastapi-project') + 1])
