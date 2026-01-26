from dotenv import load_dotenv
import os
import wikirate4py

load_dotenv()

api_key = os.getenv("WIKIRATE_API_KEY")

api = wikirate4py.API(api_key)

company = api.get_company("Hess")
print("Hess Company info:",  company.json())