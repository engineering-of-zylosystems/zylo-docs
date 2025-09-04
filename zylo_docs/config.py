import os
from dotenv import load_dotenv

# config.py 파일의 위치를 기준으로 상위 폴더의 .env 파일을 찾습니다.
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

EXTERNAL_API_BASE = os.getenv("EXTERNAL_API_BASE", "https://v2-api.zylosystems.com/v1")
