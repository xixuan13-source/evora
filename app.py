from flask import Flask, render_template, redirect, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def get_cursor():
    connection = get_db_connection()
    return connection, connection.cursor()

@app.route("/")
def home():

    connection, cursor = get_cursor()

    cursor.execute("SELECT username FROM users WHERE user_id = 1")

    username = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template(
        "home.html",
        username=username
    )


@app.route("/dashboard")
def dashboard():

    connection, cursor = get_cursor()

    # Get username
    cursor.execute("SELECT username FROM users WHERE user_id = 1")
    username = cursor.fetchone()[0]

    # Get total expenses
    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_id = 1
    """)

    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("""
    SELECT COUNT(*)
    FROM expenses
    WHERE user_id = 1
    """)

    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT category_id)
    FROM expenses
    WHERE user_id = 1
    """)

    categories_used = cursor.fetchone()[0]

    cursor.execute("""
    SELECT
        c.category_name,
        SUM(e.amount) AS total_spent
    FROM expenses e
    JOIN categories c
        ON e.category_id = c.category_id
    WHERE e.user_id = 1
    GROUP BY c.category_name
    ORDER BY total_spent DESC
    LIMIT 1
    """)

    top_category = cursor.fetchone()

    # Get recent expenses
    cursor.execute("""
    SELECT
        e.description,
        c.category_name,
        e.amount
    FROM expenses e
    JOIN categories c
        ON e.category_id = c.category_id
    WHERE e.user_id = 1
    ORDER BY e.expense_date DESC
    LIMIT 5
    """)

    recent_expenses = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        username=username,
        total_expenses=total_expenses,
        total_transactions=total_transactions,
        categories_used=categories_used,
        top_category=top_category,
        recent_expenses=recent_expenses

    )

@app.route("/expenses")
def expenses():

    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT
            e.description,
            c.category_name,
            e.amount,
            e.expense_date
        FROM expenses e
        JOIN categories c
            ON e.category_id = c.category_id
        WHERE e.user_id = 1
        ORDER BY e.expense_date DESC
    """)

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "expenses.html",
        expenses=expenses
    )

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    connection, cursor = get_cursor()

    if request.method == "POST":

        description = request.form["description"].strip()
        if not description:
            return "Description is required"

        try:
            amount = float(request.form["amount"])

            if amount <= 0:
                return "Amount must be greater than 0"

        except ValueError:
            return "Invalid amount"
        
        category_id = request.form["category_id"]
        expense_date = request.form["expense_date"]

        cursor.execute("""
            INSERT INTO expenses
            (user_id, category_id, amount, description, expense_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            1,
            category_id,
            amount,
            description,
            expense_date
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect("/expenses")

    cursor.execute("""
        SELECT category_id, category_name
        FROM categories
    """)

    categories = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "expense_form.html",
        categories=categories
    )

@app.route("/budgets")
def budgets():

    connection, cursor = get_cursor()

    cursor.execute("""
        SELECT
            c.category_name,
            b.budget_amount
        FROM budgets b
        JOIN categories c
            ON b.category_id = c.category_id
        WHERE b.user_id = 1
    """)

    budgets = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "budgets.html",
        budgets=budgets
    )

@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    connection, cursor = get_cursor()

    if request.method == "POST":

        feedback_type = request.form["feedback_type"]
        comment = request.form["comment"].strip()

        if not comment:
            return "Comment is required"

        cursor.execute("""
            INSERT INTO feedback
            (user_id, feedback_type, comment)
            VALUES (%s, %s, %s)
        """, (
            1,
            feedback_type,
            comment
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/feedback")

    cursor.close()
    connection.close()

    return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)