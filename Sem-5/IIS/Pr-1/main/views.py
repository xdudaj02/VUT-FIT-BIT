from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from datetime import datetime, timedelta


# View for html error 400
def error400(request, exception):
    return render(request, 'main/400.html', status=400)


# View for html error 404
def error404(request, exception):
    return render(request, 'main/404.html', status=404)


# View for html error 500
def error500(request):
    return redirect('home')


# View for home page
def home(request):
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    next_borrowing = None
    reservation_ready_count = None
    # for regular users calculate and display number of waiting reservations and next borrowing deadline
    if level == 0:
        next_borrowing = Borrowing.objects.filter(profile__username__exact=request.user.username,
                                                  returned=False).order_by('borrowed_to').first()
        reservation_list_var = Reservation.objects.filter(profile__username__exact=request.user.username).all()
        reservation_ready_count = sum([1 for i in reservation_list_var if (i.book is not None)])

    return render(request, 'main/home.html', {'level': level, 'next_borrowing': next_borrowing,
                                              'reservation_ready_count': reservation_ready_count})


# View for login page
def log_in(request):
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    login_form = LoginForm

    # tries to login a user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials. Try again.')

    return render(request, 'main/login.html', {'login_form': login_form, 'level': level})


# View for logout - redirects to home
def log_out(request):
    # tries to logout a user
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')


# View for register page
def register(request):
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    register_form = RegisterForm

    # tries to register a user
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if not Profile.objects.filter(email__exact=request.POST.get('email')).exists():
                register_form.save()
                user_var = Profile.objects.create(username=request.POST.get('username'),
                                                  name=request.POST.get('first_name'), email=request.POST.get('email'))
                ProfileType.objects.create(username=request.POST.get('username'), level=0)
                if level == 3:
                    return redirect('user_detail', user_id=user_var.id)
                else:
                    return redirect('login')
            else:
                messages.info(request, 'An account with this email address already exists.')

    return render(request, 'main/register.html', {'register_form': register_form, 'level': level})


# View for genre list page
def genre_list(request):
    # displays list of all genres
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    genre_list_var = Genre.objects.all().order_by('name')

    return render(request, 'main/genre_list.html', {'genre_list': genre_list_var, 'level': level})


# View for genre detail page
def genre_detail(request, genre_id):
    # displays detail of genre with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    genre_detail_var = Genre.objects.filter(id=genre_id).first()
    if not genre_detail_var:
        return redirect('genre_list')

    return render(request, 'main/genre_detail.html', {'genre_detail': genre_detail_var, 'level': level})


# View for genre adding page
def genre_add(request):
    # tries to add a genre
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [1, 2, 3]:
        return redirect('home')

    # tries to get data from input form
    genre_form = GenreForm()
    if request.method == 'POST':
        genre_form = GenreForm(request.POST)
        if genre_form.is_valid():
            genre_var = genre_form.save()
            return redirect('genre_detail', genre_id=genre_var.id)

    return render(request, 'main/genre_add.html', {'genre_form': genre_form, 'level': level})


# View for author list page
def author_list(request):
    # displays list of all authors or authors that meet the search criteria (name, surname)
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    author_list_var = Author.objects.all().order_by('surname')

    # gets and applies search criteria
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        if surname or name:
            name = name if name != '' else '.*'
            surname = surname if surname != '' else '.*'
            author_list_var = Author.objects.filter(surname__iregex=surname, name__iregex=name).order_by('surname')

    return render(request, 'main/author_list.html', {'author_list': author_list_var, 'level': level})


# View for author detail page
def author_detail(request, author_id):
    # gets and displays detail of author with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    author_detail_var = Author.objects.filter(id=author_id).first()
    if not author_detail_var:
        return redirect('author_list')
    title_list_var = author_detail_var.title_set.all().order_by('name')

    return render(request, 'main/author_detail.html',
                  {'author_detail': author_detail_var, 'title_list': title_list_var, 'level': level})


# View for author adding page
def author_add(request):
    # tries to add an author
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [1, 2, 3]:
        return redirect('home')

    # tries to get data from input form
    author_add_form = AuthorForm()
    if request.method == 'POST':
        author_add_form = AuthorForm(request.POST)
        if author_add_form.is_valid():
            author = author_add_form.save()
            return redirect('author_detail', author_id=author.id)

    return render(request, 'main/author_add.html', {'author_form': author_add_form, 'level': level})


# View for author editing page
def author_edit(request, author_id):
    # tries to edit information about author with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [1, 2, 3]:
        return redirect('home')

    author_var = Author.objects.filter(id=author_id).first()
    if not author_var:
        redirect('author_list')
    author_add_form = AuthorForm(instance=author_var)

    # listens for actions: delete (deletes author) or input form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                title_list_var = Title.objects.filter(authors__in=[author_id])
                for i in title_list_var:
                    i.delete()
                author_var.delete()
                return redirect('author_list')
        else:
            author_add_form = AuthorForm(request.POST, instance=author_var)
            if author_add_form.is_valid():
                author_add_form.save()
                return redirect('author_detail', author_id=author_id)

    return render(request, 'main/author_edit.html', {'author_form': author_add_form, 'level': level})


# View for title list page
def title_list(request):
    # gets and displays list of all titles or those that meet given search criteria (name, author name, selected genre)
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    title_list_var = Title.objects.all().order_by('name')
    title_search_form = TitleSearchForm()

    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        genre_id = request.POST.get('genre')
        if author or name or genre_id:
            name_regex = name if name != '' else '.*'
            author_regex = author if author != '' else '.*'
            genre_regex = Genre.objects.get(id=genre_id).name if genre_id else '.*'
            title_list_var_1 = Title.objects.filter(name__iregex=name_regex, authors__surname__iregex=author_regex,
                                                    genre__name__iregex=genre_regex).order_by('name').distinct()
            title_list_var_2 = Title.objects.filter(name__iregex=name_regex, authors__name__iregex=author_regex,
                                                    genre__name__iregex=genre_regex).order_by('name').distinct()
            title_list_var = title_list_var_1 | title_list_var_2
        title_search_form = TitleSearchForm(initial={'name': name, 'author': author, 'genre': genre_id})

    return render(request, 'main/title_list.html',
                  {'title_form': title_search_form, 'title_list': title_list_var, 'level': level})


