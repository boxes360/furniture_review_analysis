import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def export_random_sample():
    print("Извлекаем 200 случайных отзывов из базы...")

    query = """
    SELECT id, company_name, review_rating, review_text 
    FROM raw_reviews 
    ORDER BY RANDOM() 
    LIMIT 200;
    """
    
    df_sample = pd.read_sql(query, engine)

    df_sample['Тональность отзыва (Позитив/Негатив/Нейтрально)'] = ''
    df_sample['Тип проблемы (Сервис/Качество/Иное/Нет)'] = ''
    df_sample['Скорость доставки (Быстрая/Медленная/Нет)'] = ''
    df_sample['Причина возврата/претензии (Несоответствие описанию/Брак/Другое/Нет возврата)'] = ''
    df_sample['Тип мебели (Мягкая/Корпусная/Нет)'] = ''
    
    # Сохраняем в Excel
    output_path = "data/raw/manual_labeling_sample.xlsx"
    df_sample.to_excel(output_path, index=False)
    print(f"Готово! Файл для разметки сохранен по пути: {output_path}")

if __name__ == "__main__":
    export_random_sample()
