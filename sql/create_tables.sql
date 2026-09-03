CREATE TABLE IF NOT EXISTS raw_reviews (
id SERIAL PRIMARY KEY,
source VARCHAR(50),
company_name VARCHAR(255),
company_avg_rating VARCHAR(50),
company_rating_count VARCHAR(100),
address VARCHAR(255),
coordinates VARCHAR(255),
company_review_count VARCHAR(50),
author_name VARCHAR(255),
author_status VARCHAR(255),
review_rating VARCHAR(50),
review_date VARCHAR(100),
review_text TEXT,
likes VARCHAR(50),
dislikes VARCHAR(50)
);