# View for title adding page
def title_add(request):
    # tries to add a new title
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [1, 2, 3]:
        return redirect('home')

    # listens for input form confirmation
    title_add_form = TitleForm()
    if request.method == 'POST':
        title_add_form = TitleForm(request.POST)
        if title_add_form.is_valid():
            title = title_add_form.save()
            libraries = Library.objects.all()
            for library in libraries:
                title_in_library = TitleInLibrary.objects.create(title=title, library=library, owned=False)
                TitleNotOwned.objects.create(title_in_library=title_in_library)
            return redirect('title_detail', title_isbn=title.isbn)

    return render(request, 'main/title_add.html', {'title_form': title_add_form, 'level': level})


# View for title editing page
def title_edit(request, title_isbn):
    # tries to edit title with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [1, 2, 3]:
        return redirect('home')

    title_var = Title.objects.filter(isbn=title_isbn).first()
    if not title_var:
        return redirect('title_list')
    title_add_form = TitleForm(instance=title_var)

    # listens for delete action (deletes this title) or input form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                title_var.delete()
                return redirect('title_list')
        else:
            title_add_form = TitleForm(request.POST, instance=title_var)
            if title_add_form.is_valid():
                title_add_form.save()
                return redirect('title_detail', title_isbn=title_isbn)

    return render(request, 'main/title_edit.html', {'title_form': title_add_form, 'level': level})


# View for title detail page
def title_detail(request, title_isbn):
    # displays detail of title with this isbn
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1

    # listens for actions
    if request.method == 'POST':
        # on set reservation makes a reservation for this title in library provided through post method data
        if request.POST.get('set_reservation') is not None:
            title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn,
                                                          library__id=request.POST.get('set_reservation'))
            profile_var = Profile.objects.filter(username__exact=request.user.username).first()
            free_book = Book.objects.filter(title_in_library__title__isbn=title_isbn,
                                            title_in_library__library_id=request.POST.get('set_reservation'),
                                            state=0).first()
            reservation = Reservation.objects.create(created=datetime.now(), profile=profile_var,
                                                     title_in_library=title_in_library, book=free_book)
            # if there is an available book - add it to reservation and mark as reserved
            if free_book is not None:
                reservation.book = free_book
                reservation.ready = True
                reservation.save()
                free_book.state = 1
                free_book.save()
            return redirect('title_detail', title_isbn=title_isbn)
        # on cancel reservation cancels a reservation for this title in library provided through post method data
        elif request.POST.get('cancel_reservation') is not None:
            title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn,
                                                          library__id=request.POST.get('cancel_reservation'))
            reservation = Reservation.objects.filter(profile__username=request.user.username,
                                                     title_in_library=title_in_library).first()
            # if reservation is tied to an actual book - "releases" it
            if reservation.book is not None:
                reservation.book.state = 0
                reservation.book.save()
            reservation.delete()
            return redirect('title_detail', title_isbn=title_isbn)
        # on set vote adds a vote for this title in library provided through post method data from this user
        elif request.POST.get('set_vote') is not None:
            title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn,
                                                          library__id=request.POST.get('set_vote'))
            profile_var = Profile.objects.filter(username__exact=request.user.username).first()
            title_in_library.titlenotowned.votes.add(profile_var)
            title_in_library.titlenotowned.vote_count += 1
            title_in_library.titlenotowned.save()
            return redirect('title_detail', title_isbn=title_isbn)
        # on cancel vote cancels the vote for this title in library provided through post method data from this user
        elif request.POST.get('cancel_vote') is not None:
            title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn,
                                                          library__id=request.POST.get('cancel_vote'))
            profile_var = Profile.objects.filter(username__exact=request.user.username).first()
            title_in_library.titlenotowned.votes.remove(profile_var)
            title_in_library.titlenotowned.vote_count -= 1
            title_in_library.titlenotowned.save()
            return redirect('title_detail', title_isbn=title_isbn)

    title_detail_var = Title.objects.filter(isbn=title_isbn).first()
    if not title_detail_var:
        return redirect('title_list')
    title_in_library_list_var = title_detail_var.titleinlibrary_set.all()
    availability_dict = {}
    voted = False
    reserved = False
    # calculates availability of this title in all libraries and checks for reservations and votes from this user
    for i in title_in_library_list_var:
        if i.owned:
            owned = len(i.book_set.all())
            available = sum([1 for j in i.book_set.all() if j.state == 0])
            if request.user.is_authenticated:
                reserved = i.reservation_set.filter(profile__username__exact=request.user.username).exists()
            availability_dict[i.library] = [owned, available, voted, reserved]
        else:
            if request.user.is_authenticated:
                voted = i.titlenotowned.votes.filter(username__exact=request.user.username).exists()
            availability_dict[i.library] = [0, 0, voted, reserved]

    return render(request, 'main/title_detail.html',
                  {'title_detail': title_detail_var, 'availability_dict': availability_dict, 'level': level})


# View for library list page
def library_list(request):
    # gets and displays a list of all libraries or those that meet given search criteria (name, city)
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    library_list_var = Library.objects.all().order_by('name')

    # listens for input form confirmation
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        if city or name:
            name = name if name != '' else '.*'
            city = city if city != '' else '.*'
            library_list_var = Library.objects.filter(city__iregex=city, name__iregex=name).order_by('name')

    return render(request, 'main/library_list.html', {'library_list': library_list_var, 'level': level})


# View for library detail page
def library_detail(request, library_id):
    # displays a detail of a library with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    library_detail_var = Library.objects.filter(id=library_id).first()
    if not library_detail_var:
        return redirect('library_list')

    return render(request, 'main/library_detail.html', {'library_detail': library_detail_var, 'level': level})


# View for library adding page
def library_add(request):
    # tries to add a new library specified by input form
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level != 3:
        return redirect('home')
    library_add_form = LibraryForm()

    # listens for input form confirmation
    if request.method == 'POST':
        library_add_form = LibraryForm(request.POST)
        if library_add_form.is_valid():
            library = library_add_form.save()
            titles = Title.objects.all()
            for title in titles:
                title_in_library = TitleInLibrary.objects.create(title=title, library=library, owned=False)
                TitleNotOwned.objects.create(title_in_library=title_in_library)
            return redirect('library_detail', library_id=library.id)

    return render(request, 'main/library_add.html', {'library_form': library_add_form, 'level': level})


