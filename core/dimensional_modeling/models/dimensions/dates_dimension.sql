WITH date_generator_cte AS (
  SELECT 
    (generate_series)::DATE AS date_field
  FROM 
    generate_series('2020-11-01'::DATE, '2024-02-28'::DATE, INTERVAL 1 DAY) AS t(generate_series)
)
SELECT 
  ROW_NUMBER() OVER (ORDER BY date_field) AS date_id,
  date_field AS date,
  EXTRACT(YEAR FROM date_field) AS year,
  EXTRACT(MONTH FROM date_field) AS month,
  EXTRACT(DAY FROM date_field) AS day,
  EXTRACT(DAYOFWEEK FROM date_field) AS day_of_week,
  EXTRACT(QUARTER FROM date_field) AS quarter
FROM 
  date_generator_cte
