import requests
from dotenv import load_dotenv
import os

load_dotenv('../../.env')
val = "Bearer "+ os.getenv('API_TOKEN_SS_2')
headers = {"Authorization": val}
model = "https://api-inference.huggingface.co/models/edumunozsala/bertin_base_sentiment_analysis_es"

def get_sentiment_analysis(text : str) -> int:
    """
    This function takes a text as input and returns 1 if the text is negative and 0 otherwise.
    
    Args:
        text (str): text to analyze
        
    Returns:
        int: 1 if the text is considered negative and 0 otherwise
    """
    payload = {"inputs": text}
    response = requests.post(model, headers=headers, json=payload)
    response = response.json()
    print(response)
    response = response[0]
    # get value of the response for the key "negative"
    labels = {element['label']: element['score'] for element in response}
    if labels['Negativo'] > 0.9:
        return 1
    else:
        return 0
    
def main():
    while True:
        text = input("Enter a text to analyze: ")
        if text == "exit":
            break
        else:
            response = get_sentiment_analysis(text)
            print(response)
            
if __name__ == "__main__":
    main()
