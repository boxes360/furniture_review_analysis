import pandas as pd

def test_real_hypotheses():
    # Загружаем 100 строк
    df = pd.read_excel("data/raw/gpt_labeled_sample.xlsx")
    
    # Приводим всё к нижнему регистру
    for col in ['GPT_Тональность', 'GPT_Проблема', 'GPT_Доставка', 'GPT_Возврат', 'GPT_Мебель']:
        df[col] = df[col].astype(str).str.strip().str.lower()
        
    print("Проверка гипотез на 100 отзывах\n")
    
    # Гипотеза 1
    print("1. Клиенты чаще оставляют негативные отзывы из-за уровня сервиса, а не из-за качества мебели:")
    negative_reviews = df[df['GPT_Тональность'] == 'негатив']
    h1 = negative_reviews['GPT_Проблема'].value_counts(normalize=True) * 100
    print(h1.round(1).astype(str) + " %")
    print("-" * 60)
    
    # Гипотеза 2
    print("2. Высокая скорость доставки значительно повышает вероятность получения положительной оценки:")
    fast_delivery = df[df['GPT_Доставка'] == 'быстрая']
    if not fast_delivery.empty:
        h2 = fast_delivery['GPT_Тональность'].value_counts(normalize=True) * 100
        print(h2.round(1).astype(str) + " %")
    else:
        print("В выборке нет отзывов с быстрой доставкой.")
    print("-" * 60)
    
    # Гипотеза 3
    print("3. Наиболее частая причина возвратов и претензий — несоответствие товара описанию:")
    returns = df[(df['GPT_Возврат'] != 'нет возврата') & (df['GPT_Возврат'] != 'nan') & (df['GPT_Возврат'] != 'нет')]
    if not returns.empty:
        h3 = returns['GPT_Возврат'].value_counts(normalize=True) * 100
        print(h3.round(1).astype(str) + " %")
    else:
        print("В тестовой выборке нет ни одного возврата для анализа.")
    print("-" * 60)
    
    # Гипотеза 4
    print("4. Покупатели мягкой мебели оставляют более длинные отзывы по сравнению с корпусной:")
    # Считаем длину каждого отзыва в символах
    df['Длина_отзыва'] = df['review_text'].astype(str).apply(len)
    # Выводим среднюю длину отзыва по категориям мебели
    h4 = df.groupby('GPT_Мебель')['Длина_отзыва'].mean()
    print("Средняя длина отзыва (в символах):")
    print(h4.round(0))
    print("-" * 60 + "\n")
    

if __name__ == "__main__":
    test_real_hypotheses()
