import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

print("Выгружаем данные из базы...")
df = pd.read_sql("SELECT * FROM raw_reviews", engine)

df['review_length'] = df['review_text'].fillna('').astype(str).apply(len)

if 'review_text' in df.columns:
    df = df.drop(columns=['review_text'])

file_name = "full_reviews_labeled.csv"
df.to_csv(file_name, index=False)
print(f"Файл {file_name} создан")
