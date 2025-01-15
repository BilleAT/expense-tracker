from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
expenses = []  # Stores expenses as a list of dictionaries

@app.route("/")
def index():
    # Calculate total in USD
    total_usd = sum(
        expense["amount"] if expense["currency"] == "USD" else expense["amount"] / 7.2
        for expense in expenses
    )
    return render_template("index.html", total_usd=(total_usd))

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
    # Calculate total in USD
    total_usd = sum(
        expense["amount"] if expense["currency"] == "USD" else expense["amount"] / 7.2
        for expense in expenses
    )
    return render_template("filter.html", expenses=expenses, total_usd=(total_usd))

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
