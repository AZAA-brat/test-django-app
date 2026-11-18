from django.contrib import admin
from .models import Author, Book

admin.site.site_header = "Book shop"
admin.site.site_title = "Admin panel of Book shop"
admin.site.index_title = "Book management"

class AuthorInline(admin.TabularInline):
    model = Author
    extra = 1
    fields = ("name", "country")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("name", "country")
    search_fields = ("name", "country")
    list_per_page = 50

class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ("title", "author", "pages", "published_date", "genre", "in_stock")

@admin.action(description="Remove a book")
def make_unavailable(modeladmin, request, queryset):
    count = queryset.update(in_stock=False)
    modeladmin.message_user(
        request, f"Removed from selling: {count}")

@admin.action(description="Add a book")
def make_available(modeladmin, request, queryset):
    count = queryset.update(in_stock=True)
    modeladmin.message_user(
        request, f"Added for selling: {count}")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "pages", "published_date", "genre", "in_stock")
    list_filter = ("author", "genre", "published_date", "in_stock")
    search_fields = ("title", "author", "pages", "published_date", "genre")
    list_per_page = 25
    readonly_fields = ("published_date", "author", "genre", "in_stock")
    actions = [make_unavailable, make_available]

