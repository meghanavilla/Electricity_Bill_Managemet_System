import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Function to connect to the database
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Meghana@2005",  # Replace with your MySQL password
            database="ElectricityBillManagement"  # Corrected database name
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Database connection
db = connect_to_database()
if db:
    cursor = db.cursor()
else:
    exit()

# Function to authenticate user
def login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        query = "SELECT * FROM Users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error querying database: {err}")
        return

    if result:
        messagebox.showinfo("Login", "Login Successful")
        user_id.set(result[0])
        root.destroy()
        open_main_app()
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Function to open the main application after login
def open_main_app():
    main_app = tk.Tk()
    main_app.title("Electricity Bill Management System")

    tk.Label(main_app, text="Welcome to the Electricity Bill Management System").pack()

    def view_bills():
        user_id_val = user_id.get()
        try:
            query = """
            SELECT amount, due_date, paid 
            FROM Bills
            WHERE user_id = %s
            """
            cursor.execute(query, (user_id_val,))
            bills = cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error querying database: {err}")
            return

        if not bills:
            messagebox.showinfo("No Bills", "No bills found for this user.")
        else:
            for bill in bills:
                tk.Label(main_app, text=f"Amount: {bill[0]}, Due Date: {bill[1]}, Paid: {bill[2]}").pack()

    def pay_bill():
        user_id_val = user_id.get()
        try:
            query = "SELECT id, amount, due_date FROM Bills WHERE user_id = %s AND paid = FALSE"
            cursor.execute(query, (user_id_val,))
            unpaid_bills = cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error querying database: {err}")
            return

        if not unpaid_bills:
            messagebox.showinfo("No Unpaid Bills", "No unpaid bills found.")
        else:
            for bill in unpaid_bills:
                bill_info = f"ID: {bill[0]}, Amount: {bill[1]}, Due Date: {bill[2]}"
                bill_label = tk.Label(main_app, text=bill_info)
                bill_label.pack()
                tk.Button(main_app, text="Pay Now", command=lambda b_id=bill[0]: process_payment(b_id, bill_label)).pack()

    def process_payment(bill_id, label):
        try:
            update_query = "UPDATE Bills SET paid = TRUE WHERE id = %s"
            cursor.execute(update_query, (bill_id,))
            db.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating database: {err}")
            return

        label.config(text=f"Bill ID {bill_id} - Paid")
        messagebox.showinfo("Payment", f"Bill ID {bill_id} has been paid.")

    tk.Button(main_app, text="View Bills", command=view_bills).pack()
    tk.Button(main_app, text="Pay Bill", command=pay_bill).pack()

    main_app.mainloop()

# GUI setup
root = tk.Tk()
root.title("Electricity Bill Management System - Login")

user_id = tk.IntVar()

tk.Label(root, text="Username").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password").grid(row=1, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2)

root.mainloop()

# Close the cursor and database connection
cursor.close()
db.close()
