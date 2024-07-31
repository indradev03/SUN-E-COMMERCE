from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
from tkinter import Toplevel


# Initialize root window
root = Tk()
root.iconbitmap("icon.ico")
root.title("SUN e Shopping")
root.minsize(600, 300)
root.configure(bg='#fff')
root.resizable(False, False)

# Create or connect to the database
def initialize_db():
    with sqlite3.connect('signup.db') as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS user (
                signup_fname TEXT,
                signup_lname TEXT,
                signup_phone TEXT,
                signup_email TEXT,
                signup_username TEXT PRIMARY KEY,
                signup_password TEXT
            )
        """)
        conn.commit()

initialize_db()

# DASHBOARD BOARD FOR SELLERS 

# Function to create the purchases table if it doesn't exist
def create_purchase_table():
    conn = sqlite3.connect('shopping.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        product_name TEXT,
        price REAL,
        purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    
create_purchase_table()   

# Prices for the products on each page
prices = {
    1: ['Rs.500', 'Rs.300', 'Rs.300', 'Rs.800', 'Rs.1200', 'Rs.1200'],
    2: ['Rs.1200', 'Rs.300', 'Rs.1200', 'Rs.1200', 'Rs.800', 'Rs.1200'],
    3: ['Rs.400', 'Rs.1200', 'Rs.2000', 'Rs.400', 'Rs.300', 'Rs.300']
}
# images of the products that will displays on each page
product_images = {
    1: ['tshirt1.jpg', 'tshirt2.jpg', 'tshirt3.jpg', 'Shirt1.jpg', 'hoddie1.jpg', 'hoddei2.jpg'],
    2: ['hoddie5.jpg', 'vest3.jpg', 'hoddie6.jpg', 'hoddie7.jpg', 'shirt2.jpg', 'hoddie8.jpg'],
    3: ['tshirt4.jpg', 'hoddie3.jpg', 'hoddie4.jpg', 'tshirt5.jpg', 'vest1.jpg', 'vest2.jpg']
}

# FUNCTIONS FOR PRODUCTS DISPLAY AND MANAGEMENT

#For Save edit prices
def save_prices(page, entries): 
    for i, entry in enumerate(entries): 
        prices[page][i] = entry.get()

#For Delete the Product
def delete_product(page, index): 
    prices[page].pop(index)
    product_images[page].pop(index)
    if messagebox.askyesno("Delete", "Are you sure you want to Delete this product?"):
        messagebox.showinfo("Delete", " Your products have been succesfully delete")
    update_product_display(page)

# After Saving edit prices Or Delete products this code update the dashboard after changes
def update_product_display(page): 
    for widget in root.winfo_children():
        if isinstance(widget, Frame) and widget.winfo_x() == 152 and widget.winfo_y() == 41:
            widget.destroy()

    entries = create_product_frame(root, page, product_images[page])
    create_navigation_buttons(page, entries)
    
#  To show the products in the dashboard
def create_product_frame(parent, page, images):
    product_frame = Frame(parent, width=450, height=325, bg='white')
    product_frame.place(x=152, y=41)

    frames = [Frame(product_frame, width=125, height=120, bg='white') for _ in range(len(prices[page]))]
    positions = [(15, 5), (163, 5), (310, 5), (15, 160), (163, 160), (310, 160)]

    for frame, pos in zip(frames, positions):
        frame.place(x=pos[0], y=pos[1])

    entries = []
    for i, frame in enumerate(frames):
        if i < len(images):
            img = Image.open(images[i])
            photo = ImageTk.PhotoImage(img)
            img_label = Label(frame, image=photo, width=100, height=100, bg='white')
            img_label.place(x=10, y=0)
            img_label.image = photo

            price_entry = Entry(frame, font=('Arial', 8), bg='white')
            price_entry.insert(0, prices[page][i])
            price_entry.place(x=25, y=100)
            entries.append(price_entry)

            delete_button = Button(frame, text='Delete', font=('Arial', 8), command=lambda index=i: delete_product(page, index), bg='red', fg='white')
            delete_button.place(x=85, y=97)

    return entries

# Display First page products 
def first_page_products():
    entries = create_product_frame(root, 1, product_images[1])
    create_navigation_buttons(1, entries)
    
# Display second page products 
def second_page_products():
    entries = create_product_frame(root, 2, product_images[2])
    create_navigation_buttons(2, entries)
    
# Display Third page products 
def third_page_products():
    entries = create_product_frame(root, 3, product_images[3])
    create_navigation_buttons(3, entries)
    
# Save button in the productt page 
def create_navigation_buttons(current_page, entries):
    save_button = Button(root, text='Save', command=lambda: save_prices(current_page, entries), bg='white', fg='green', font=('Arial', 8))
    save_button.place(x=530, y=330)

# Products Pages button
    Button(root, text='1', command=first_page_products, border=1, bg='white').place(x=340, y=330)
    Button(root, text='2', command=second_page_products, border=1, bg='white').place(x=370, y=330)
    Button(root, text='3', command=third_page_products, border=1, bg='white').place(x=400, y=330)

# Functions for showing different sections of the SELLERS DASHBOARD
def show_dashboard(username, account_type):
    login_frame.pack_forget()
    signup_frame.pack_forget()
    forgetpassword_frame.pack_forget()
    left_frame.pack_forget()
    header.pack_forget()

# Initally Show Homepage of dashboard
    show_homepage()

# Upper Frame
    dashboard_frame = Frame(root, width=600, height=40, bg='lightgrey')
    dashboard_frame.place(x=100, y=0)
    
# Lefside frame contains different buttons
    dashboard_left = Frame(root, width=150, height=400, bg='lightgrey', highlightbackground='grey', highlightcolor='grey', highlightthickness=2)
    dashboard_left.place(x=0, y=0)
    
# logo in the dashboard left frame
    logo = Image.open('smallLogo.jpg')
    photo1 = ImageTk.PhotoImage(logo)
    logo_label = Label(dashboard_left, image=photo1, width=50, height=40, bg='white')
    logo_label.place(x=8, y=0)
    logo_label.image = photo1

# SEARCH BAR
    setup_search_bar(dashboard_frame)
    create_sidebar_buttons(dashboard_left, username)

def setup_search_bar(frame):
    def on_enter(e):
        if search_entry.get() == 'Search':
            search_entry.delete(0, END)

    def on_leave(e):
        if search_entry.get() == '':
            search_entry.insert(0, 'Search')

    search_entry = Entry(frame, font=('Arial', 12), bg='white', width=20)
    search_entry.place(x=80, y=10)
    search_entry.insert(0, 'Search')
    search_entry.bind('<FocusIn>', on_enter)
    search_entry.bind('<FocusOut>', on_leave)

    search_btn = Button(frame, text='Search', command=lambda: None)
    search_btn.place(x=270, y=10)


# Homepage of Dashboard
def show_homepage():
    homepage_frame = Frame(root, width=450, height=325, bg='white')
    homepage_frame.place(x=152, y=41)
    Label(homepage_frame, text='WEL-COME \n TO \n SUN \n E-SHOPPING', bg = 'white' ,font=('Arial', 20, 'bold')).place(x=230, y=85)
    
    logo = Image.open('mediumlogo.jpg')
    photo = ImageTk.PhotoImage(logo)
    photolbl = Label(homepage_frame, image=photo, bg='white')
    photolbl.image = photo  # Keep a reference to avoid garbage collection
    photolbl.place(x=30, y=41)

    # Function to handle logout with conditions
def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            # Perform the logout operation
            messagebox.showinfo("Logout", "You have been logged out.")
            root.destroy()
    

# Button that are displayed in Dashboard left frame
def create_sidebar_buttons(parent, username):
    Button(parent, text="Home", width=15, command=show_homepage, bg='light grey').place(x=16, y=80)
    Button(parent, text="Products", command=first_page_products, width=15, bg='light grey').place(x=16, y=120)
    Button(parent, text="Orders", command=lambda: show_order_history(username), width=15, bg='light grey').place(x=16, y=160)
    Button(parent, text='Account', width=15, command=lambda: Account(username), bg='light grey').place(x=16, y=200)
    Button(parent, text='Logout', width=15,command=logout, bg='light grey').place(x=16, y=240)
    

# This will show order history in seller account which is ordered/purchased by the buyers

def show_order_history(username):
    orders_frame = Frame(root, width=450, height=325, bg='white')
    orders_frame.place(x=152, y=41)
    Label(orders_frame, text='Orders lists', font=('Arial',18, 'bold'), bg='white').place(x=20, y=20)

    try:
        with sqlite3.connect('shopping.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT username,product_name, price, purchase_time FROM purchases WHERE username = ?", (username,))
            purchases = cur.fetchall()

        if purchases:
            for i, purchase in enumerate(purchases):
                Label(orders_frame, text=f"Name: {purchase[0]}", bg='white', font=('Arial', 8)).place(x=10, y=60 + i * 40)
                Label(orders_frame, text=f"Product: {purchase[1]}", bg='white', font=('Arial', 8)).place(x=90, y=60 + i * 40)
                Label(orders_frame, text=f"Price: {purchase[2]}", bg='white', font=('Arial', 8)).place(x=190, y=60 + i * 40)
                Label(orders_frame, text=f"Date: {purchase[3]}", bg='white', font=('Arial', 8)).place(x=270, y=60 + i * 40)
                
        else:
            Label(orders_frame, text='No order history found', bg='white', font=('Arial', 8)).place(x=30, y=60)

        
        
        # Add a button to complete the order
        complete_order_btn = Button(orders_frame, text='Complete Order', command=order_completed, bg='green', fg='white')
        complete_order_btn.place(x=320, y=270)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        

# Order Completed Button
def order_completed():
    messagebox.showinfo("Order Completed", "These order has been successfully placed!")
    
    
# THIS WILL SHOWS THE DETAILS OF THE USER IN THE DASHBOARD WHICH WAS  FILLED DURING SIGNUP TIME
def Account(username):
    account_frame = Frame(root, width=450, height=325, bg='white')
    account_frame.place(x=152, y=41)

    try:
        with sqlite3.connect('signup.db') as conn: #Connects signup data here
            c = conn.cursor()
            c.execute("SELECT signup_fname, signup_lname, signup_email, signup_phone FROM user WHERE signup_username = ?", (username,))
            user = c.fetchone()

        if user:
            create_account_details_frame(account_frame, user, username)
        else:
            Label(account_frame, text='No account found', font=('Arial', 14)).place(x=30, y=60)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

# This will show the details in dashboard
def create_account_details_frame(parent, user, username):
    Label(parent, text='Account Details', bg='white', font=('Arial', 20)).place(x=30, y=20)
    
    labels = ["First Name:", "Last Name:", "Email:", "Phone:"]
    entries = []
    
    for i, label in enumerate(labels):
        Label(parent, text=label, bg='white', font=('Arial', 14)).place(x=30, y=60 + i * 40)
        entry = Entry(parent, font=('Arial', 14))
        entry.place(x=180, y=60 + i * 40)
        entry.insert(0, user[i])
        entries.append(entry)

    Button(parent, text='Save Changes', command=lambda: save_changes(entries, username), bg='lightgrey').place(x=180, y=220)
    
# This code helps to save the changes in account details and at the same time the database table deatils also changed
def save_changes(entries, username):
    new_data = [entry.get() for entry in entries]
    
    try:
        with sqlite3.connect('signup.db') as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE user
                SET signup_fname = ?, signup_lname = ?, signup_email = ?, signup_phone = ?
                WHERE signup_username = ?
            """, (*new_data, username))
            conn.commit()
        messagebox.showinfo("Update Successful", "Account details updated successfully")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        


