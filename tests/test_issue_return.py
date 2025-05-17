import os
from storage import load_csv, save_csv
from librarian_menu import issue_book, return_book

TEST_DATA_DIR = ""  # or wherever your test CSV files are

def test_issue_and_return_book(monkeypatch):
    test_books_file = os.path.join(TEST_DATA_DIR, "books.csv")
    test_loans_file = os.path.join(TEST_DATA_DIR, "loans.csv")

    # Setup initial book data with 1 copy available
    test_isbn = "9780201616224"
    book = {
        "ISBN": test_isbn,
        "Title": "Test Book",
        "Author": "Tester",
        "CopiesTotal": "1",
        "CopiesAvailable": "1"
    }
    save_csv(test_books_file, [book], book.keys())
    save_csv(test_loans_file, [], ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"])

    # Monkeypatch input() for issue_book()
    monkeypatch.setattr("builtins.input", lambda prompt="": {
        "ISBN to issue: ": test_isbn,
        "Member ID: ": "1001",
        "Loan ID: ": ""  # default empty for return_book
    }[prompt])

    # Monkeypatch file loading/saving to use test data dir
    monkeypatch.setattr("librarian_menu.load_csv", lambda f: load_csv(f.replace("data", TEST_DATA_DIR)))
    monkeypatch.setattr("librarian_menu.save_csv", lambda f, data, fields: save_csv(f.replace("data", TEST_DATA_DIR), data, fields))

    # Issue the book
    issue_book()

    # Verify CopiesAvailable is now 0
    books_after_issue = load_csv(test_books_file)
    assert books_after_issue[0]["CopiesAvailable"] == "0"

    # Get loan ID from loans.csv for return test
    loans = load_csv(test_loans_file)
    loan_id = loans[0]["LoanID"]

    # Monkeypatch input() for return_book()
    monkeypatch.setattr("builtins.input", lambda prompt="": {
        "Loan ID: ": loan_id
    }[prompt])

    # Return the book
    return_book()

    # Verify CopiesAvailable restored to 1
    books_after_return = load_csv(test_books_file)
    assert books_after_return[0]["CopiesAvailable"] == "1"
