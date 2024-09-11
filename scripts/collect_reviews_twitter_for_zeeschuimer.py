import json
import re
import insert_table_sentic_reviews as insert

def get_reviews(file_path):
    full_texts = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    full_text = data.get('data', {}).get('legacy', {}).get('full_text')
                    if full_text:
                        full_texts.append(full_text)
                except json.JSONDecodeError:
                    print(f"Erro de decodificação JSON para a linha: {line}")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
    return full_texts

def clean_review(review):
    cleaned_text = re.sub(r'#\w+\s*', '', review)  # Remove as hashtags e o texto após elas
    cleaned_text = re.sub('[^A-Za-z ]+', ' ', cleaned_text.lower())  # Remove caracteres especiais e converte para minúsculas
    return cleaned_text.strip()

def has_single_review(review):
    review = review.strip()
    return ' ' not in review

reviews = get_reviews('data_collect_twitter.ndjson')

if reviews is not None:
    for review in reviews:
        review_formatted = clean_review(review)
        if  has_single_review:
            insert.creating_reviews(review_formatted)
        print("Review:", review_formatted)