# DASHBOARD FOR BUYERS

# Function to show the dashboard
def show_dashboard1(username, account_type):
    # Hide other frames
    login_frame.pack_forget()
    signup_frame.pack_forget()
    forgetpassword_frame.pack_forget()
    left_frame.pack_forget()
    header.pack_forget()
    
    # initially show homepage
    show_homepage()
    
    # Dashboard Setup For upper frame
    dashboard_frame1 = Frame(root, width=600, height=40, bg='lightgrey')
    dashboard_frame1.place(x=100, y=0)
    # Lefside frame contains different buttons
    dashboard_left = Frame(root, width=150, height=400, bg='lightgrey', highlightbackground='grey', highlightcolor='grey', highlightthickness=2)
    dashboard_left.place(x=0, y=0)

    # logo in the dashboard left frame
    logo = Image.open('smallLogo.jpg')
    photo1 = ImageTk.PhotoImage(logo)
    logo_label = Label(dashboard_left, image=photo1, width=50, height=40, bg='white')
    logo_label.place(x=8, y=0)
    logo_label.image = photo1  # Keep a reference

    # Image storage for product images
    image_references = []

    # SEARCH BAR SETUP FOR SEARCHING THE PRODUCTS 
    def setup_search_bar(frame):
        product_frame1 = Frame(root, width=450, height=325, bg='white')
        product_frame1.place(x=152, y=41)

        search_entry = Entry(frame, font=('Arial', 12), bg='white', width=20)
        search_entry.place(x=80, y=10)
        search_entry.insert(0, 'Search')
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, END) if search_entry.get() == 'Search' else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, 'Search') if search_entry.get() == '' else None)

        search_btn = Button(frame, text='Search', command=lambda: search_products(product_frame1, search_entry.get().lower()))
        search_btn.place(x=270, y=10)

    def search_products(product_frame1, search_term):
        for widget in product_frame1.winfo_children():
            widget.destroy()
        
        # Combine all product data
        all_products = first_page + second_page + third_page

        # Filter products based on the search term
        filtered_products = [(name, price, img_path) for (name, price, img_path) in all_products if search_term in name.lower()]

        create_product_page(filtered_products, search_term)
        
    setup_search_bar(dashboard_frame1)

    # Function to handle purchases and save them in the database
    def confirm_purchase(product_name, price):
        def on_confirm(payment_method):
            conn = sqlite3.connect('shopping.db')
            cur = conn.cursor()
            
            # Insert the purchase information into the purchases table
            cur.execute('''
            INSERT INTO purchases (username, product_name, price)
            VALUES (?, ?, ?)
            ''', (username, product_name, price))
            
            conn.commit()
            conn.close()
            if messagebox.askyesno("Purchase", "Are you sure you want to purchse this item?"):
                messagebox.showinfo("Purchase", f"You have purchased {product_name} for Rs.{price} using {payment_method}!")
            
            popup.destroy()

        def on_cancel():
            popup.destroy()

        # PAYMENT POPOUT
        popup = Toplevel(root)
        popup.title("Confirm Purchase")
        popup.geometry("300x250")

        Label(popup, text=f"Do you want to purchase {product_name} for Rs.{price}?", font=('Arial', 10)).pack(pady=20)

        Label(popup, text="Select Payment Method:", font=('Arial', 10)).pack()
        payment_method_var = StringVar()
        payment_method_var.set("Mobile Baking")
        payment_methods = ["Khalti", "Mobile Banking", "e-sewa"]
        OptionMenu(popup, payment_method_var, *payment_methods).pack(pady=10)

        Button(popup, text="Confirm", command=lambda: on_confirm(payment_method_var.get())).pack(side=LEFT, padx=30)
        Button(popup, text="Cancel", command=on_cancel).pack(side=RIGHT, padx=30)

    # Function to load and keep image references
    def load_image(path):
        img = Image.open(path)
        photo_image = ImageTk.PhotoImage(img)
        image_references.append(photo_image)  # Store a reference
        return photo_image

    # Product Page Creation
    def create_product_page(products, search_term=''):
        product_frame = Frame(root, width=450, height=325, bg='white')
        product_frame.place(x=152, y=41)

        for index, (product_name, price, img_path) in enumerate(products):
            if search_term in product_name.lower() or search_term == '':
                frame = Frame(product_frame, width=125, height=120, bg='white')
                frame.place(x=(index % 3) * 148 + 15, y=(index // 3) * 155 + 5)

                Button(frame, text='Buy', bg='white', border=0, fg='green', font=('Arial', 8),
                        command=lambda name=product_name, price=price: confirm_purchase(name, price)).place(x=70, y=100)
                Label(frame, text=f'Rs.{price}', font=('Arial', 8), bg='white').place(x=25, y=100)

                product_image = load_image(img_path)
                img_label = Label(frame, image=product_image, bg='white')
                img_label.place(x=10, y=0)
                img_label.image = product_image  # Keep a reference
                
                # Add price label below the image
                Label(frame, text=f'Rs.{price}', font=('Arial', 8), bg='white').place(x=30, y=103)

                # Add buy button below the price label
                Button(frame, text='Buy', bg='white', border=0, fg='green', font=('Arial', 8),
                    command=lambda name=product_name, price=price: confirm_purchase(name, price)).place(x=80, y=103)

        # Products Pages button
        Button(product_frame, text='1', command=lambda: create_product_page(first_page, search_term), border=1, bg='white').place(x=190, y=290)
        Button(product_frame, text='2', command=lambda: create_product_page(second_page, search_term), border=1, bg='white').place(x=220, y=290)
        Button(product_frame, text='3', command=lambda: create_product_page(third_page, search_term), border=1, bg='white').place(x=250, y=290)

    # Function to retrieve and display purchase history
    def show_purchase_history():
        # Create a new window
        history_window = Toplevel(root)
        history_window.title("Purchase History")
        history_window.geometry("600x300")
        history_window.resizable(False, False)

        # Create a treeview to display the purchase history
        columns = ("id", "product_name", "price")
        tree = ttk.Treeview(history_window, columns=columns, show="headings")
        tree.heading("id", text="ID")
        tree.heading("product_name", text="Product Name")
        tree.heading("price", text="Price")
        tree.pack(fill=BOTH, expand=True)

        # Connect to the database and fetch purchase history
        conn = sqlite3.connect('shopping.db')
        cur = conn.cursor()
        cur.execute('''
        SELECT id, product_name, price, purchase_time FROM purchases WHERE username=?''', (username,))
        rows = cur.fetchall()
        conn.close()

        # Insert the purchase records into the treeview
        for row in rows:
            tree.insert("", END, values=row)

        # Function to delete selected purchase history
        def delete_purchase_history():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("Delete", "No items selected to delete.")
                return
            
            conn = sqlite3.connect('shopping.db')
            cur = conn.cursor()
            
            for item in selected_items:
                if messagebox.askyesno("Delete", "Are you sure you want to delete?"):
                    item_id = tree.item(item, "values")[0]
                    cur.execute('DELETE FROM purchases WHERE id=?', (item_id,))
                    tree.delete(item)
            
                conn.commit()
                conn.close()
                messagebox.showinfo("Delete", "Selected purchase history deleted successfully.")

        # Add a Delete button to the history window t0 delete the purchase history
        delete_btn = Button(history_window, text="Delete Selected", command=delete_purchase_history)
        delete_btn.pack(pady=10)

    # Product Data(PRODUCT_NAME, PRICE, IMGAE_LOACTION)
    first_page = [
        ('TShirt 1', 500, 'tshirt1.jpg'),
        ('TShirt 2', 300, 'tshirt2.jpg'),
        ('TShirt 3', 300, 'tshirt3.jpg'),
        ('Shirt 1', 800, 'Shirt1.jpg'),
        ('Hoodie 1', 1200, 'hoddie1.jpg'),
        ('Hoodie 2', 1200, 'hoddei2.jpg')
    ]

    second_page = [
        ('Hoodie 5', 1200, 'hoddie5.jpg'),
        ('Vest 3', 300, 'vest3.jpg'),
        ('Hoodie 6', 1200, 'hoddie6.jpg'),
        ('Hoodie 7', 1200, 'hoddie7.jpg'),
        ('Shirt 2', 800, 'shirt2.jpg'),
        ('Hoodie 8', 1200, 'hoddie8.jpg')
    ]

    third_page = [
        ('TShirt 4', 400, 'tshirt4.jpg'),
        ('Hoodie 3', 1200, 'hoddie3.jpg'),
        ('Hoodie 4', 2000, 'hoddie4.jpg'),
        ('T-Shirt 5', 400, 'tshirt5.jpg'),
        ('Vest 1', 300, 'vest1.jpg'),
        ('Vest 2', 300, 'vest2.jpg')
    ]


    # HOMEPAGE OF BUYERS DASHBOARD
    def homepage():
        homepage_frame = Frame(root, width=450, height=325, bg='white')
        homepage_frame.place(x=152, y=41)
        Label(homepage_frame, text='WEL-COME \n TO \n SUN \n E-SHOPPING', bg = 'white' ,font=('Arial', 20, 'bold')).place(x=230, y=85)
        logo = Image.open('mediumlogo.jpg')
        photo = ImageTk.PhotoImage(logo)
        photolbl = Label(homepage_frame, image=photo, bg='white')
        photolbl.image = photo  # Keep a reference to avoid garbage collection
        photolbl.place(x=30, y=41)

    # Function to handle logout with conditions
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            # Perform the logout operation
            messagebox.showinfo("Logout", "You have been logged out.")
            root.destroy()


    # THIS WILL SHOWS THE DETAILS OF THE USER IN THE DASHBOARD WHICH WAS  FILLED DURING SIGNUP TIME
    def account_details(username):
        account_frame = Frame(root, width=450, height=325, bg='white')
        account_frame.place(x=152, y=41)

        try:
            with sqlite3.connect('signup.db') as conn:
                c = conn.cursor()
                c.execute("SELECT signup_fname, signup_lname, signup_email, signup_phone FROM user WHERE signup_username = ?", (username,))
                user = c.fetchone()
                
            # This will show the details in dashboard
            if user:
                Label(account_frame, text='Account Details', bg='white', font=('Arial', 20)).place(x=30, y=20)
                
                labels = ["First Name:", "Last Name:", "Email:", "Phone:"]
                entries = []
                for idx, label in enumerate(labels):
                    Label(account_frame, text=label, bg='white', font=('Arial', 14)).place(x=30, y=60 + idx * 40)
                    entry = Entry(account_frame, font=('Arial', 14))
                    entry.place(x=180, y=60 + idx * 40)
                    entry.insert(0, user[idx])
                    entries.append(entry)
                    
                # This code helps to save the changes in account details and at the same time the database table deatils also change
                def save_changes():
                    new_values = [entry.get() for entry in entries]
                    try:
                        with sqlite3.connect('signup.db') as conn:
                            c = conn.cursor()
                            c.execute("""
                                UPDATE user
                                SET signup_fname = ?, signup_lname = ?, signup_email = ?, signup_phone = ?
                                WHERE signup_username = ?
                            """, (*new_values, username))
                            conn.commit()
                        messagebox.showinfo("Update Successful", "Account details updated successfully")
                    except sqlite3.Error as e:
                        messagebox.showerror("Database Error", str(e))

                Button(account_frame, text='Save Changes', command=save_changes, bg='lightgrey').place(x=180, y=220)
            else:
                Label(account_frame, text='No account found', font=('Arial', 14)).place(x=30, y=60)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    # Sidebar Buttons of Buyers ID
    Button(dashboard_left, text="Home", width=15, command=homepage, bg='lightgrey').place(x=16, y=80)
    Button(dashboard_left, text="Products", width=15, command=lambda: create_product_page(first_page), bg='lightgrey').place(x=16, y=120)
    Button(dashboard_left, text='Account', width=15, command=lambda: account_details(username), bg='lightgrey').place(x=16, y=160)
    
    # Add a Retrieve button to the dashboard to show purchase history
    retrieve_btn = Button(dashboard_left, width=15, text="Purchase History", bg='light grey', command=show_purchase_history)
    retrieve_btn.place(x=16, y=200)
    Button(dashboard_left, text='Logout', width=15,command=logout, bg='lightgrey').place(x=16, y=240)
    

    # initally show homepage
    homepage()
    
# To destory the another frames
def show_signup():
    login_frame.pack_forget()
    forgetpassword_frame.pack_forget()
    signup_frame.pack(fill=BOTH, expand=True, side=RIGHT)

def show_login():
    signup_frame.pack_forget()
    forgetpassword_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=True, side=RIGHT)

def show_forgetpassword():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    forgetpassword_frame.pack(fill=BOTH, expand=True, side=RIGHT)

# Header
header = Frame(root, bg='white')
header.pack(side=TOP, fill=X)

# create a frame in the leftside for customer support
header_left = Frame(header, bg='white')
header_left.pack(side=LEFT)
Button(header_left, text="Customer Support", bg='light grey').pack(side=LEFT, padx=10)

# create a frame in the rightside to display these buttons
header_right = Frame(header, bg='white')
header_right.pack(side=RIGHT)
Button(header_right, text="Sign Up", command=show_signup, bg='light grey').pack(side=LEFT, padx=10)
Label(header_right, text="|", bg='white').pack(side=LEFT)
Button(header_right, text="Login", command=show_login, bg='light grey').pack(side=LEFT, padx=10)

# Main content Frame
main_content = Frame(root, bg='white')
main_content.pack(fill=BOTH, expand=True)

# Left Frame for IMAGE OF MAIN LOGO
left_frame = Frame(main_content, bg='white')
left_frame.pack(side=LEFT, fill=BOTH, expand=True)

# IMAGE OF MAIN LOGO
image = Image.open('Logo.ico')
photo = ImageTk.PhotoImage(image)
Label(left_frame, image=photo, bg='white').pack(expand=True) 

# Right Frame for LOGIN AND SIGNUP
right_frame = Frame(main_content, bg='white')
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Conditions that are applied during login
def login():
    account_type = login_account_type.get()
    username = login_name.get()
    password = login_password.get()

    try:
        with sqlite3.connect('signup.db') as conn:
            c = conn.cursor()
            c.execute("SELECT signup_password FROM user WHERE signup_username = ?", (username,))
            user = c.fetchone()

        if user:
            if user[0] == password:
                if account_type == 'Buyers':
                    show_dashboard1(username, account_type)
                elif account_type == 'Sellers':
                    show_dashboard(username, account_type)
                else:
                    messagebox.showerror('Login Failed', 'Choose a valid account type')
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        
# LOGIN FRAME
login_frame = Frame(right_frame, bg='white')
Label(login_frame, text="Login", font=("Arial", 20), bg='white').pack(pady=10)

# NAME
Label(login_frame, text="Name", bg='white').pack(pady=5)
login_name = Entry(login_frame)
login_name.pack(pady=5)

# PASSWORD
Label(login_frame, text="Password", bg='white').pack(pady=5)
login_password = Entry(login_frame, show="*")
login_password.pack(pady=5)

# radio buttons whether choose buyers or sellers account
login_account_type = StringVar(value="Buyers")
Radiobutton(login_frame, text="Sellers", variable=login_account_type, value="Sellers", bg='white').pack(pady=5)
Radiobutton(login_frame, text="Buyers", variable=login_account_type, value="Buyers", bg='white').pack(pady=5)

# BUTTON FOR LOGIN
Button(login_frame, text="Login", command=login, bg='light grey').pack(pady=10)

# BUTTON FOR RESET PASSWORD
Button(login_frame, text="Forgot Password?", command=show_forgetpassword, bg='light grey').pack(pady=5)

# Add "Don't have an account?" text and signup button
dont_have_account_frame = Frame(login_frame, bg='white')
dont_have_account_frame.pack(pady=5)

Label(dont_have_account_frame, text="Don't have an account?", bg='white').pack(side=LEFT)
Button(dont_have_account_frame, text="Sign Up", command=show_signup, bg='light grey').pack(side=LEFT, padx=5)


# Conditions that are applied during Signup
def signup():
    fname = signup_fname.get()
    lname = signup_lname.get()
    phone = signup_phone.get()
    email = signup_email.get()
    username = signup_username.get()
    password = signup_password.get()
    confirm_password = signup_confirm_password.get()
    account_type = signup_account_type.get()

    if all([fname, lname, phone, email, username, password, confirm_password]):
        if len(password) >= 8 and password == confirm_password:
            if password not in (fname, lname, phone, username):
                try:
                    with sqlite3.connect('signup.db') as conn:
                        c = conn.cursor()
                        # Check if username already exists
                        c.execute("SELECT 1 FROM user WHERE signup_username = ?", (username,))
                        if c.fetchone():
                            messagebox.showerror("Signup Error", "Username already exists.")
                            return
                        # Insert new user
                        c.execute("INSERT INTO user (signup_fname, signup_lname, signup_phone, signup_email, signup_username, signup_password) VALUES (?, ?, ?, ?, ?, ?)",
                                (fname, lname, phone, email, username, password))
                        conn.commit()
                    messagebox.showinfo("Signup", f"Signup Successful for {account_type}\nUsername: {username}")
                    show_login()
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))
            else:
                messagebox.showerror("Signup Error", "Password should not match any other criteria.")
        else:
            messagebox.showerror("Signup Error", "Passwords do not match or password is too short.")
    else:
        messagebox.showerror("Signup Error", "All fields must be filled.")
        
        