# View for library editing page
def library_edit(request, library_id):
    # tries to edit library with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only administrator is allowed
    if level != 3:
        return redirect('home')
    library_var = Library.objects.filter(id=library_id).first()
    if not library_var:
        return redirect('library_list')
    library_add_form = LibraryForm(instance=library_var)

    # listens for delete action (deletes library with this id) or input form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                library_var.delete()
                return redirect('library_list')
        else:
            library_add_form = LibraryForm(request.POST, instance=library_var)
            if library_add_form.is_valid():
                library_add_form.save()
                return redirect('library_detail', library_id=library_id)

    return render(request, 'main/library_edit.html', {'library_form': library_add_form, 'level': level})


# View for order list page
def order_list(request):
    # gets and displays all orders separated into pending and delivered ones or ones meeting search criteria
    #       (employee, distributor, state, created between dates)
    # displays unfinished orders at the top of the page if they exist
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # basic user not allowed
    if level not in [1, 2, 3]:
        return redirect('home')
    # different data displayed for distributor than employees
    if level == 1:
        order_list_not_handled = Order.objects.filter(finished=True, handled=False,
                                                      distributor__username__exact=request.user.username).order_by(
            '-created')
        order_list_handled = Order.objects.filter(finished=True, handled=True,
                                                  distributor__username__exact=request.user.username).order_by(
            '-created')
        order_list_not_finished = None
    else:
        order_list_not_handled = Order.objects.filter(finished=True, handled=False).order_by('-created')
        order_list_handled = Order.objects.filter(finished=True, handled=True).order_by('-created')
        if level == 2:
            order_list_not_finished = Order.objects.filter(finished=False, employee__username__exact=request.user.
                                                           username).order_by('-created')
        else:
            order_list_not_finished = Order.objects.filter(finished=False).order_by('-created')
    order_form = OrderSearchForm

    # listens for search form confirmation
    if request.method == 'POST' and level != 1:
        employee_id = request.POST.get('employee')
        distributor_id = request.POST.get('distributor')
        state = request.POST.get('state')
        created_from = request.POST.get('created_after')
        created_to = request.POST.get('created_before')

        if employee_id or distributor_id or state or created_from or created_to:
            employee_regex = '^' + Employee.objects.get(id=employee_id).username + '$' if employee_id else '.*'
            distributor_regex = '^' + Distributor.objects.get(
                id=distributor_id).username + '$' if distributor_id else '.*'
            created_from = created_from if created_from else '2000-01-01'
            created_to = created_to if created_to else '3000-01-01'
            if state == 'handled':
                order_list_not_handled = None
                order_list_handled = Order.objects.filter(employee__username__iregex=employee_regex,
                                                          distributor__username__iregex=distributor_regex,
                                                          created__gte=created_from,
                                                          created__lte=created_to,
                                                          finished=True,
                                                          handled=True).order_by('-created').distinct()
            elif state == 'unhandled':
                order_list_handled = None
                order_list_not_handled = Order.objects.filter(employee__username__iregex=employee_regex,
                                                              distributor__username__iregex=distributor_regex,
                                                              created__gte=created_from,
                                                              created__lte=created_to,
                                                              finished=True,
                                                              handled=False).order_by('-created').distinct()
            else:
                order_list_handled = Order.objects.filter(employee__username__iregex=employee_regex,
                                                          distributor__username__iregex=distributor_regex,
                                                          created__gte=created_from,
                                                          created__lte=created_to,
                                                          finished=True,
                                                          handled=True).order_by('-created').distinct()
                order_list_not_handled = Order.objects.filter(employee__username__iregex=employee_regex,
                                                              distributor__username__iregex=distributor_regex,
                                                              created__gte=created_from,
                                                              created__lte=created_to,
                                                              finished=True,
                                                              handled=False).order_by('-created').distinct()

        order_form = OrderSearchForm(initial={'employee': employee_id, 'distributor': distributor_id, 'state': state,
                                              'created_after': created_from, 'created_before': created_to})

    return render(request, 'main/order_list.html',
                  {'order_form': order_form, 'order_list_not_handled': order_list_not_handled,
                   'order_list_handled': order_list_handled,
                   'order_list_unfinished': order_list_not_finished, 'level': level})


# View for order detail page
def order_detail(request, order_id):
    # displays detail of order with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # basic users cant view orders
    if level not in [1, 2, 3]:
        return redirect('home')
    order_detail_var = Order.objects.filter(id=order_id).first()
    if not order_detail_var:
        return redirect('order_list')
    order_content_list = order_detail_var.ordertitleinlibrary_set.all().order_by('title_in_library__library_id',
                                                                                 'title_in_library__title__name')

    # listens for delete action, or deliver action (adds books of titles to libraries according to this order)
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                for i in OrderTitleInLibrary.objects.filter(order_id=order_id):
                    i.delete()
                order_detail_var.delete()
                return redirect('order_list')
            if request.POST.get('action') == 'execute':
                order_detail_var.handled = True
                order_detail_var.save()
                for i in order_content_list:
                    if i.title_in_library.owned is False:
                        i.title_in_library.titlenotowned.delete()
                    i.title_in_library.owned = True
                    i.title_in_library.save()
                    for j in range(i.count):
                        book = Book.objects.create(state=0, title_in_library=i.title_in_library)
                        order_detail_var.books.add(book)
                return redirect('order_list')

    return render(request, 'main/order_detail.html',
                  {'order_detail': order_detail_var, 'level': level, 'order_content': order_content_list})


# View for order adding page (initial)
def order_add(request):
    # tries to create a new order
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees can create orders
    if level not in [2, 3]:
        return redirect('home')
    order_add_form = OrderForm()

    # listens for cancel action (delete order and return), add action (add item to order and continue)
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'cancel':
                return redirect('order_list')
            elif request.POST.get('action') == 'add':
                distributor_id = request.POST.get('distributor')
                library_id = request.POST.get('library')
                title_isbn = request.POST.get('title')
                count = request.POST.get('count')
                employee = Employee.objects.filter(username__exact=request.user.username).first()
                title_in_library = TitleInLibrary.objects.filter(title__isbn=title_isbn, library_id=library_id).first()
                order_var = Order.objects.create(distributor_id=distributor_id, employee=employee,
                                                 created=datetime.now())
                OrderTitleInLibrary.objects.create(title_in_library=title_in_library, count=count, order=order_var)
                return redirect('order_add_more', order_id=order_var.id)

    return render(request, 'main/order_add.html',
                  {'order_form': order_add_form, 'level': level, 'order_detail': None, 'distributor': None})


