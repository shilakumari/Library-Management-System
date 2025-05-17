from dataclasses import dataclass
from datetime import date

@dataclass
class Book:
    ISBN: str
    Title: str
    Author: str
    CopiesTotal: int
    CopiesAvailable: int

@dataclass
class Member:
    MemberID: str
    Name: str
    PasswordHash: str
    Email: str
    JoinDate: str  # YYYY-MM-DD
    Role: str

@dataclass
class Loan:
    LoanID: str
    MemberID: str
    ISBN: str
    IssueDate: str  # YYYY-MM-DD
    DueDate: str    # YYYY-MM-DD
    ReturnDate: str # YYYY-MM-DD or blank

