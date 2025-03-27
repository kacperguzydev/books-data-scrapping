from scrape import get_links, get_data
from database import create_database, insert_book_data, print_books


def main():
    create_database()
    links = get_links()
    data = get_data(links)

    for book in data:
        insert_book_data(book['link'], book['name'], book['price'])

    print_books()


if __name__ == "__main__":
    main()