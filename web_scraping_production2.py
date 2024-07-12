#imports
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

from openai import OpenAI

import csv

from transformers import pipeline ##


#SETUP OPENAI
# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# create pipeline for NER
ner_pipeline = pipeline('ner', aggregation_strategy="simple") ##

#functions

def fetch_and_store_text(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.get_text()
    return text

def CallOpenAI(document, prompt):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Document text: "+ document},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content

def read_prompts():
    path = "/Users/funmiadebiyi/Desktop/ds-funmi/Prompts/prompts.txt"
    f = open(path, "r")
    prompts = f.readlines()
    return prompts

def clean_response(response):
    SplitResponse = response.split(":")
    if len(SplitResponse) < 2:
        raise ValueError("Response does not contain a ':' ")
    cleaned_response = SplitResponse[1].replace("\n", ", ").replace("- ", "")
    return SplitResponse[0], cleaned_response

def extract_entities(text): ##
    entities = ner_pipeline(text) ##
    return entities ##

field_names = ["URL", "Title", "Publication Date", "Author", "Topic", "Entities", "Event", "Quotes", "Stats", "Tone"]

csv_filename = '/Users/funmiadebiyi/Desktop/ds-funmi/results.csv'
def write_row(Prompt_Answers, csv_filename):
    with open(csv_filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = field_names)
        writer.writerow(Prompt_Answers)






def main(URL):
    #Takes URL
    #Scrapes text of website
    # Cleans text
    # Extracts information with LLM
    #Processes LLM Response
    #Stores result in csv
    prompts = read_prompts()
    text = fetch_and_store_text(URL)

    entities = extract_entities(text)
    entity_names = [entity['word'] for entity in entities]

    # Print entities to see the output
    print("Extracted Entities:", entity_names)

    Prompt_Answers = {}

    Prompt_Answers ["URL"] = URL
    Prompt_Answers["Entities"] = ', '.join(entity_names)
    
    for prompt in tqdm(prompts): 
        Key_People = CallOpenAI(text, prompt)
        cleaned_key, cleaned_value = clean_response(Key_People)
        Prompt_Answers[cleaned_key] = cleaned_value

    #write_row(Prompt_Answers, csv_filename)

    #Returns true if successful
    return True

#calls to main to test
if __name__ == "__main__":
    while True:
        try:
            NoOfTimes = int(input("How many URLS are you inputting?: "))
            if NoOfTimes <= 0:
                raise Exception()
        except ValueError:
            print("NoOfTimes has to be an integer") 
        except Exception:
            print("NoOfTimes has to be a positive integer")
        
        else:   
            for i in range(NoOfTimes):
                URL = input("Enter URL: ")
                fetch_and_store_text(URL)
                main(URL)
            break