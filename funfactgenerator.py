import json
import requests
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

def get_fun_fact():
    clear()
    # Fetch a random fun fact from the API
    response=requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    if response.status_code == 200:
        data=response.json()
        fact=data.get("text")
        put_text(f"Fun Fact: {fact}")
    else:
        put_text("Failed to fetch a fun fact. Please try again later.")



get_fun_fact()