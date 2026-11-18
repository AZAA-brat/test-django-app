from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books"
    )
    pages = models.IntegerField()
    published_date = models.DateField()
    genre = models.CharField(max_length=100, blank=True)
    in_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"