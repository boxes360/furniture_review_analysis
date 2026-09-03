import pandas as pd

def calculate_metrics():
    # Загружаем файл с результатами
    df = pd.read_excel("data/raw/gpt_labeled_sample.xlsx")
    
    # Пары колонок для сравнения
    pairs = [
        ('Тональность отзыва (Позитив/Негатив/Нейтрально)', 'GPT_Тональность'),
        ('Тип проблемы (Сервис/Качество/Иное/Нет)', 'GPT_Проблема'),
        ('Скорость доставки (Быстрая/Медленная/Нет)', 'GPT_Доставка'),
        ('Причина возврата/претензии (Несоответствие описанию/Брак/Другое/Нет возврата)', 'GPT_Возврат'),
        ('Тип мебели (Мягкая/Корпусная/Нет)', 'GPT_Мебель')
    ]
    
    print("=== Результаты проверки Yandex GPT ===\n")
    
    for manual_col, gpt_col in pairs:
        # Очищаем текст от лишних пробелов и переводим в нижний регистр
        clean_manual = df[manual_col].astype(str).str.strip().str.lower()
        clean_gpt = df[gpt_col].astype(str).str.strip().str.lower()
        
        # Считаем долю совпадений
        accuracy = (clean_manual == clean_gpt).mean() * 100
        print(f"Метрика для [{manual_col.split(' ')[0]}]: Accuracy = {accuracy:.1f}%")
        
        # Строим матрицу ошибок
        print("\nМатрица пересечений (Строки - ручная разметка, Столбцы - GPT):")
        matrix = pd.crosstab(
            clean_manual, 
            clean_gpt, 
            rownames=['Руками'], 
            colnames=['GPT'],
            margins=True
        )
        print(matrix)
        print("-" * 60 + "\n")

if __name__ == "__main__":
    calculate_metrics()
