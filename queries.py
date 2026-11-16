import os
from datetime import date

import django
from django.db import connection, reset_queries
from django.db.models import Avg, Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from library.models import Author, Book  # noqa: E402


def seed():
    Book.objects.all().delete()
    Author.objects.all().delete()
    a1 = Author.objects.create(name="Leo Tolstoy", country="Russia")
    a2 = Author.objects.create(name="Fyodor Dostoevsky", country="Russia")
    a3 = Author.objects.create(name="Jane Austen", country="UK")
    a4 = Author.objects.create(name="Mark Twain", country="USA")
    a5 = Author.objects.create(name="Agatha Christie", country="UK")
    Book.objects.bulk_create([
        Book(title="War and Peace", author=a1, pages=1225, published_date=date(1869, 1, 1), genre="Novel"),
        Book(title="Anna Karenina", author=a1, pages=864, published_date=date(1877, 1, 1), genre="Novel"),
        Book(title="Childhood", author=a1, pages=150, published_date=date(1852, 1, 1), genre="Novella"),
        Book(title="Crime and Punishment", author=a2, pages=671, published_date=date(1866, 1, 1), genre="Novel"),
        Book(title="The Idiot", author=a2, pages=640, published_date=date(1869, 1, 1), genre="Novel"),
        Book(title="Demons", author=a2, pages=768, published_date=date(1872, 1, 1), genre="Novel"),
        Book(title="Pride and Prejudice", author=a3, pages=432, published_date=date(1813, 1, 28), genre="Novel"),
        Book(title="Emma", author=a3, pages=474, published_date=date(1815, 12, 23), genre="Novel"),
        Book(title="Sense and Sensibility", author=a3, pages=360, published_date=date(1811, 10, 30), genre="Novel"),
        Book(title="Adventures of Huckleberry Finn", author=a4, pages=366, published_date=date(1884, 12, 10), genre="Novel"),
        Book(title="The Adventures of Tom Sawyer", author=a4, pages=274, published_date=date(1876, 6, 1), genre="Novel"),
        Book(title="A Connecticut Yankee in King Arthur's Court", author=a4, pages=480, published_date=date(1889, 1, 1), genre="Novel"),
        Book(title="Murder on the Orient Express", author=a5, pages=256, published_date=date(1934, 1, 1), genre="Detective"),
        Book(title="The Murder of Roger Ackroyd", author=a5, pages=312, published_date=date(1926, 6, 1), genre="Detective"),
        Book(title="Death on the Nile", author=a5, pages=288, published_date=date(1937, 11, 1), genre="Detective"),
        Book(title="And Then There Were None", author=a5, pages=272, published_date=date(1939, 11, 6), genre="Detective"),
        Book(title="The ABC Murders", author=a5, pages=256, published_date=date(1936, 1, 6), genre="Detective"),
        Book(title="Crooked House", author=a5, pages=211, published_date=date(1949, 3, 1), genre="Detective"),
        Book(title="Endless Night", author=a5, pages=224, published_date=date(1967, 10, 30), genre="Detective"),
        Book(title="Postern of Fate", author=a5, pages=310, published_date=date(1973, 10, 1), genre="Detective"),
    ])


def run_queries():
    print("1.", list(Author.objects.values_list("name", flat=True)))
    print("2.", Book.objects.count())
    print("3.", list(Book.objects.filter(pages__gt=500).values_list("title", flat=True)))  # gt
    print("4.", list(Book.objects.filter(title__icontains="murder").values_list("title", flat=True)))  # icontains
    print("5.", Book.objects.filter(genre__in=["Novel", "Detective"]).count())  # in
    print("6.", list(Book.objects.filter(pages__range=(300, 500)).values_list("title", flat=True)))  # range
    print("7.", list(Book.objects.filter(published_date__year=1869).values_list("title", flat=True)))  # year
    print("8.", list(Author.objects.filter(country="UK").values_list("name", flat=True)))
    print("9.", list(Book.objects.order_by("-pages")[:5].values_list("title", "pages")))
    print("10.", list(Book.objects.filter(author__name="Leo Tolstoy").values_list("title", flat=True)))


def report():
    for a in Author.objects.annotate(books_count=Count("books"), avg_pages=Avg("books__pages")).order_by("name"):
        print(f"{a.name}: count={a.books_count}, avg={round(a.avg_pages, 2) if a.avg_pages else None}")


def n_plus_one():
    reset_queries()
    books = list(Book.objects.all()[:20])
    for b in books:
        _ = b.author.name
    print("without select_related:", len(connection.queries))

    reset_queries()
    books = list(Book.objects.select_related("author").all()[:20])
    for b in books:
        _ = b.author.name
    print("with select_related:", len(connection.queries))
    for b in books:
        print(b.title, "-", b.author.name)


if __name__ == "__main__":
    seed()
    run_queries()
    report()
    n_plus_one()
