least_unique_book: str = """
SELECT
    f.list_id,
    COUNT(DISTINCT f.book_id) AS distinct_books_count
FROM nyt_books.main_models.best_sellers_facts AS f
JOIN nyt_books.main_models.dates_dimension AS d
    ON f.published_date_id = d.date_id
GROUP BY f.list_id
ORDER BY COUNT(DISTINCT f.book_id) ASC
LIMIT 3
"""

most_weeks_in_top_3: str = """
SELECT
    b.title,
    COUNT(*) AS weeks_in_top_3
FROM nyt_books.main_models.best_sellers_facts AS f
JOIN nyt_books.main_models.dates_dimension AS d
    ON f.published_date_id = d.date_id
JOIN nyt_books.main_models.books_dimension AS b
    ON f.book_id = b.id
WHERE f.rank <= 3
  AND d.year = 2022
GROUP BY b.title
ORDER BY weeks_in_top_3 DESC
LIMIT 1
"""

publishers_rank: str = """
WITH book_quarter_rank AS (
    SELECT
        f.book_id,
        p.publisher_name,
        d.quarter,
        d.year,
        MIN(f."rank") AS best_rank
    FROM nyt_books.main_models.best_sellers_facts AS f
    LEFT JOIN nyt_books.main_models.publishers_dimension  AS p
        ON f.publisher_id = p.id
    LEFT JOIN nyt_books.main_models.dates_dimension AS d
        ON f.published_date_id = d.date_id
    WHERE d."date" >= '2021-01-01' AND d."date" < '2024-01-01'
    GROUP BY f.book_id, p.publisher_name, d.quarter, d.year
),
book_quarter_rank_points AS (
    SELECT
        publisher_name,
        year,
        quarter,
        best_rank,
        CASE
            WHEN best_rank = 1 THEN 5
            WHEN best_rank = 2 THEN 4
            WHEN best_rank = 3 THEN 3
            WHEN best_rank = 4 THEN 2
            WHEN best_rank = 5 THEN 1
            ELSE 0
        END AS points
    FROM book_quarter_rank
),
best_publishers AS (
    SELECT
        publisher_name,
        year,
        quarter,
        SUM(points) AS total_points
    FROM book_quarter_rank_points
    GROUP BY publisher_name, year, quarter
    ORDER BY year ASC, quarter ASC, SUM(points) DESC
),
publishers_ranked AS (
    SELECT
        publisher_name,
        year,
        quarter,
        total_points,
        RANK() OVER(PARTITION BY year, quarter ORDER BY total_points DESC) AS publishers_rank
    FROM best_publishers
)
SELECT *
FROM publishers_ranked
WHERE publishers_rank <= 5
ORDER BY year ASC, quarter ASC, publishers_rank ASC
"""

scipts_dict: dict[str, str] = {
    "least_unique_book": least_unique_book,
    "most_weeks_in_top_3": most_weeks_in_top_3,
    "publishers_rank": publishers_rank
}
