import argparse
import auth
import librarian_menu
import member_menu
import storage
session = {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', default='data', help='Path to data directory')
    args = parser.parse_args()
    
    storage.set_data_dir(args.data_dir)
    
    print("=== Library Management System ===")
    while True:
        print("\nLogin as:")
        print("1. Librarian")
        print("2. Member")
        print("3. Exit")
        choice = input("> ")

        if choice == '1':
            user = auth.login('Librarian')
            if user:
                session['user'] = user
                librarian_menu.dashboard(session)

        elif choice == '2':
            user = auth.login('Member')
            if user:
                session['user'] = user
                member_menu.dashboard(session)

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
