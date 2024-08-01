from pathlib import Path

from dataclasses import dataclass
import yaml

@dataclass
class Paths:
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    SECRETS_PATH: Path = BASE_DIR.joinpath("app", "secrets.yml")

with open(Paths.SECRETS_PATH, "r", encoding="utf-8") as file:
    SECRETS = yaml.safe_load(file)

@dataclass(frozen=True)
class ElasticsearchConfig:
    INDEX_NAME = SECRETS["ELASTICSEARCH"]["PROD_INDEX_NAME"]
    ES_CLOUD_ID = SECRETS["ELASTICSEARCH"]["CLOUD_ID"]
    ES_USER = SECRETS["ELASTICSEARCH"]["USER"]
    ES_PASSWORD = SECRETS["ELASTICSEARCH"]["PASSWORD"]