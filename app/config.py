import os
import json
from dotenv import load_dotenv


load_dotenv()

EXEMPT_TOKENS = os.getenv('EXEMPT_TOKENS').split(',')
TOKENS = json.loads(os.getenv('TOKENS'))
apitally_id = os.getenv('apitally_id')
default_limit = '2/minute'
