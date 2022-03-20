import os

from dotenv import load_dotenv
load_dotenv()

print(type(os.environ.get('EMAIL_ADDRESS')))
