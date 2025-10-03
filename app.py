import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

exec(open('webui/NanoTik.py', encoding='utf-8').read())
