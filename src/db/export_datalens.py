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

def export_for_datalens():
    print("Выгружаем данные для DataLens...")
    query = "SELECT * FROM raw_reviews;"
    df = pd.read_sql(query, engine)
    
    output_path = "data/raw/datalens_export.csv"
    
    df.to_csv(output_path, index=False)
    print(f"Успешно! Файл сохранен: {output_path}")

if __name__ == "__main__":
    export_for_datalens()
