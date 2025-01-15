from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

# Configure the session
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"


expenses = []  # Stores expenses as a list of dictionaries

@app.route("/")
def index():
    # Get the selected currency from the session, default to USD
    selected_currency = session.get("currency", "USD")

    # Calculate total in USD
    total_usd = sum(
        expense["amount"] if expense["currency"] == "USD" else expense["amount"] / 7.2
        for expense in expenses
    )
    return render_template("index.html", total_usd=total_usd, currency=selected_currency)

@app.route("/set_currency", methods=["POST"])
def set_currency():
    # Save the selected currency in the session
    session["currency"] = request.form["currency"]
    return redirect(url_for("index"))

@app.route("/add", methods=["POST"])
def add_expense():
    # Add a new expense with its currency
    amount = float(request.form["amount"])
    category = request.form["category"]
    currency = request.form["currency"]
    expenses.append({"amount": amount, "category": category, "currency": currency})
    return redirect(url_for("index"))

@app.route("/filter", methods=["GET"])
def filter_expenses():
    # Get the selected currency from the session, default to USD
    selected_currency = session.get("currency", "USD")

    # Calculate total in USD
    total_usd = sum(
        expense["amount"] if expense["currency"] == "USD" else expense["amount"] / 7.2
        for expense in expenses
    )
    return render_template("filter.html", expenses=expenses, total_usd=total_usd, currency=selected_currency)

@app.route("/remove", methods=["POST"])
def remove_expense():
    # Retrieve the expense details from the form
    amount = float(request.form["amount"])
    currency = request.form["currency"]
    category = request.form["category"]

    # Remove the matching expense
    global expenses
    expenses = [
        exp for exp in expenses
        if not (exp["amount"] == amount and exp["currency"] == currency and exp["category"] == category)
    ]
    return redirect(url_for("filter_expenses"))

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

