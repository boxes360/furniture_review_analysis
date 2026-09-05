import os
import time
import json
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Настройки API
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
API_KEY = os.getenv("YANDEX_API_KEY")

# Настройки БД
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def setup_database():
    queries = [
        "ALTER TABLE raw_reviews ADD COLUMN IF NOT EXISTS gpt_tonality TEXT;",
        "ALTER TABLE raw_reviews ADD COLUMN IF NOT EXISTS gpt_problem TEXT;",
        "ALTER TABLE raw_reviews ADD COLUMN IF NOT EXISTS gpt_delivery TEXT;",
        "ALTER TABLE raw_reviews ADD COLUMN IF NOT EXISTS gpt_return TEXT;",
        "ALTER TABLE raw_reviews ADD COLUMN IF NOT EXISTS gpt_furniture TEXT;"
    ]
    with engine.begin() as conn:
        for q in queries:
            conn.execute(text(q))
    print("Колонки в базе данных успешно подготовлены.")

def classify_review(text_content):
    """Отправляет запрос в Yandex GPT"""
    if pd.isna(text_content) or str(text_content).strip() == "":
        return None

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "x-folder-id": FOLDER_ID
    }
    
    system_prompt = """
    Ты аналитик. Классифицируй отзыв о мебельном магазине. Верни ответ СТРОГО в формате JSON.
    Ключи и допустимые значения:
    "Тональность": "Позитив", "Негатив", "Нейтрально"
    "Проблема": "Сервис", "Качество", "Иное", "Нет"
    "Доставка": "Быстрая", "Медленная", "Нет"
    "Возврат": "Несоответствие описанию", "Брак", "Другое", "Нет возврата"
    "Мебель": "Мягкая", "Корпусная", "Нет" (ОТВЕЧАЙ "Нет", ЕСЛИ ТИП МЕБЕЛИ НЕ УКАЗАН ПРЯМО. НЕ ВЫДУМЫВАЙ И НЕ КОМБИНИРУЙ КАТЕГОРИИ!)
    """
    
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.1, "maxTokens": "1000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": str(text_content)}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return None
            
        result_json = response.json()
        if 'result' not in result_json:
             return None
             
        result_text = result_json['result']['alternatives'][0]['message']['text']
        clean_json = result_text.replace('```json', '').replace('```', '').strip()
        
        parsed_data = json.loads(clean_json)
        
        if isinstance(parsed_data, dict):
            return parsed_data
        else:
            print("Сбой формата нейросети (вернула список). Пропускаем...")
            return None
            
    except Exception as e:
        return None

def process_unlabeled_reviews():
    setup_database()
    
    query_select = text("SELECT id, review_text FROM raw_reviews WHERE gpt_tonality IS NULL;")
    
    with engine.connect() as conn:
        unprocessed = conn.execute(query_select).fetchall()
        
    total_left = len(unprocessed)
    print(f"Осталось обработать отзывов: {total_left}")
    
    if total_left == 0:
        print("Вся база уже размечена!")
        return

    print("Начинаем массовую обработку...")

    for index, row in enumerate(unprocessed):
        row_id, review_text = row[0], row[1]
        
        gpt_answer = classify_review(review_text)
        
        if gpt_answer:
            update_query = text("""
                UPDATE raw_reviews 
                SET gpt_tonality = :tonality, 
                    gpt_problem = :problem, 
                    gpt_delivery = :delivery, 
                    gpt_return = :return_reason, 
                    gpt_furniture = :furniture
                WHERE id = :id
            """)
            
            with engine.begin() as conn:
                conn.execute(update_query, {
                    "tonality": gpt_answer.get('Тональность', ''),
                    "problem": gpt_answer.get('Проблема', ''),
                    "delivery": gpt_answer.get('Доставка', ''),
                    "return_reason": gpt_answer.get('Возврат', ''),
                    "furniture": gpt_answer.get('Мебель', ''),
                    "id": row_id
                })
                
        time.sleep(1.5)
        
        if (index + 1) % 50 == 0:
            print(f"Обработано {index + 1} из {total_left}...")

if __name__ == "__main__":
    process_unlabeled_reviews()
