from dotenv import dotenv_values, load_dotenv
import os
load_dotenv()

print(os.getenv('MY_KEY'))
print(os.getenv('API_KEY'))