# View for order adding page (adding more titles)
def order_add_more(request, order_id):
    # tries to handle creation of order with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees can create orders
    if level not in [2, 3]:
        return redirect('home')

    order_var = Order.objects.filter(id=order_id).first()
    if not order_var:
        return redirect('order_list')
    order_add_form = OrderForm(initial={'distributor': order_var.distributor})
    # listens for cancel action, add item action, finish action (finishes order creation and returns)
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'cancel':
                for i in OrderTitleInLibrary.objects.filter(order_id=order_id):
                    i.delete()
                order_var.delete()
                return redirect('order_list')
            elif request.POST.get('action') == 'add':
                distributor_id = request.POST.get('distributor')
                library_id = request.POST.get('library')
                title_isbn = request.POST.get('title')
                count = request.POST.get('count')
                title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn, library_id=library_id)
                OrderTitleInLibrary.objects.create(title_in_library=title_in_library, count=count, order=order_var)
                order_var.distributor_id = distributor_id
                order_var.save()
                return redirect('order_add_more', order_id=order_id)
            elif request.POST.get('action') == 'finish':
                items_in_order = len(OrderTitleInLibrary.objects.filter(order_id=order_id))
                if items_in_order <= 0:
                    order_var.delete()
                else:
                    order_var.finished = True
                    order_var.created = datetime.now()
                    order_var.save()
                return redirect('order_list')

        elif request.POST.get('remove') is not None:
            OrderTitleInLibrary.objects.filter(id=request.POST.get('remove')).delete()
            return redirect('order_add_more', order_id=order_id)

    return render(request, 'main/order_add.html', {'order_form': order_add_form, 'level': level,
                                                   'order_detail': order_var.ordertitleinlibrary_set.all(),
                                                   'distributor': order_var.distributor})


# View for borrowing list page
def borrowing_list(request):
    # gets and displays all borrowings or ones that meet given search criteria
    #       (user, created by employee, state, borrowed between dates, deadline/returned between dates)
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [0, 2, 3]:
        return redirect('home')

    borrowing_list_unfinshed_var = None
    # for basic user get only his borrowings
    if level == 0:
        borrowing_list_active_var = Borrowing.objects.filter(profile__username__exact=request.user.username,
                                                             returned=False, finished=True).order_by('-borrowed_to')
        borrowing_list_returned_var = Borrowing.objects.filter(profile__username__exact=request.user.username,
                                                               returned=True, finished=True).order_by('-borrowed_to')
    else:
        borrowing_list_active_var = Borrowing.objects.filter(returned=False, finished=True).order_by('-borrowed_to')
        borrowing_list_returned_var = Borrowing.objects.filter(returned=True, finished=True).order_by('-borrowed_to')
        borrowing_list_unfinshed_var = Borrowing.objects.filter(finished=False).order_by('-borrowed_from')
    borrowing_form = BorrowingSearchForm()

    # listens for search form confirmation (only for employees)
    if request.method == 'POST' and level != 0:
        user_id = request.POST.get('user')
        created_id = request.POST.get('created')
        state = request.POST.get('state')
        start_from = request.POST.get('borrowing_start_after')
        start_to = request.POST.get('borrowing_start_before')
        end_from = request.POST.get('borrowing_end_after')
        end_to = request.POST.get('borrowing_end_before')

        if user_id or created_id or state or start_from or start_to or end_from or end_to:
            user_regex = '^' + Profile.objects.get(id=user_id).username + '$' if user_id else '.*'
            created_regex = '^' + Employee.objects.get(id=created_id).username + '$' if created_id else '.*'
            start_from = start_from if start_from else '2000-01-01'
            start_to = start_to if start_to else '3000-01-01'
            end_from = end_from if end_from else '2000-01-01'
            end_to = end_to if end_to else '3000-01-01'
            if state == 'active':
                borrowing_list_returned_var = None
                borrowing_list_active_var = Borrowing.objects.filter(profile__username__iregex=user_regex,
                                                                     created__username__iregex=created_regex,
                                                                     borrowed_from__gte=start_from,
                                                                     borrowed_from__lte=start_to,
                                                                     borrowed_to__gte=end_from,
                                                                     borrowed_to__lte=end_to, finished=True,
                                                                     returned=False).order_by('-borrowed_to').distinct()
            elif state == 'returned':
                borrowing_list_active_var = None
                borrowing_list_returned_var = Borrowing.objects.filter(profile__username__iregex=user_regex,
                                                                       created__username__iregex=created_regex,
                                                                       borrowed_from__gte=start_from,
                                                                       borrowed_from__lte=start_to,
                                                                       borrowed_to__gte=end_from,
                                                                       borrowed_to__lte=end_to, finished=True,
                                                                       returned=True).order_by(
                    '-borrowed_to').distinct()
            else:
                borrowing_list_active_var = Borrowing.objects.filter(profile__username__iregex=user_regex,
                                                                     created__username__iregex=created_regex,
                                                                     borrowed_from__gte=start_from,
                                                                     borrowed_from__lte=start_to,
                                                                     borrowed_to__gte=end_from,
                                                                     borrowed_to__lte=end_to, finished=True,
                                                                     returned=False).order_by('-borrowed_to').distinct()
                borrowing_list_returned_var = Borrowing.objects.filter(profile__username__iregex=user_regex,
                                                                       created__username__iregex=created_regex,
                                                                       borrowed_from__gte=start_from,
                                                                       borrowed_from__lte=start_to,
                                                                       borrowed_to__gte=end_from,
                                                                       borrowed_to__lte=end_to, finished=True,
                                                                       returned=True).order_by(
                    '-borrowed_to').distinct()

        borrowing_form = BorrowingSearchForm(initial={'user': user_id, 'created': created_id, 'state': state,
                                                      'borrowing_start_after': start_from,
                                                      'borrowing_start_before': start_to,
                                                      'borrowing_end_after': end_from,
                                                      'borrowing_end_before': end_to})

    return render(request, 'main/borrowing_list.html',
                  {'borrowing_form': borrowing_form, 'borrowing_list_active': borrowing_list_active_var,
                   'borrowing_list_returned': borrowing_list_returned_var, 'borrowing_list_unfinished':
                       borrowing_list_unfinshed_var, 'level': level})


