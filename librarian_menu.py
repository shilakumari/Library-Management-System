from storage import load_csv, save_csv
from models import Book
import datetime

def dashboard(session):
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book\n2. Remove Book\n3. Register Member\n4. Issue Book\n5. Return Book\n6. View Overdue List\n7. Logout")
        choice = input("> ")
        if choice == '1':
            add_book()
        if choice == '2':
            remove_book()
        elif choice == '3':
            import auth
            auth.register_member()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            view_overdue()
        elif choice == '7':
            break
        else:
            print("Invalid option")

def add_book():
    books = load_csv('books.csv')
    isbn = input("ISBN: ").strip()
    
    if not isbn or not isbn.isdigit() or len(isbn) not in (10, 13):
        print("Invalid ISBN format.")
        return

    for b in books:
        if b['ISBN'] == isbn:
            print("Book already exists.")
            return
    title = input("Title: ")
    author = input("Author: ")
    total = int(input("Total Copies: "))
    if total < 0 :
        print("Can't be Negative copies")
    new_book = {'ISBN': isbn, 'Title': title, 'Author': author, 'CopiesTotal': total, 'CopiesAvailable': total}
    books.append(new_book)
    save_csv('books.csv', books, new_book.keys())
    print("Book added.")

def remove_book():
    books = load_csv('books.csv')
    isbn = input("Enter ISBN of the book to delete: ")
    updated_books = [b for b in books if b['ISBN'] != isbn]
    
    if len(updated_books) == len(books):
        print("Book not found.")
    else:
        save_csv('books.csv', updated_books, books[0].keys())
        print("Book deleted.")


def issue_book():
    import uuid
    loans = load_csv('loans.csv')
    books = load_csv('books.csv')
    isbn = input("ISBN to issue: ").strip()
    if not isbn or not isbn.isdigit():
        print("Invalid ISBN.")
        return
    member_id = input("Member ID: ")
    for book in books:
        if book['ISBN'] == isbn:
            if int(book['CopiesAvailable']) <= 0:
                print("Book not available.")
                return
            book['CopiesAvailable'] = str(int(book['CopiesAvailable']) - 1)
            issue_date = datetime.date.today()
            due_date = issue_date + datetime.timedelta(days=14)
            new_loan = {
                'LoanID': str(uuid.uuid4()),
                'MemberID': member_id,
                'ISBN': isbn,
                'IssueDate': str(issue_date),
                'DueDate': str(due_date),
                'ReturnDate': ''
            }
            loans.append(new_loan)
            save_csv('loans.csv', loans, new_loan.keys())
            save_csv('books.csv', books, book.keys())
            print(f"Book issued. Due on {due_date.strftime('%d-%b-%Y')}.")
            return
    print("ISBN not found.")

def return_book():
    loans = load_csv('loans.csv')
    books = load_csv('books.csv')
    loan_id = input("Loan ID: ")
    for loan in loans:
        if loan['LoanID'] == loan_id and loan['ReturnDate'] == '':
            loan['ReturnDate'] = str(datetime.date.today())
            for book in books:
                if book['ISBN'] == loan['ISBN']:
                    book['CopiesAvailable'] = str(int(book['CopiesAvailable']) + 1)
            save_csv('loans.csv', loans, loan.keys())
            save_csv('books.csv', books, books[0].keys())
            print("Book returned.")
            return
    print("Loan not found or already returned.")

def view_overdue():
    loans = load_csv('loans.csv')
    today = datetime.date.today()
    print("\n--- Overdue Loans ---")
    for loan in loans:
        if loan['ReturnDate'] == '' and datetime.date.fromisoformat(loan['DueDate']) < today:
            print(f"LoanID: {loan['LoanID']}, MemberID: {loan['MemberID']}, Book: {loan['ISBN']}, Due: {loan['DueDate']}")

