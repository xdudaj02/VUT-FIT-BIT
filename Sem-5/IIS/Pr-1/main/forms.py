from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


# Form used for user login
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput()}
        fields = ['username', 'password']


# Form used for registration of users of any type
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Name', required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


# Form used for editing the profile of users of any type
class ProfileEditForm(UserChangeForm):
    password = None
    first_name = forms.CharField(label='Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'first_name': forms.TextInput(),
            'password': forms.HiddenInput()
        }


# Form used for adding a new title to the database
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'


# Form used for inputting search criteria when filtering titles
class TitleSearchForm(forms.ModelForm):
    name = forms.CharField(required=False)
    author = forms.CharField(required=False)

    genre_choices = Genre.objects.all().order_by('name')
    genre = forms.ModelChoiceField(genre_choices, required=False)

    class Meta:
        model = Title
        fields = ['name', 'author', 'genre']


# Form used for adding a new author to the database
class AuthorForm(forms.ModelForm):
    born = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    died = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Author
        fields = '__all__'


# Form used for adding a new genre to the database
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


# Form used for adding a new library to the database
class LibraryForm(forms.ModelForm):
    opening_monday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    closing_monday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    opening_tuesday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    closing_tuesday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    opening_wednesday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    closing_wednesday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    opening_thursday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    closing_thursday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    opening_friday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))
    closing_friday = forms.TimeField(widget=forms.TimeInput(attrs={'placeholder': 'hh:mm'}))

    class Meta:
        model = Library
        fields = '__all__'


# Form used for creating a new order
class OrderForm(forms.ModelForm):
    library_choices = Library.objects.all().order_by('name')
    library = forms.ModelChoiceField(library_choices)

    title_choices = Title.objects.all().order_by('name')
    title = forms.ModelChoiceField(title_choices)

    count = forms.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = ['distributor', 'library', 'title', 'count']


# Form used for creating a new borrowing
class BorrowingForm(forms.ModelForm):
    user_choices = Profile.objects.all().order_by('username')
    user = forms.ModelChoiceField(user_choices)

    book_choices = Book.objects.filter(state=0).all().order_by('id')
    book = forms.ModelChoiceField(book_choices)

    days = forms.IntegerField(min_value=7, max_value=60, initial=30)

    class Meta:
        model = Borrowing
        fields = ['user', 'days', 'book']


# Form used for creating a new borrowing
class ReservationForm(forms.ModelForm):
    user_choices = Profile.objects.all().order_by('username')
    user = forms.ModelChoiceField(user_choices)

    title_choices = Title.objects.all().order_by('name')
    title = forms.ModelChoiceField(title_choices)

    library_choices = Library.objects.all().order_by('name')
    library = forms.ModelChoiceField(library_choices)

    class Meta:
        model = Borrowing
        fields = ['user', 'title', 'library']


# Form used for inputting search criteria when filtering borrowings
class BorrowingSearchForm(forms.ModelForm):
    user_choices = Profile.objects.all().order_by('username')
    user = forms.ModelChoiceField(user_choices, required=False)

    employee_choices = Employee.objects.all().order_by('username')
    created = forms.ModelChoiceField(employee_choices, required=False)

    state = forms.ChoiceField(choices=(('any', 'any'), ('active', 'active'), ('returned', 'returned')), required=False)

    borrowing_start_after = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)
    borrowing_start_before = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)

    borrowing_end_after = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)
    borrowing_end_before = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)

    class Meta:
        model = Borrowing
        fields = ['user', 'created', 'state', 'borrowing_start_after', 'borrowing_start_before', 'borrowing_end_after', 'borrowing_end_before']


# Form used for inputting search criteria when filtering reservations
class ReservationSearchForm(forms.ModelForm):
    user_choices = Profile.objects.all().order_by('username')
    user = forms.ModelChoiceField(user_choices, required=False)

    state = forms.ChoiceField(choices=(('any', 'any'), ('ready', 'ready'), ('waiting', 'waiting')), required=False)

    created_after = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)
    created_before = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)

    class Meta:
        model = Reservation
        fields = ['user', 'state', 'created_after', 'created_before']


# Form used for inputting search criteria when filtering orders
class OrderSearchForm(forms.ModelForm):
    employee_choices = Employee.objects.all().order_by('username')
    employee = forms.ModelChoiceField(employee_choices, required=False)

    distributor_choices = Distributor.objects.all().order_by('username')
    distributor = forms.ModelChoiceField(distributor_choices, required=False)

    state = forms.ChoiceField(choices=(('any', 'any'), ('handled', 'handled'), ('unhandled', 'unhandled')), required=False)

    created_after = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)
    created_before = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}), required=False)

    class Meta:
        model = Order
        fields = ['employee', 'distributor', 'state', 'created_after', 'created_before']
