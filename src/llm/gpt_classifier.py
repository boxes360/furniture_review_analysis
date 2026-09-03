import os
import pandas as pd
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
API_KEY = os.getenv("YANDEX_API_KEY")

def classify_review(text):
    # Предобработка: защита от пустых строк
    if pd.isna(text) or str(text).strip() == "":
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
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {"stream": False, "temperature": 0.1, "maxTokens": "1000"},
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": str(text)}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            return None

        result_json = response.json()
        if 'result' not in result_json:
             print(f"Неожиданный ответ от API: {result_json}")
             return None
             
        result_text = result_json['result']['alternatives'][0]['message']['text']
        clean_json = result_text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
        
    except json.JSONDecodeError:
        print(f"GPT вернул невалидный JSON: {result_text}")
        return None
    except Exception as e:
        print(f"Системная ошибка: {e}")
        return None

def process_sample():
    print("Чтение размеченных данных...")
    df = pd.read_excel("data/raw/manual_labeling_sample.xlsx")
    
    df_100 = df.head(100).copy()
    
    for col in ["Тональность", "Проблема", "Доставка", "Возврат", "Мебель"]:
        df_100[f'GPT_{col}'] = ''
        
    print("Отправка запросов в Yandex GPT (это займет пару минут)...")
    for index, row in df_100.iterrows():
        gpt_answer = classify_review(row['review_text'])
        
        if gpt_answer:
            df_100.at[index, 'GPT_Тональность'] = gpt_answer.get('Тональность', '')
            df_100.at[index, 'GPT_Проблема'] = gpt_answer.get('Проблема', '')
            df_100.at[index, 'GPT_Доставка'] = gpt_answer.get('Доставка', '')
            df_100.at[index, 'GPT_Возврат'] = gpt_answer.get('Возврат', '')
            df_100.at[index, 'GPT_Мебель'] = gpt_answer.get('Мебель', '')
            
        time.sleep(1.5)
        if (index + 1) % 10 == 0:
            print(f"Обработано {index + 1} из 100 отзывов...")
            
    output_path = "data/raw/gpt_labeled_sample.xlsx"
    df_100.to_excel(output_path, index=False)
    print(f"Успешно! Файл с ответами GPT сохранен: {output_path}")

if __name__ == "__main__":
    process_sample()
