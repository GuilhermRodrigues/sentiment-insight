import requests
import sqlite3
import re

# Conecta ao banco de dados SQLite
conn = sqlite3.connect('reviews.db')
cursor = conn.cursor()

# Seleciona todos os textos da tabela
cursor.execute('SELECT id, review FROM sentic_reviews')
rows = cursor.fetchall()

# Define as URLs das rotas
urls = [
    'https://sentic.net/api/en/{key-polarity}?text={}',
    'https://sentic.net/api/en/{key-intensity}?text={}',
    'https://sentic.net/api/en/{key-emotion}?text={}'
]

def remove_after_bracket(text):
    return re.sub(r'\[.*', '', text)

# Percorre os textos da tabela e faz as chamadas para cada rota
for row in rows:
    id = row[0]
    review = row[1]

    # Chamada para a primeira URL
    polarity_classification = requests.get(urls[0].format(review)).text
    
    # Chamada para a segunda URL
    intensity_ranking = requests.get(urls[1].format(review))
    intensity_ranking_dao = int(intensity_ranking.text)
    
    # Chamada para a terceira URL
    emotion_recognition = requests.get(urls[2].format(review))
    emotion_recognition_dao = remove_after_bracket(emotion_recognition.text)
    
    # Atualiza a linha na tabela com os resultados
    cursor.execute('UPDATE sentic_reviews SET polarity_classification = ?, intensity_ranking = ?, emotion_recognition = ? WHERE id = ?', (polarity_classification, intensity_ranking_dao, emotion_recognition_dao, id))
    # Commit da transação
    conn.commit()

# Fecha a conexão com o banco de dados
conn.close()