import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def load_all_files():
    files_info = {
        "data/raw/reviews_2gis.xlsx": "2gis",
        "data/raw/reviews_yandex.xlsx": "yandex",
        "data/raw/reviews_google.xlsx": "google"
    }
    
    all_dataframes = []
    
    for file_path, source_name in files_info.items():
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        df['source'] = source_name 
        all_dataframes.append(df)
        
    # Объединяем все три датафрейма в один
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    combined_df = combined_df.rename(columns={
        'Наименование': 'company_name',
        'Оценка': 'company_avg_rating',
        'Количество оценок': 'company_rating_count',
        'Адрес': 'address',
        'Координаты объекта': 'coordinates',
        'Количество отзывов': 'company_review_count',
        'Автор': 'author_name',
        'Статус автора': 'author_status',
        'Оценка автора': 'review_rating',
        'Дата': 'review_date',
        'Текст': 'review_text',
        'Like': 'likes',
        'Dislike': 'dislikes'
    })
    
    print(f"Всего собрано {len(combined_df)} строк. Загружаем в базу PostgreSQL...")
    
    # Загружаем в БД
    combined_df.to_sql('raw_reviews', engine, if_exists='append', index=False)
    print("Данные успешно загружены!")

if __name__ == "__main__":
    load_all_files()
