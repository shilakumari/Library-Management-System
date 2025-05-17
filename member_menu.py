import datetime
from storage import load_csv, save_csv


def dashboard(session):
    while True:
        print("\n=== Member Dashboard ===")
        print("1. Search Catalogue\n2. Borrow Book\n3. My Loans\n4. Logout")
        choice = input("> ")
        if choice == '1':
            search_catalogue()
        if choice == '2':
            borrow_book(session['user']['MemberID'])
        elif choice == '3':
            view_my_loans(session['user']['MemberID'])
        elif choice == '4':
            break
        else:
            print("Invalid option")

def search_catalogue():
    keyword = input("Enter title or author keyword: ").lower()
    books = load_csv('books.csv')
    for b in books:
        if keyword in b['Title'].lower() or keyword in b['Author'].lower():
            print(f"{b['ISBN']} | {b['Title']} by {b['Author']} | Available: {b['CopiesAvailable']}")

def borrow_book(member_id):
    import uuid
    loans = load_csv('loans.csv')
    books = load_csv('books.csv')
    isbn = input("ISBN to issue: ")
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


def view_my_loans(member_id):
    loans = load_csv('loans.csv')
    print("\n--- Your Loans ---")
    for loan in loans:
        if loan['MemberID'] == member_id:
            print(f"LoanID: {loan['LoanID']} | Book: {loan['ISBN']} | Due: {loan['DueDate']} | Returned: {loan['ReturnDate'] or 'No'}")
