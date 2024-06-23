WITH distinct_publishers AS (
    SELECT DISTINCT publisher AS publisher_name
    FROM {{ source("nyt_books_data", "nyt_books__lists__books") }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY publisher_name) AS id,
    publisher_name
FROM distinct_publishers
