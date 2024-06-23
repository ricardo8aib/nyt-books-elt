SELECT
	ROW_NUMBER() OVER () AS id,
	published_date_ids.date_id as published_date_id,
	previous_published_date_ids.date_id as previous_published_date_id,
	next_published_date_ids.date_id as next_published_date_id,
	books.id  as book_id,
	lists.list_id ,
	authors.id as author_id,
	publishers.id as publisher_id,
	base."rank",
	base.rank_last_week,
	base.weeks_on_list
FROM {{ source("nyt_books_data", "nyt_books__lists__books") }} AS base
LEFT JOIN {{ ref("publishers_dimension") }} AS publishers
	ON publishers.publisher_name = base.publisher
LEFT JOIN {{ ref("authors_dimension") }} AS authors
	ON authors.name = base.author
LEFT JOIN {{ source("nyt_books_data", "nyt_books__lists") }} AS lists
	ON base."_dlt_parent_id" = lists."_dlt_id"
LEFT JOIN {{ ref("books_dimension") }} AS books
	ON base.title = books.title 
LEFT JOIN {{ source("nyt_books_data", "nyt_books") }} AS books_dates
	ON books_dates."_dlt_id" = lists."_dlt_parent_id"
LEFT JOIN {{ ref("dates_dimension") }} AS published_date_ids
	ON books_dates.published_date = published_date_ids."date"
LEFT JOIN {{ ref("dates_dimension") }} AS previous_published_date_ids
	ON books_dates.previous_published_date = previous_published_date_ids."date"
LEFT JOIN {{ ref("dates_dimension") }} AS next_published_date_ids
	ON books_dates.next_published_date  = next_published_date_ids."date" 