# SIGNUP FRAME
signup_frame = Frame(right_frame, bg='white')
Label(signup_frame, text="Signup", font=("Arial", 20), bg='white').pack(pady=10)

# FIRST NAME
Label(signup_frame, text="First Name", bg='white').pack(pady=5)
signup_fname = Entry(signup_frame)
signup_fname.pack(pady=5)

# LAST NAME
Label(signup_frame, text="Last Name", bg='white').pack(pady=5)
signup_lname = Entry(signup_frame)
signup_lname.pack(pady=5)

# PHONE NO.
Label(signup_frame, text="Phone No.", bg='white').pack(pady=5)
signup_phone = Entry(signup_frame)
signup_phone.pack(pady=5)

# EMAIL ID
Label(signup_frame, text="Email ID", bg='white').pack(pady=5)
signup_email = Entry(signup_frame)
signup_email.pack(pady=5)

# CREATE USERNAME
Label(signup_frame, text="Create a Username", bg='white').pack(pady=5)
signup_username = Entry(signup_frame)
signup_username.pack(pady=5)

# PASSWORD
Label(signup_frame, text="Create a Password", bg='white').pack(pady=5)
signup_password = Entry(signup_frame, show="*")
signup_password.pack(pady=5)

Label(signup_frame, text="Confirm Password", bg='white').pack(pady=5)
signup_confirm_password = Entry(signup_frame, show="*")
signup_confirm_password.pack(pady=5)

