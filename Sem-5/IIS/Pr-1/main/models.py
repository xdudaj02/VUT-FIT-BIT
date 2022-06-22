from django.db import models
from django.contrib.auth.models import User


# Class representing a genre
class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Class representing an author
class Author(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name + " " + self.surname


# Class representing a title
class Title(models.Model):
    isbn = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, db_table='title_author')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Class that exists simultaneously with the User class and is used to determine the level of the user that is logged in
class ProfileType(models.Model):
    username = models.CharField(max_length=150, unique=True)
    level = models.PositiveSmallIntegerField()

    def __str__(self):
        type_dict = {0: 'user', 1: 'distributor', 2: 'employee', 3: 'administrator'}
        return type_dict[self.level]


# Class representing a basic user
class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


# Class representing a library
class Library(models.Model):
    name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    street_no = models.PositiveSmallIntegerField(null=True)
    city = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    opening_monday = models.TimeField()
    closing_monday = models.TimeField()
    opening_tuesday = models.TimeField()
    closing_tuesday = models.TimeField()
    opening_wednesday = models.TimeField()
    closing_wednesday = models.TimeField()
    opening_thursday = models.TimeField()
    closing_thursday = models.TimeField()
    opening_friday = models.TimeField()
    closing_friday = models.TimeField()

    def __str__(self):
        return self.name


# Class representing a title in a certain library (exists for each title in each library)
class TitleInLibrary(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    owned = models.BooleanField()

    def __str__(self):
        return self.title.name + " in " + self.library.name


# Class representing a title that is not purchased in a given library
class TitleNotOwned(models.Model):
    title_in_library = models.OneToOneField(TitleInLibrary, on_delete=models.CASCADE)
    votes = models.ManyToManyField(Profile, db_table='votes', blank=True)
    vote_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title_in_library.title.name + " - not owned in " + self.title_in_library.library.name + " (" + str(
            self.votes) + " votes)"


# Class representing an actual book
class Book(models.Model):
    title_in_library = models.ForeignKey(TitleInLibrary, on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        state_dict = {0: 'available', 1: 'borrowed', 2: 'reserved'}
        return str(
            self.id) + " (" + self.title_in_library.title.name + ", " + self.title_in_library.library.name + ", " + \
               state_dict[self.state] + ")"


# Class representing an employee (type of a user)
class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    administrator = models.BooleanField()

    def __str__(self):
        return self.name


# Class representing a distributor (type of a user)
class Distributor(models.Model):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


# Class representing an order
class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, db_table='ordered_books')
    created = models.DateTimeField()
    finished = models.BooleanField(default=False)
    handled = models.BooleanField(default=False)

    def __str__(self):
        delivered_dict = {True: 'delivered', False: 'pending'}
        return "order " + str(self.id) + " (" + str(self.distributor) + ", " + delivered_dict[self.handled] + ")"


# Class representing a title in a certain library contained in an order (main use is storing the amount)
class OrderTitleInLibrary(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title_in_library = models.ForeignKey(TitleInLibrary, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)


# Class representing a reservation
class Reservation(models.Model):
    created = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title_in_library = models.ForeignKey(TitleInLibrary, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return self.title_in_library.title.name + ", " + self.profile.name + " (" + str(self.ready) + ")"


# Class representing a borrowing
class Borrowing(models.Model):
    borrowed_from = models.DateField()
    borrowed_to = models.DateField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created')
    collected = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='collected')
    books = models.ManyToManyField(Book, db_table='borrowed_books')
    finished = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    def __str__(self):
        returned_dict = {True: 'returned', False: 'active'}
        return "borrowing " + str(self.id) + " (" + str(self.profile) + ", " + str(self.created) + ", " + returned_dict[
            self.returned] + ")"
