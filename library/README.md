# library-api
Simple REST API for getting and saving information about books from google API (https://www.googleapis.com/books/v1/).

# API endpoints
| Method    | Endpoint    | Information    |
| --------- | ----------- | -------------- |
| GET       | /books      | returns a list of all books in app database |
| GET       | /books?published_date={year} | returns a list of all books published in specified year|
| GET       | /books?sort={-/+}published_date | returns a list of all books in desc(-) or asc(+) order of publication date |
| GET       | /books?author={author_fullname} | returns a list of all books writen by author format of author name is eg. Jan+Kowalski|
| POST      | /db/        | request body must contain {"q": "word"}. It's populate app database with books from google api containing "word" in title |