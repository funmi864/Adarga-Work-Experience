#imports
from openai import OpenAI
client = OpenAI()

import pandas as pd

#SETUP OPENAI
# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Access environment variables as if they came from the actual environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


#function
def CallOpenAI(document, user_question):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Here is the data from the CSV file about sports: "+ document},
        {"role": "user", "content": user_question}
    ]
    )

    return completion.choices[0].message.content


def main():
    df = pd.read_csv('/Users/funmiadebiyi/Desktop/ds-funmi/results.csv')
    document = df.to_string()
    print("Hello! I can answer questions about the csv file! ")
    question = True
    while question is True:
        user_question = input("Question: ")
        response = CallOpenAI(document, user_question)
        print(response)
        another_question = input("Do you have another question?(y/n): ")
        if another_question.lower() == 'y':
            question = True
        else:
            question = False

#calls to main to test
main()