# View for borrowing detail page
def borrowing_detail(request, borrowing_id):
    # displays detail of borrowing with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [0, 2, 3]:
        return redirect('home')
    borrowing_detail_var = Borrowing.objects.filter(id=borrowing_id).first()
    if not borrowing_detail_var:
        return redirect('borrowing_list')
    if level == 0 and borrowing_detail_var.profile.username != request.user.username:
        return redirect('borrowing_list')

    # listens for  actions
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            #  collect action simulates return of a borrowing
            if request.POST.get('action') == 'collect':
                borrowing_detail_var.returned = True
                employee = Employee.objects.filter(username__exact=request.user.username).first()
                borrowing_detail_var.collected = employee
                borrowing_detail_var.borrowed_to = datetime.now()
                borrowing_detail_var.save()
                for book in borrowing_detail_var.books.all():
                    book.state = 0
                    book.save()
                    reservation = Reservation.objects.filter(title_in_library=book.title_in_library,
                                                             ready=False).order_by('created').first()
                    if reservation:
                        reservation.book = book
                        reservation.ready = True
                        reservation.save()
                        book.state = 1
                        book.save()
                return redirect('borrowing_list')
            # extend action - extends borrowing duration by 30 days
            elif request.POST.get('action') == 'extend':
                days = (borrowing_detail_var.borrowed_to - borrowing_detail_var.borrowed_from).days
                if days <= 30:
                    borrowing_detail_var.borrowed_to += timedelta(days=30)
                    borrowing_detail_var.save()
                else:
                    messages.info(request, 'Cant extend. Maximum borrowing period is 60 days.')

    return render(request, 'main/borrowing_detail.html', {'borrowing_detail': borrowing_detail_var, 'level': level})


# View for borrowing adding page (initial)
def borrowing_add(request):
    # tries to create a new borrowing
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [2, 3]:
        return redirect('home')
    borrowing_add_form = BorrowingForm()

    # listens for cancel action (dont create and return), and add action (add item and continue)
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'cancel':
                return redirect('borrowing_list')
            elif request.POST.get('action') == 'add':
                user_id = request.POST.get('user')
                length_days = request.POST.get('days')
                book_id = request.POST.get('book')
                employee = Employee.objects.filter(username__exact=request.user.username).first()
                curr_datetime = datetime.now()
                deadline = curr_datetime + timedelta(days=int(length_days))
                borrowing_var = Borrowing.objects.create(profile_id=user_id, created=employee,
                                                         borrowed_from=curr_datetime, borrowed_to=deadline)
                book = Book.objects.get(id=book_id)
                # if book available
                if book.state == 0:
                    book.state = 2
                    book.save()
                    borrowing_var.books.add(book)
                    borrowing_var.save()
                    return redirect('borrowing_add_more', borrowing_id=borrowing_var.id)
                else:
                    messages.info(request, 'Selected book is not available at this moment.')

    return render(request, 'main/borrowing_add.html',
                  {'borrowing_form': borrowing_add_form, 'level': level, 'borrowing_detail': None})


# View for borrowing adding page (adding more books)
def borrowing_add_more(request, borrowing_id):
    # tries to handle creation of borrowing with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [2, 3]:
        return redirect('home')
    borrowing_var = Borrowing.objects.filter(id=borrowing_id).first()
    if not borrowing_var:
        return redirect('borrowing_list')
    days = (borrowing_var.borrowed_to - borrowing_var.borrowed_from).days
    borrowing_add_form = BorrowingForm(initial={'user': borrowing_var.profile, 'days': days})

    # listens for cancel action, finish action (confirm and finish borrowing) and add action (add item and continue)
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'cancel':
                for i in borrowing_var.books.all():
                    i.state = 0
                    reservation = Reservation.objects.filter(title_in_library=i.title_in_library,
                                                             ready=False).order_by('created').first()
                    if reservation:
                        reservation.book = i
                        reservation.ready = True
                        reservation.save()
                        i.state = 1
                    i.save()
                borrowing_var.delete()
                return redirect('borrowing_list')
            elif request.POST.get('action') == 'add':
                user_id = request.POST.get('user')
                length_days = request.POST.get('days')
                book_id = request.POST.get('book')
                borrowing_var.profile_id = user_id
                borrowing_var.borrowed_to = borrowing_var.borrowed_from + timedelta(days=int(length_days))
                book = Book.objects.get(id=book_id)
                # if book is available
                if book.state == 0:
                    book.state = 2
                    book.save()
                    borrowing_var.books.add(book_id)
                    borrowing_var.save()
                else:
                    messages.info(request, 'Selected book is not available at this moment.')
                return redirect('borrowing_add_more', borrowing_id=borrowing_id)
            elif request.POST.get('action') == 'finish':
                books_in_borrowing = len(borrowing_var.books.all())
                # if borrowing is empty
                if books_in_borrowing <= 0:
                    borrowing_var.delete()
                else:
                    days = (borrowing_var.borrowed_to - borrowing_var.borrowed_from).days
                    borrowing_var.borrowed_from = datetime.now()
                    borrowing_var.borrowed_to = datetime.now() + timedelta(days=int(days))
                    borrowing_var.finished = True
                    borrowing_var.save()
                return redirect('borrowing_list')

        elif request.POST.get('remove') is not None:
            book = Book.objects.get(id=request.POST.get('remove'))
            borrowing_var.books.remove(book)
            return redirect('borrowing_add_more', borrowing_id=borrowing_id)

    return render(request, 'main/borrowing_add.html',
                  {'borrowing_form': borrowing_add_form, 'level': level, 'borrowing_detail': borrowing_var})


