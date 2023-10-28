from pymongo import MongoClient
import json

with open('config.json') as f:
    config = json.load(f)

CLUSTER = MongoClient(config['mongodb'])

DB = CLUSTER['hackathon']

USERS = DB['users']
TASK_QUEUE = DB['task_queue']

# List of google ids that are allowed to access the admin page
ADMINS = []

CAPITALONE_KEY = config['capitalone_key']
CAPITALONE_ENDPOINT = "https://sandbox.capitalone.co.uk/developer-services-platform-pr/api/data"

AUTH0_CLIENT_ID = config["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = config["AUTH0_CLIENT_SECRET"]
AUTH0_DOMAIN = config["AUTH0_DOMAIN"]

SECRET_KEY = config["secret_key"]

TASKS = [
    {
        "id": 1,
        "name": "Touch grass",
        "description": "Be a good gamer and go outside today and touch some grass.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 2,
        "name": "Drink water",
        "description": "Be a good gamer and drink some water.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 3,
        "name": "Eat a fruit",
        "description": "Be a good gamer and eat a fruit.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 4,
        "name": "Eat a vegetable",
        "description": "Be a good gamer and eat a vegetable.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 5,
        "name": "Do 10 pushups",
        "description": "Be a good gamer and do 10 pushups.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 6,
        "name": "Donate to the nhs",
        "description": "Be a good gamer and do 10 situps.",
        "type": "donation",
        "paid_total": 0, # This will be edited in the code
    },
    {
        "id": 7,
        "name": "Do 10 squats",
        "description": "Be a good gamer and do 10 squats.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 8,
        "name": "Do 10 jumping jacks",
        "description": "Be a good gamer and do 10 jumping jacks.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    },
    {
        "id": 9,
        "name": "Do 10 burpees",
        "description": "Be a good gamer and do 10 burpees.",
        "type": "image",
        "submitted": None, # This will be edited in the code
    }
]