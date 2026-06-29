from dotenv import load_dotenv
import os

class Secrets:

    NVIDIA_API_KEY = ""
    SERP_API_KEY = ""
    OXYLABS_API_UN = ""
    OXYLABS_API_PW = ""
    GEMINI_API_KEY = ""

    def __init__(self):
        load_dotenv()
        self.NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
        self.SERP_API_KEY = os.getenv("SERP_API_KEY")
        self.OXYLABS_API_UN = os.getenv("OXYLABS_API_UN")
        self.OXYLABS_API_PW = os.getenv("OXYLABS_API_PW")
        self.GEMINI_API_KEY = os.getenv("GEMINI_KEY")
