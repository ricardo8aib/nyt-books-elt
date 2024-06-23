WITH distinct_lists AS (
    SELECT 
        list_id AS id,
        list_name,
        display_name,
        updated
    FROM {{ source("nyt_books_data", "nyt_books__lists") }}
    WHERE list_id IS NOT NULL
)

SELECT
    DISTINCT id,
    list_name,
    display_name,
    updated
FROM distinct_lists
ORDER BY id
