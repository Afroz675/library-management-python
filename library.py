
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn, genre, qty):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.qty = qty

    def __repr__(self):
        return f'"{self.title}" by {self.author} - {self.qty} left'

class Borrower:
    def __init__(self, name, contact, member_id):
        self.name = name
        self.contact = contact
        self.member_id = member_id

    def __repr__(self):
        return f'{self.name} (ID: {self.member_id})'

class Library:
    def __init__(self):
        self.books = {}       # isbn -> Book
        self.borrowers = {}   # member_id -> Borrower
        self.borrowed = {}    # member_id -> [(isbn, due_date)]

    # --- Book Management ---
    def add_book(self, b):
        self.books[b.isbn] = b
        print(f"Added book: {b}")

    def update_book(self, isbn, **kw):
        if isbn in self.books:
            for k, v in kw.items():
                setattr(self.books[isbn], k, v)
            print(f"Updated book {isbn}")
        else:
            print("Book not found.")

    def remove_book(self, isbn):
        if isbn in self.books:
            del self.books[isbn]
            print(f"Removed book {isbn}")
        else:
            print("Book not found.")

    # --- Borrower Management ---
    def add_borrower(self, br):
        self.borrowers[br.member_id] = br
        print(f"Added borrower: {br}")

    def update_borrower(self, mid, **kw):
        if mid in self.borrowers:
            for k, v in kw.items():
                setattr(self.borrowers[mid], k, v)
            print(f"Updated borrower {mid}")
        else:
            print("Borrower not found.")

    def remove_borrower(self, mid):
        if mid in self.borrowers:
            del self.borrowers[mid]
            print(f"Removed borrower {mid}")
        else:
            print("Borrower not found.")

    # --- Borrow & Return ---
    def borrow_book(self, mid, isbn, days=7):
        if mid not in self.borrowers:
            print("Borrower not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return
        book = self.books[isbn]
        if book.qty < 1:
            print("No copies available.")
            return

        book.qty -= 1
        due_date = datetime.now() + timedelta(days=days)
        self.borrowed.setdefault(mid, []).append((isbn, due_date))
        print(f"{book.title} borrowed by {self.borrowers[mid].name}. Due on {due_date}")

    def return_book(self, mid, isbn):
        if mid not in self.borrowed:
            print("No borrowed books found for this member.")
            return

        for b in self.borrowed[mid]:
            if b[0] == isbn:
                self.borrowed[mid].remove(b)
                self.books[isbn].qty += 1
                print(f"{self.books[isbn].title} returned.")
                return
        print("Book not found in borrowed list.")

    # --- Search ---
    def search(self, key):
        found = False
        for b in self.books.values():
            if key.lower() in b.title.lower() or key.lower() in b.author.lower() or key.lower() in b.genre.lower():
                print(f"{b.title} by {b.author} ({b.qty} available)")
                found = True
        if not found:
            print("No matching books.")

# --- Example Run ---
if __name__ == "__main__":
    L = Library()
    L.add_book(Book("Python Basics", "John Doe", "001", "Programming", 3))
    L.add_book(Book("Data Science Intro", "Jane Smith", "002", "Science", 2))
    L.add_borrower(Borrower("Alice", "alice@mail.com", "M1"))
    L.borrow_book("M1", "001")
    L.search("python")
    L.return_book("M1", "001")