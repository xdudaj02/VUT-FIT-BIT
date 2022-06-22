from django.contrib import admin
from .models import *


# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'born', 'died')
    list_filter = ('born', 'died')
    search_fields = ('name', 'surname')


def authors_list(obj):
    return ", ".join([a.name for a in obj.authors.all()])


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', authors_list, 'genre')
    list_filter = ('name', 'authors', 'genre')
    autocomplete_fields = ('authors',)


class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('username', 'level')
    list_filter = ('level',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'email', 'administrator')
    list_filter = ('administrator',)


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'street_name', 'street_no', 'city')
    list_filter = ('city',)


class DistributorAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email')
    list_filter = ('name',)


def titles_in_library_list(obj):
    return ", ".join([t for t in obj.title_in_library.all()])


def books_list(obj):
    return ", ".join([str(b.id) for b in obj.books.all()])


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'distributor', 'created', 'handled')
    list_filter = ('employee', 'distributor', 'handled', 'created')


class OrderTitleInLibraryAdmin(admin.ModelAdmin):
    list_display = ('order', 'title_in_library', 'count')
    list_filter = ('order', 'title_in_library', 'count')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('created', 'profile', 'title_in_library', 'book', 'ready')
    list_filter = ('created', 'profile', 'ready')


class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'returned', 'borrowed_from', 'borrowed_to', 'profile', 'created', 'collected', books_list)
    list_filter = ('borrowed_from', 'returned', 'borrowed_to', 'profile', 'created', 'collected')


class TitleInLibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'library', 'owned')
    list_filter = ('title', 'library', 'owned')


def votes_list(obj):
    return ", ".join([v.name for v in obj.votes.all()])


class TitleNotOwnedAdmin(admin.ModelAdmin):
    list_display = ('title_in_library', votes_list, 'vote_count')
    list_filter = ('title_in_library', 'votes', 'vote_count')


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_in_library', 'state')
    list_filter = ('title_in_library', 'state')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderTitleInLibrary, OrderTitleInLibraryAdmin)
admin.site.register(ProfileType, ProfileTypeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Borrowing, BorrowingAdmin)
admin.site.register(TitleInLibrary, TitleInLibraryAdmin)
admin.site.register(TitleNotOwned, TitleNotOwnedAdmin)
admin.site.register(Book, BookAdmin)
