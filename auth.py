import bcrypt
from storage import load_csv
from models import Member

MEMBERS_FILE = 'members.csv'

def login(role):
    members = load_csv(MEMBERS_FILE)
    member_id = input("Member ID: ")
    password = input("Password: ")
    for m in members:
        #print(bcrypt.hashpw(b'shila', bcrypt.gensalt()).decode())
        if m['MemberID'] == member_id and m['Role'] == role:
            if not bcrypt.checkpw(password.encode(), m['PasswordHash'].encode()):
                print("Password Mismatch")
            else:
                return m
    print("Login failed.")
    return None

def register_member():
    import uuid, datetime
    members = load_csv(MEMBERS_FILE)
    new_id = str(int(members[-1]['MemberID']) + 1 if members else 1001)
    
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    join_date = str(datetime.date.today())
    new_member = {'MemberID': new_id, 'Name': name, 'PasswordHash': hashed, 'Email': email, 'JoinDate': join_date}
    members.append(new_member)
    from storage import save_csv
    save_csv(MEMBERS_FILE, members, new_member.keys())
    print(f"Member {name} registered.")