# radio buttons whether choose buyers or sellers account
signup_account_type = StringVar(value="Buyers")
Radiobutton(signup_frame, text="Sellers", variable=signup_account_type, value="Sellers", bg='white').pack(side=LEFT, padx=10)
Radiobutton(signup_frame, text="Buyers", variable=signup_account_type, value="Buyers", bg='white').pack(side=LEFT, padx=10)

# BUTTON FOR SIGNUP
Button(signup_frame, text="Sign Up", command=signup, bg='light grey').pack(pady=10)

# Conditions that are applied during reset password
def forgetpassword():
    username = forget_fname.get()
    password = forget_password.get()
    confirm_password = forget_confirm_password.get()

    if all([username, password, confirm_password]):
        if len(password) >= 8 and password == confirm_password:
            if password != username:
                try:
                    with sqlite3.connect('signup.db') as conn:
                        c = conn.cursor()
                        c.execute("UPDATE user SET signup_password = ? WHERE signup_username = ?", (password,username))
                        conn.commit()
                    messagebox.showinfo("Password Reset", f"Password reset successful for {username}")
                    show_login()
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", str(e))
            else:
                messagebox.showerror("Password Reset Error", "Password should not match the username.")
        else:
            messagebox.showerror("Password Reset Error", "Passwords do not match or password is too short.")
    else:
        messagebox.showerror("Password Reset Error", "All fields must be filled.")
        
        
# FORGET PASSWORD FRAME
forgetpassword_frame = Frame(right_frame, bg='white')
Label(forgetpassword_frame, text="Reset Password", font=("Arial", 20), bg='white').pack(pady=10)

# username
Label(forgetpassword_frame, text="Username", bg='white').pack(pady=5)
forget_fname = Entry(forgetpassword_frame)
forget_fname.pack(pady=5)

# new password
Label(forgetpassword_frame, text="New Password", bg='white').pack(pady=5)
forget_password = Entry(forgetpassword_frame, show="*")
forget_password.pack(pady=5)
# confrim password
Label(forgetpassword_frame, text="Confirm Password", bg='white').pack(pady=5)
forget_confirm_password = Entry(forgetpassword_frame, show="*")
forget_confirm_password.pack(pady=5)

# BUTTON FOR RESET PASSWORD
Button(forgetpassword_frame, text="Reset Password", command=forgetpassword, bg='light grey').pack(pady=10)


# Initially show login page
show_login()

root.mainloop()
