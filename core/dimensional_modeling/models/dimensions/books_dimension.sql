WITH base AS (
    SELECT
        title,
        description,
        price,
        contributor,
        contributor_note,
        age_group,
        book_review_link,
        amazon_product_url,
        first_chapter_link,
        ROW_NUMBER() OVER (PARTITION BY title ORDER BY LENGTH(description) DESC) as rn
    FROM {{ source("nyt_books_data", "nyt_books__lists__books") }}
    WHERE title IS NOT NULL
),
distinct_books AS (
	SELECT
	    title,
	    description,
	    price,
	    contributor,
	    contributor_note,
	    age_group,
	    book_review_link,
	    amazon_product_url,
	    first_chapter_link
	FROM base
	WHERE rn = 1
	ORDER BY title
),
base_model AS (
SELECT
	ROW_NUMBER() OVER (ORDER BY title) AS id,
	title,
    description,
    price,
    contributor,
    contributor_note,
    age_group,
    book_review_link,
    amazon_product_url,
    first_chapter_link
FROM distinct_books
)
SELECT
	DISTINCT id,
	title,
    description,
    price,
    contributor,
    contributor_note,
    age_group,
    book_review_link,
    amazon_product_url,
    first_chapter_link
 FROM base_model
 ORDER BY id