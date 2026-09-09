import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
import warnings

# Отключаем предупреждения sklearn для классов с нулем примеров
warnings.filterwarnings('ignore')

def calculate_metrics():
    # Загружаем файл с результатами (оставил твой путь к файлу)
    df = pd.read_excel("data/raw/gpt_labeled_sample.xlsx")
    
    # Пары колонок для сравнения
    pairs = [
        ('Тональность отзыва (Позитив/Негатив/Нейтрально)', 'GPT_Тональность'),
        ('Тип проблемы (Сервис/Качество/Иное/Нет)', 'GPT_Проблема'),
        ('Скорость доставки (Быстрая/Медленная/Нет)', 'GPT_Доставка'),
        ('Причина возврата/претензии (Несоответствие описанию/Брак/Другое/Нет возврата)', 'GPT_Возврат'),
        ('Тип мебели (Мягкая/Корпусная/Нет)', 'GPT_Мебель')
    ]
    
    print("=== Расчет метрик запущен ===\n")
    
    # Открываем файл для записи отчета
    with open("metrics_report.txt", "w", encoding="utf-8") as f:
        f.write("=== Результаты проверки Yandex GPT ===\n\n")
        
        for manual_col, gpt_col in pairs:
            # Очищаем текст ручной разметки
            clean_manual = df[manual_col].astype(str).str.strip().str.lower()
            
            # Очищаем текст GPT и ИСПРАВЛЯЕМ БАГ с "нет возврата", как просил наставник
            clean_gpt = df[gpt_col].astype(str).str.strip().str.lower()
            if gpt_col == 'GPT_Возврат':
                clean_gpt = clean_gpt.replace('нет', 'нет возврата')
            
            # 1. Считаем долю самого частого класса (Baseline)
            baseline = clean_manual.value_counts(normalize=True).max() * 100
            
            # 2. Считаем общую точность (Accuracy)
            accuracy = accuracy_score(clean_manual, clean_gpt) * 100
            
            # Формируем заголовок и базовые метрики
            category_name = manual_col.split(' ')[0]
            output_str = f"--- Анализ категории: [{category_name}] ---\n"
            output_str += f"Доля самого частого класса (Baseline): {baseline:.1f}%\n"
            output_str += f"Общая точность модели (Accuracy):      {accuracy:.1f}%\n\n"
            
            # 3. Формируем подробный отчет (Precision, Recall, F1)
            output_str += "Подробный отчет по каждому классу:\n"
            report = classification_report(clean_manual, clean_gpt)
            output_str += report + "\n"
            output_str += "-" * 60 + "\n\n"
            
            # Выводим на экран и сразу пишем в файл
            print(output_str)
            f.write(output_str)

    print("Готово! Результаты успешно сохранены в файл: metrics_report.txt")

if __name__ == "__main__":
    calculate_metrics()