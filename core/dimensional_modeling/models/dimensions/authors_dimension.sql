WITH distinct_authors AS (
    SELECT DISTINCT author
    FROM {{ source("nyt_books_data", "nyt_books__lists__books") }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY author) AS id,
    author AS name
FROM distinct_authors