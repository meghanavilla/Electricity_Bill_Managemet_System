import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk


# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Meghana@2005",
        database="electricity_billing"
    )


# Add Customer Function
def add_customer():
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    
    if name and address and phone:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)",
            (name, address, phone)
        )
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Customer added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


# Add Bill Function
def add_bill():
    customer_id = entry_customer_id.get()
    billing_date = entry_billing_date.get()
    due_date = entry_due_date.get()
    amount = entry_amount.get()
    status = entry_status.get()
    
    if customer_id and billing_date and due_date and amount and status:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO bills (customer_id, billing_date, due_date, amount, status) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, billing_date, due_date, amount, status)
        )
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Bill added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


# View Customers Function
def view_customers():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    db.close()
    customer_text.delete(1.0, END)
    for customer in customers:
        customer_info = f"ID: {customer[0]}, Name: {customer[1]}, Address: {customer[2]}, Phone: {customer[3]}\n"
        customer_text.insert(END, customer_info)


# View Bills Function
def view_bills():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM bills")
    bills = cursor.fetchall()
    db.close()
    bill_text.delete(1.0, END)
    for bill in bills:
        bill_info = f"ID: {bill[0]}, Customer ID: {bill[1]}, Billing Date: {bill[2]}, Due Date: {bill[3]}, Amount: {bill[4]}, Status: {bill[5]}\n"
        bill_text.insert(END, bill_info)


# Update Bill Status Function
def update_bill_status():
    bill_id = entry_bill_id.get()
    new_status = entry_new_status.get()
    
    if bill_id and new_status:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE bills SET status = %s WHERE bill_id = %s", 
            (new_status, bill_id)
        )
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Bill status updated successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")


# Main Window
root = Tk()
root.title("Electricity Bill Management")
root.geometry("800x600")

# Colors and Styles
bg_color = "#F9FAFC"
frame_color = "#FFFFFF"
button_color = "#4CAF50"
button_fg_color = "#FFFFFF"
text_color = "#333333"

# Fonts
header_font = ("Arial", 24, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Header
header_frame = Frame(root, bg=bg_color)
header_frame.pack(fill=X)
Label(header_frame, text="Electricity Bill Management", font=header_font, bg=bg_color, fg=text_color, padx=20, pady=10).pack()

# Notebook (Tabbed Interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill=BOTH)

# Customers Tab
customer_frame = Frame(notebook, bg=bg_color)
customer_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

Label(customer_frame, text="Customer Management", font=("Arial", 18, "bold"), bg=bg_color, fg=text_color).pack(pady=10)

Label(customer_frame, text="Name", bg=bg_color, fg=text_color, font=label_font).pack()
entry_name = Entry(customer_frame, font=label_font)
entry_name.pack()

Label(customer_frame, text="Address", bg=bg_color, fg=text_color, font=label_font).pack()
entry_address = Entry(customer_frame, font=label_font)
entry_address.pack()

Label(customer_frame, text="Phone", bg=bg_color, fg=text_color, font=label_font).pack()
entry_phone = Entry(customer_frame, font=label_font)
entry_phone.pack()

btn_add_customer = Button(customer_frame, text="Add Customer", bg=button_color, fg=button_fg_color, font=button_font, command=add_customer)
btn_add_customer.pack(pady=10)

btn_view_customers = Button(customer_frame, text="View Customers", bg=button_color, fg=button_fg_color, font=button_font, command=view_customers)
btn_view_customers.pack(pady=10)

customer_text = Text(customer_frame, height=10, wrap=WORD)
customer_text.pack(pady=10)

# Bills Tab
bill_frame = Frame(notebook, bg=bg_color)
bill_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

Label(bill_frame, text="Billing Management", font=("Arial", 18, "bold"), bg=bg_color, fg=text_color).pack(pady=10)

Label(bill_frame, text="Customer ID", bg=bg_color, fg=text_color, font=label_font).pack()
entry_customer_id = Entry(bill_frame, font=label_font)
entry_customer_id.pack()

btn_view_bills = Button(bill_frame, text="View Bills", bg=button_color, fg=button_fg_color, font=button_font, command=view_bills)
btn_view_bills.pack(pady=10)

bill_text = Text(bill_frame, height=10, wrap=WORD)
bill_text.pack(pady=10)

# Status Tab
status_frame = Frame(notebook, bg=bg_color)
status_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

Label(status_frame, text="Update Bill Status", font=("Arial", 18, "bold"), bg=bg_color, fg=text_color).pack(pady=10)

Label(status_frame, text="Bill ID", bg=bg_color, fg=text_color, font=label_font).pack()
entry_bill_id = Entry(status_frame, font=label_font)
entry_bill_id.pack()

Label(status_frame, text="New Status (PAID/UNPAID)", bg=bg_color, fg=text_color, font=label_font).pack()
entry_new_status = Entry(status_frame, font=label_font)
entry_new_status.pack()

btn_update_status = Button(status_frame, text="Update Status", bg=button_color, fg=button_fg_color, font=button_font, command=update_bill_status)
btn_update_status.pack(pady=10)

# Add Tabs to Notebook
notebook.add(customer_frame, text="Customers")
notebook.add(bill_frame, text="Bills")
notebook.add(status_frame, text="Bill Status")

root.mainloop()
