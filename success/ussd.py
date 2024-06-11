from flask import Flask, request, jsonify

app = Flask(__name__)

# User data stored in memory for simplicity
users = {
    "1234567890": {"balance": 1000},
    "0987654321": {"balance": 500}
}

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    if phone_number not in users:
        users[phone_number] = {"balance": 0}

    response = ""

    if text == "":
        response = "CON Welcome to Money Transfer Service\n1. Send Money\n2. Check Balance"
    elif text == "1":
        response = "CON Enter receiver's phone number:"
    elif text.startswith("1*"):
        parts = text.split('*')
        if len(parts) == 2:
            response = "CON Enter amount to send:"
        elif len(parts) == 3:
            receiver_number = parts[1]
            amount = float(parts[2])
            if receiver_number in users and users[phone_number]["balance"] >= amount:
                users[phone_number]["balance"] -= amount
                users[receiver_number]["balance"] += amount
                response = f"END Successfully sent {amount} to {receiver_number}.\nYour new balance is {users[phone_number]['balance']}."
            else:
                response = "END Transaction failed. Check receiver number or your balance."
    elif text == "2":
        response = f"END Your balance is {users[phone_number]['balance']}."
    else:
        response = "END Invalid input. Please try again."

    return response, 200

if __name__ == "__main__":
    app.run(debug=True)
