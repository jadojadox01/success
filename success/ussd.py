import json

class User:
    def __init__(self, phone_number, balance=0):
        self.phone_number = phone_number
        self.balance = balance

    def send_money(self, receiver, amount):
        if self.balance >= amount:
            self.balance -= amount
            receiver.balance += amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def to_dict(self):
        return {'phone_number': self.phone_number, 'balance': self.balance}

    @staticmethod
    def from_dict(data):
        return User(data['phone_number'], data['balance'])


class USSDSession:
    def __init__(self, data_file='users.json'):
        self.data_file = data_file
        self.users = self.load_users()
    
    def load_users(self):
        try:
            with open(self.data_file, 'r') as f:
                users_data = json.load(f)
                return {phone: User.from_dict(data) for phone, data in users_data.items()}
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.data_file, 'w') as f:
            json.dump({phone: user.to_dict() for phone, user in self.users.items()}, f)
    
    def add_user(self, phone_number, balance):
        self.users[phone_number] = User(phone_number, balance)
        self.save_users()
    
    def get_user(self, phone_number):
        return self.users.get(phone_number, None)
    
    def start_session(self):
        while True:
            print("\nWelcome to the USSD Money Transfer Service")
            phone_number = input("Enter your phone number (or type 'register' to sign up): ")

            if phone_number.lower() == 'register':
                self.register_user()
                continue
            
            user = self.get_user(phone_number)
            
            if not user:
                print("Phone number not registered. Please try again.")
                continue
            
            print("\n1. Send Money")
            print("2. Check Balance")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.send_money(user)
            elif choice == '2':
                print(f"Your balance is: {user.get_balance()}")
            elif choice == '3':
                print("Thank you for using the USSD Money Transfer Service.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def register_user(self):
        phone_number = input("Enter new phone number: ")
        if self.get_user(phone_number):
            print("Phone number already registered.")
            return
        balance = float(input("Enter initial balance: "))
        self.add_user(phone_number, balance)
        print(f"User registered with phone number {phone_number} and balance {balance}.")
    
    def send_money(self, sender):
        receiver_number = input("Enter receiver's phone number: ")
        amount = float(input("Enter amount to send: "))
        receiver = self.get_user(receiver_number)

        if not receiver:
            print("Receiver's phone number not registered.")
        elif sender.send_money(receiver, amount):
            self.save_users()
            print(f"Successfully sent {amount} to {receiver_number}")
            print(f"Your new balance is: {sender.get_balance()}")
            print(f"Receiver's new balance is: {receiver.get_balance()}")
        else:
            print("Insufficient balance to send money.")

if __name__ == "__main__":
    ussd_session = USSDSession()
    
    # Optionally add some initial users for testing
    if not ussd_session.get_user("1234567890"):
        ussd_session.add_user("1234567890", 1000)  # User 1
    if not ussd_session.get_user("0987654321"):
        ussd_session.add_user("0987654321", 500)   # User 2
    
    ussd_session.start_session()
