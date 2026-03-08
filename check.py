import os
from dotenv import load_dotenv

load_dotenv()

nvidia_api_key = os.getenv("Nvd_API")
print("Loaded API:", nvidia_api_key)