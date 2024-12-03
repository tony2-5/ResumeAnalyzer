import requests
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('HUGGING_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": f'Bearer {SECRET_KEY}'}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
	"question": "What is my name?",
	"context": "My name is Clara and I live in Berkeley."
},
})
print(output)