# View for reservation list page
def reservation_list(request):
    # gets and displays all reservations or ones that meet search criteria (user, created between dates)
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    reservation_list_var = None
    if level not in [0, 2, 3]:
        return redirect('home')

    if level == 0:
        reservation_list_var = Reservation.objects.filter(profile__username__exact=request.user.username).order_by(
            '-ready', 'created')
    elif level == 2 or level == 3:
        reservation_list_var = Reservation.objects.all().order_by('-ready', 'created')
    reservation_form = ReservationSearchForm()

    if request.method == 'POST' and level != 0:
        user_id = request.POST.get('user')
        state = request.POST.get('state')
        created_from = request.POST.get('created_after')
        created_to = request.POST.get('created_before')

        if user_id or state or created_from or created_to:
            user_regex = '^' + Profile.objects.get(id=user_id).username + '$' if user_id else '.*'
            created_from = created_from if created_from else '2000-01-01'
            created_to = created_to if created_to else '3000-01-01'
            if state == 'ready':
                reservation_list_var = \
                    Reservation.objects.filter(profile__username__iregex=user_regex,
                                               created__gte=created_from, created__lte=created_to,
                                               ready=True).order_by('-ready', 'created').distinct()
            elif state == 'waiting':
                reservation_list_var = \
                    Reservation.objects.filter(profile__username__iregex=user_regex,
                                               created__gte=created_from, created__lte=created_to,
                                               ready=False).order_by('-ready', 'created').distinct()
            else:
                reservation_list_var = \
                    Reservation.objects.filter(profile__username__iregex=user_regex, created__gte=created_from,
                                               created__lte=created_to).order_by('-ready', 'created').distinct()

        reservation_form = ReservationSearchForm(
            initial={'user': user_id, 'state': state, 'created_after': created_from, 'created_before': created_to})

    return render(request, 'main/reservation_list.html',
                  {'reservation_form': reservation_form, 'reservation_list': reservation_list_var, 'level': level})


# View for reservation detail page
def reservation_detail(request, reservation_id):
    # displays detail of reservation with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [0, 2, 3]:
        return redirect('home')
    reservation_detail_var = Reservation.objects.filter(id=reservation_id).first()
    if not reservation_detail_var:
        return redirect('reservation_list')
    if level == 0 and reservation_detail_var.profile.username != request.user.username:
        return redirect('reservation_list')

    # listens for actions
    if request.method == 'POST':
        # cancel reservation cancels this reservation
        if request.POST.get('cancel_reservation') is not None:
            if reservation_detail_var.book is not None:
                reservation_detail_var.book.state = 0
                reservation_detail_var.book.save()
            reservation_detail_var.delete()
            return redirect('reservation_list')
        # to borrowing starts borrowing creation with book from this reservation already added
        if request.POST.get('to_borrowing') is not None:
            user_id = reservation_detail_var.profile.id
            length_days = 30
            book = reservation_detail_var.book
            employee = Employee.objects.filter(username__exact=request.user.username).first()
            curr_datetime = datetime.now()
            deadline = curr_datetime + timedelta(days=int(length_days))
            borrowing_var = Borrowing.objects.create(profile_id=user_id, created=employee, borrowed_from=curr_datetime,
                                                     borrowed_to=deadline)
            if book.state == 1:
                book.state = 2
                book.save()
                borrowing_var.books.add(book)
                borrowing_var.save()
                reservation_detail_var.delete()
                return redirect('borrowing_add_more', borrowing_id=borrowing_var.id)
            else:
                messages.info(request, 'Selected book is not available at this moment.')

    return render(request, 'main/reservation_detail.html',
                  {'reservation_detail': reservation_detail_var, 'level': level})


# View for reservation adding page
def reservation_add(request):
    # tries to create a new reservation
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    reservation_add_form = ReservationForm()

    # listens for form confirmation
    if request.method == 'POST':
        user_id = request.POST.get('user')
        title_id = request.POST.get('title')
        library_id = request.POST.get('library')
        title_in_library_var = TitleInLibrary.objects.filter(title_id=title_id, library_id=library_id).first()
        reservation_var = Reservation.objects.create(profile_id=user_id, created=datetime.now(),
                                                     title_in_library=title_in_library_var)
        # if there is an available book - add it to reservation and mark as reserved
        free_book = Book.objects.filter(title_in_library=title_in_library_var, state=0).first()
        if free_book is not None:
            reservation_var.book = free_book
            reservation_var.ready = True
            reservation_var.save()
            free_book.state = 1
            free_book.save()
        return redirect('reservation_list')

    return render(request, 'main/reservation_add.html', {'reservation_form': reservation_add_form, 'level': level})


# View for vote list page
def vote_list(request):
    # gets and displays all votes
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    votes_dict = {}
    if level == 1:
        return redirect('home')

    # for employees - displays form with checkboxes for all items with any votes that allows to directly put
    #       selected ones into an order
    if level == 2 or level == 3:
        # listens for prompt to put items in an order
        if request.method == 'POST':
            distributor = Distributor.objects.first()
            if distributor:
                employee = Employee.objects.filter(username__exact=request.user.username).first()
                order_var = Order.objects.create(distributor=distributor, employee=employee, created=datetime.now())
                for i in request.POST.getlist('selected'):
                    isbn, library_id, count = i.split('&')
                    count = int(count) // 10 + 1
                    title_in_library = TitleInLibrary.objects.get(title__isbn=isbn, library_id=library_id)
                    OrderTitleInLibrary.objects.create(title_in_library=title_in_library, count=count, order=order_var)
                return redirect('order_add_more', order_id=order_var.id)
            else:
                messages.info(request, 'Cannot create an order because there are no distributors to order from.')

        title_not_owned_list_var = TitleNotOwned.objects.all().order_by('-vote_count', 'title_in_library__title__name')
        for i in title_not_owned_list_var:
            if i.vote_count > 0:
                votes_dict[i.title_in_library] = i.vote_count
        return render(request, 'main/vote_list_select.html', {'votes_dict': votes_dict, 'level': level})

    # for basic users displays list of all titles with options
    elif level == 0:
        # listens for actions
        if request.method == 'POST':
            # set vote - adds a vote for a title in a library from this user
            if request.POST.get('set_vote') is not None:
                title_isbn, library_id = request.POST.get('set_vote').split('&')
                title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn, library__id=library_id)
                profile_var = Profile.objects.filter(username__exact=request.user.username).first()
                title_in_library.titlenotowned.votes.add(profile_var)
                title_in_library.titlenotowned.vote_count += 1
                title_in_library.titlenotowned.save()
                return redirect('vote_list')
            # cancel votes removes this vote
            elif request.POST.get('cancel_vote') is not None:
                title_isbn, library_id = request.POST.get('cancel_vote').split('&')
                title_in_library = TitleInLibrary.objects.get(title__isbn=title_isbn, library__id=library_id)
                profile_var = Profile.objects.filter(username__exact=request.user.username).first()
                title_in_library.titlenotowned.votes.remove(profile_var)
                title_in_library.titlenotowned.vote_count -= 1
                title_in_library.titlenotowned.save()
                return redirect('vote_list')

    title_not_owned_list_var = TitleNotOwned.objects.all().order_by('-vote_count', 'title_in_library__title__name')
    voted = False
    for i in title_not_owned_list_var:
        if request.user.is_authenticated:
            voted = i.votes.filter(username__exact=request.user.username).exists()
        votes_dict[i.title_in_library] = [i.vote_count, voted]
    return render(request, 'main/vote_list_view.html', {'votes_dict': votes_dict, 'level': level})


