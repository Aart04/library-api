import requests


def get_book_data(q):
    url = "https://www.googleapis.com/books/v1/volumes?q={}".format(q)
    response = requests.get(url=url)
    response_json = response.json()

    return response_json
