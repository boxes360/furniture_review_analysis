UPDATE raw_reviews SET gpt_tonality = LOWER(TRIM(gpt_tonality));
UPDATE raw_reviews SET gpt_problem = LOWER(TRIM(gpt_problem));
UPDATE raw_reviews SET gpt_delivery = LOWER(TRIM(gpt_delivery));
UPDATE raw_reviews SET gpt_return = LOWER(TRIM(gpt_return));
UPDATE raw_reviews SET gpt_furniture = LOWER(TRIM(gpt_furniture));

UPDATE raw_reviews 
SET gpt_return = 'нет возврата' 
WHERE gpt_return = 'нет';

-- Тональность
UPDATE raw_reviews 
SET gpt_tonality = 'другое' 
WHERE gpt_tonality NOT IN ('позитив', 'негатив', 'нейтрально') 
   OR gpt_tonality IS NULL;

-- Проблема
UPDATE raw_reviews 
SET gpt_problem = 'другое' 
WHERE gpt_problem NOT IN ('сервис', 'качество', 'нет') 
   OR gpt_problem IS NULL;

-- Доставка
UPDATE raw_reviews 
SET gpt_delivery = 'другое' 
WHERE gpt_delivery NOT IN ('быстрая', 'медленная', 'нет') 
   OR gpt_delivery IS NULL;

-- Возврат
UPDATE raw_reviews 
SET gpt_return = 'другое' 
WHERE gpt_return NOT IN ('несоответствие описанию', 'брак', 'другое', 'нет возврата') 
   OR gpt_return IS NULL;

-- Мебель
UPDATE raw_reviews 
SET gpt_furniture = 'другое' 
WHERE gpt_furniture NOT IN ('мягкая', 'корпусная', 'нет') 
   OR gpt_furniture IS NULL;


ALTER TABLE raw_reviews 
ALTER COLUMN review_rating TYPE NUMERIC(3,1) 
USING NULLIF(REGEXP_REPLACE(review_rating, '[^\d.]', '', 'g'), '')::NUMERIC(3,1);


#Нормализация даты
UPDATE raw_reviews SET review_date = SPLIT_PART(review_date, ',', 1);

-- Шаг Б: Превращаем русские текстовые месяцы в числовой формат (DD.MM.YYYY)
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' января ', '.01.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' февраля ', '.02.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' марта ', '.03.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' апреля ', '.04.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' мая ', '.05.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' июня ', '.06.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' июля ', '.07.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' августа ', '.08.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' сентября ', '.09.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' октября ', '.10.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' ноября ', '.11.');
UPDATE raw_reviews SET review_date = REPLACE(LOWER(review_date), ' декабря ', '.12.');

Обнуляем неформат (например, "5 лет назад")
-- Относительное время нельзя точно привязать к конкретному дню календаря, 
-- поэтому такие строки мы делаем пустыми (NULL), чтобы они не ломали конвертацию.
UPDATE raw_reviews 
SET review_date = NULL 
WHERE review_date !~ '^\d{1,2}\.\d{2}\.\d{4}$';

ALTER TABLE raw_reviews 
ALTER COLUMN review_date TYPE DATE 
USING TO_DATE(review_date, 'DD.MM.YYYY');