# View for profile page
def profile(request):
    # displays profile page of current user
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level == -1:
        return redirect('home')
    profile_var = None
    if level == 0:
        profile_var = Profile.objects.filter(username__exact=request.user.username).first()
    elif level == 1:
        profile_var = Distributor.objects.filter(username__exact=request.user.username).first()
    elif level == 2 or level == 3:
        profile_var = Employee.objects.filter(username__exact=request.user.username).first()

    return render(request, 'main/profile_detail.html', {'profile': profile_var, 'level': level})


# View for editing of profile page
def profile_edit(request):
    # tries to edit profile information of current user
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level == -1:
        return redirect('home')
    profile_var = None
    if level == 0:
        profile_var = Profile.objects.filter(username__exact=request.user.username).first()
    elif level == 1:
        profile_var = Distributor.objects.filter(username__exact=request.user.username).first()
    elif level == 2 or level == 3:
        profile_var = Employee.objects.filter(username__exact=request.user.username).first()
    profile_type_var = ProfileType.objects.filter(username__exact=request.user.username).first()
    user_var = User.objects.filter(username__exact=request.user.username).first()
    profile_edit_form = ProfileEditForm(instance=user_var)

    # listens for delete action or edit form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                if level != 3:
                    if not Borrowing.objects.filter(profile__username__exact=profile_var.username, returned=False):
                        for r in Reservation.objects.filter(profile__username__exact=profile_var.username,
                                                            ready=True).all():
                            reservations = Reservation.objects.filter(title_in_library=r.title_in_library,
                                                                      ready=False).order_by('created')
                            if reservations:
                                reservations.first().book = r.book
                                reservations.first().ready = True
                                reservations.first().save()
                            else:
                                r.book.state = 0
                                r.book.save()
                        profile_type_var.delete()
                        profile_var.delete()
                        user_var.delete()
                        return redirect('home')
                    else:
                        messages.info(request, 'Cannot delete. First return all borrowed books.')
                else:
                    messages.info(request, 'Administrator account can not be deleted.')
        else:
            profile_edit_form = ProfileEditForm(request.POST, instance=user_var)
            if profile_edit_form.is_valid():
                profile_edit_form.save()
                profile_var.name = request.POST.get('first_name')
                profile_var.save()
                return redirect('profile')

    return render(request, 'main/profile_edit.html',
                  {'profile': profile_var, 'profile_edit_form': profile_edit_form, 'level': level})


# View for employee list page
def employee_list(request):
    # displays list of all employees
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only admin is allowed
    if level != 3:
        return redirect('home')
    employee_list_var = Employee.objects.all().order_by('-administrator', 'username')

    return render(request, 'main/employee_list.html', {'employee_list': employee_list_var, 'level': level})


# View for employee detail page
def employee_detail(request, employee_id):
    # displays detail of employee with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only admin is allowed
    if level != 3:
        return redirect('home')
    employee_detail_var = Employee.objects.filter(id=employee_id).first()
    if not employee_detail_var:
        return redirect('employee_list')

    # listens for edit and delete actions
    if request.method == 'POST':
        if request.POST.get('action') == 'edit':
            return redirect('employee_detail', employee_id=employee_id)
        elif request.POST.get('action') == 'delete':
            if not employee_detail_var.administrator:
                employee_var = Employee.objects.get(id=employee_id)
                profile_type = ProfileType.objects.get(username__exact=employee_var.username)
                user_var = User.objects.filter(username__exact=employee_var.username).first()
                profile_type.delete()
                employee_var.delete()
                user_var.delete()
                return redirect('employee_list')
            else:
                messages.info(request, 'Administrator account can not be deleted.')

    order_list_var = Order.objects.filter(employee_id=employee_detail_var.id, finished=True)
    borrowing_created_list_var = Borrowing.objects.filter(created_id=employee_detail_var.id, finished=True)
    borrowing_collected_list_var = Borrowing.objects.filter(collected_id=employee_detail_var.id, finished=True)

    return render(request, 'main/employee_detail.html',
                  {'employee_detail': employee_detail_var, 'level': level, 'order_list': order_list_var,
                   'borrowing_1_list': borrowing_created_list_var, 'borrowing_2_list': borrowing_collected_list_var})


# View for employee adding page
def employee_add(request):
    # tries to add a new employee
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only admin is allowed
    if level != 3:
        return redirect('home')
    employee_add_form = RegisterForm()

    # listens for form confirmation
    if request.method == 'POST':
        employee_add_form = RegisterForm(request.POST)
        if employee_add_form.is_valid():
            if not Employee.objects.filter(email__exact=request.POST.get('email')).exists():
                employee_add_form.save()
                employee_var = Employee.objects.create(username=request.POST.get('username'),
                                                       name=request.POST.get('first_name'),
                                                       email=request.POST.get('email'), administrator=False)
                ProfileType.objects.create(username=request.POST.get('username'), level=2)
                return redirect('employee_detail', employee_id=employee_var.id)
            else:
                messages.info(request, 'An account with this email address already exists.')

    return render(request, 'main/employee_add.html', {'employee_form': employee_add_form, 'level': level})


# View for employee editing page
def employee_edit(request, employee_id):
    # tries to edit an employee with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level != 3:
        return redirect('home')
    employee_var = Employee.objects.filter(id=employee_id).first()
    if not employee_var:
        return redirect('employee_list')
    profile_type_var = ProfileType.objects.get(username__exact=employee_var.username)
    user_var = User.objects.get(username__exact=employee_var.username)
    profile_edit_form = ProfileEditForm(instance=user_var)

    # listens for delete action or form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                if profile_type_var.level != 3:
                    profile_type_var.delete()
                    employee_var.delete()
                    user_var.delete()
                    return redirect('employee_list')
                else:
                    messages.info(request, 'Administrator account can not be deleted.')
        else:
            profile_edit_form = ProfileEditForm(request.POST, instance=user_var)
            if profile_edit_form.is_valid():
                profile_edit_form.save()
                employee_var.name = request.POST.get('first_name')
                employee_var.save()
                return redirect('employee_detail', employee_id=employee_id)

    return render(request, 'main/employee_edit.html',
                  {'employee_detail': employee_var, 'employee_form': profile_edit_form, 'level': level})


