class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('{n}: email address has been updated to {e}'.format(n=self.name, e=self.email))

    def __repr__(self):
        return 'User {n}, email: {e}, books read: {b}'.format(n=self.name, e=self.email, b=len(self.books))

    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        if len(self.books) > 0:
            for rating in self.books.values():
                if rating is not None:
                    total += rating
            return (total/len(self.books))

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('{t}: ISBN has been updated to {i}'.format(t=self.title, i=self.isbn))

    def add_rating(self, rating):
        if rating is not None:
            if (rating >= 0) and (rating <= 4):
                self.ratings.append(rating)

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def get_average_rating(self):
        total = 0
        if len(self.ratings) > 0:
            for rating in self.ratings:
                total += rating
            return (total/len(self.ratings))

    def __hash__(self):
        return hash((self.title, self.isbn))

    #Added __repr__ dunder method, since plain Book objects didn't have one in the project instructions
    def __repr__(self):
        return '{t} with ISBN: {i}'.format(t=self.title, i=self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return '{t} by {a}'.format(t=self.title, a=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return '{t}, a {l} manual on {s}'.format(t=self.title, l=self.level, s=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def unique_isbn_check(self, isbn):
        #Added check against already existing ISBNs, ensuring unique ISBNs
        #This check is the first step in create_book(), create_novel(), and create_non_fiction()
        existing_isbns = []
        for book in self.books.keys():
            existing_isbns.append(book.get_isbn())
        if isbn in existing_isbns:
            return False
        else:
            return True

    def create_book(self, title, isbn):
        #Check that this new book's isbn isn't already in Tome Rater
        if self.unique_isbn_check(isbn):
            new_book = Book(title, isbn)
            return new_book
        #If it is already here, tell the user and don't create a new Book object
        else:
            print('{t} with ISBN: {i} already exists in Tome Rater.'.format(t=title, i=isbn))

    def create_novel(self, title, author, isbn):
        if self.unique_isbn_check(isbn):
            new_novel = Fiction(title, author, isbn)
            return new_novel
        else:
            print('{t} with ISBN: {i} already exists in Tome Rater.'.format(t=title, i=isbn))

    def create_non_fiction(self, title, subject, level, isbn):
        if self.unique_isbn_check(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn)
            return new_non_fiction
        else:
            print('{t} with ISBN: {i} already exists in Tome Rater.'.format(t=title, i=isbn))

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email)
        if user is not None:
            user.read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print('No user with email {e}!'.format(e=email))

    def add_user(self, name, email, user_books=None):
        #Added error testing for valid email address and for unique email address
        if ('@' in email) and (('.com' in email) or ('.edu' in email) or ('.org') in email):
            if email in self.users.keys():
                print('The email {e} is already in use in Tome Rater.'.format(e=email))
            else:
                new_user = User(name, email)
                self.users[email] = new_user
                if user_books is not None:
                    for user_book in user_books:
                        self.add_book_to_user(user_book, email)
        else:
            print('Please provide a valid email address')

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        most_read = None
        most_read_number = 0
        for book, times_read in self.books.items():
            if times_read > most_read_number:
                most_read_number = times_read
                most_read = book
        return most_read

    def highest_rated_book(self):
        highest_rated = None
        highest_average = 0
        for book in self.books.keys():
            if book.get_average_rating() > highest_average:
                highest_average = book.get_average_rating()
                highest_rated = book
        return highest_rated

    def most_positive_user(self):
        most_positive = None
        highest_average = 0
        for user in self.users.values():
            if user.get_average_rating() > highest_average:
                highest_average = user.get_average_rating()
                most_positive = user
        return most_positive


        