# View for distributor list page
def distributor_list(request):
    # displays list of all distributors
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees are allowed
    if level not in [2, 3]:
        return redirect('home')
    distributor_list_var = Distributor.objects.all().order_by('username')

    return render(request, 'main/distributor_list.html', {'distributor_list': distributor_list_var, 'level': level})


# View for distributor detail page
def distributor_detail(request, distributor_id):
    # displays detail of distributor with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees are allowed
    if level not in [2, 3]:
        return redirect('home')
    distributor_detail_var = Distributor.objects.filter(id=distributor_id).first()
    if not distributor_detail_var:
        return redirect('distributor_list')

    # listens for edit and delete actions
    if request.method == 'POST':
        if request.POST.get('action') == 'edit':
            return redirect('distributor_detail', distributor_id=distributor_id)
        elif request.POST.get('action') == 'delete':
            distributor_var = Distributor.objects.get(id=distributor_id)
            profile_type = ProfileType.objects.get(username__exact=distributor_var.username)
            user_var = User.objects.filter(username__exact=distributor_var.username).first()
            profile_type.delete()
            distributor_var.delete()
            user_var.delete()
            return redirect('distributor_list')

    order_list_var = Order.objects.filter(distributor_id=distributor_detail_var.id, finished=True)

    return render(request, 'main/distributor_detail.html',
                  {'distributor_detail': distributor_detail_var, 'order_list': order_list_var, 'level': level})


# View for distributor adding page
def distributor_add(request):
    # tries to add a new distributor profile
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level != 3:
        return redirect('home')
    distributor_add_form = RegisterForm()

    # listens for form confirmation
    if request.method == 'POST':
        distributor_add_form = RegisterForm(request.POST)
        if distributor_add_form.is_valid():
            if not Distributor.objects.filter(email__exact=request.POST.get('email')).exists():
                distributor_add_form.save()
                distributor_var = Distributor.objects.create(username=request.POST.get('username'),
                                                             name=request.POST.get('first_name'),
                                                             email=request.POST.get('email'))
                ProfileType.objects.create(username=request.POST.get('username'), level=1)
                return redirect('distributor_detail', distributor_id=distributor_var.id)
            else:
                messages.info(request, 'An account with this email address already exists.')

    return render(request, 'main/distributor_add.html', {'distributor_form': distributor_add_form, 'level': level})


# View for distributor editing page
def distributor_edit(request, distributor_id):
    # tries to edit a distributor profile with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only admin is allowed
    if level != 3:
        return redirect('home')
    distributor_var = Distributor.objects.filter(id=distributor_id).first()
    if not distributor_var:
        return redirect('distributor_list')
    profile_type_var = ProfileType.objects.get(username__exact=distributor_var.username)
    user_var = User.objects.get(username__exact=distributor_var.username)
    profile_edit_form = ProfileEditForm(instance=user_var)

    # listens for form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                profile_type_var.delete()
                distributor_var.delete()
                user_var.delete()
                return redirect('distributor_list')
        else:
            profile_edit_form = ProfileEditForm(request.POST, instance=user_var)
            if profile_edit_form.is_valid():
                profile_edit_form.save()
                distributor_var.name = request.POST.get('first_name')
                distributor_var.save()
                return redirect('distributor_detail', distributor_id=distributor_id)

    return render(request, 'main/distributor_edit.html',
                  {'distributor_detail': distributor_var, 'distributor_form': profile_edit_form, 'level': level})


# View for user list page
def user_list(request):
    # displays list of all users
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees allowed
    if level not in [2, 3]:
        return redirect('home')
    user_list_var = Profile.objects.all().order_by('username')

    return render(request, 'main/user_list.html', {'user_list': user_list_var, 'level': level})


# View for user detail page
def user_detail(request, user_id):
    # displays detail of user profile with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    # only employees allowed
    if level not in [2, 3]:
        return redirect('home')
    user_detail_var = Profile.objects.filter(id=user_id).first()
    if not user_detail_var:
        return redirect('user_list')

    reservation_list_var = Reservation.objects.filter(profile_id=user_id)
    active_borrowing_list_var = Borrowing.objects.filter(profile_id=user_id, returned=False, finished=True)
    returned_borrowing_list_var = Borrowing.objects.filter(profile_id=user_id, returned=True, finished=True)

    return render(request, 'main/user_detail.html',
                  {'user_detail': user_detail_var, 'level': level, 'reservation_list': reservation_list_var,
                   'active_borrowing_list': active_borrowing_list_var,
                   'returned_borrowing_list': returned_borrowing_list_var})


# View for user editing page
def user_edit(request, user_id):
    # trie to edit the user profile with this id
    level = ProfileType.objects.filter(
        username__exact=request.user.username).first().level if request.user.is_authenticated else -1
    if level not in [2, 3]:
        return redirect('home')
    profile_var = Profile.objects.filter(id=user_id).first()
    if not profile_var:
        return redirect('user_list')
    profile_type_var = ProfileType.objects.get(username__exact=profile_var.username)
    user_var = User.objects.get(username__exact=profile_var.username)
    profile_edit_form = ProfileEditForm(instance=user_var)

    # listens for delete action or form confirmation
    if request.method == 'POST':
        if request.POST.get('action') is not None:
            if request.POST.get('action') == 'delete':
                if not Borrowing.objects.filter(profile_id=user_id, returned=False):
                    for r in Reservation.objects.filter(profile_id=user_id, ready=True).all():
                        reservations = Reservation.objects.filter(title_in_library=r.title_in_library,
                                                                  ready=False).order_by('created')
                        if reservations:
                            reservations.first().book = r.book
                            reservations.first().ready = True
                            reservations.first().save()
                        else:
                            r.book.state = 0
                            r.book.save()
                    profile_type_var.delete()
                    profile_var.delete()
                    user_var.delete()
                    return redirect('user_list')
                else:
                    messages.info(request, 'Cannot delete. User has an active borrowing.')
        else:
            profile_edit_form = ProfileEditForm(request.POST, instance=user_var)
            if profile_edit_form.is_valid():
                profile_edit_form.save()
                profile_var.name = request.POST.get('first_name')
                profile_var.save()
                return redirect('user_detail', user_id=user_id)

    return render(request, 'main/user_edit.html',
                  {'user_detail': profile_var, 'user_form': profile_edit_form, 'level': level})
