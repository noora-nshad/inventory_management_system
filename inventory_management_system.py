import sqlite3
# import os
# print(os.path.abspath("inventory.db"))
conn=sqlite3.connect("inventory.db")
cursor=conn.cursor()
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS people(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
    )
    '''
)
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price TEXT,
    quantity INTEGER
    )
    '''
)
conn.commit()

# ---------------------------------LOGIN--------------------------------------------------------
def login():
    check=int(input("1.NEW LOGIN REGISTRATION \n 2.LOGIN\n"))
    if check==1:
        tname=input('user name:')
        tpass=input('password:')
        pass2=input('confirm password:')
        if tpass==pass2:
            trole=int(input('role:1.Admin\n2.Manager\n3.Employee'))
            if trole==1:
                trole='Admin'
            elif trole==2:
                trole='Manager'
            elif trole==3:
                trole='Employee'
            else:
                print('Invalid option!')
                login()
                return
            
            cursor.execute(
            '''
            INSERT INTO people(username,password,role)
                VALUES(?,?,?)
            ''',(tname,tpass,trole)
            )
            conn.commit()
            print("Login registered!!")
        else:
            print("password don't match,try again!")
        login()
        return
    
        # cursor.execute(
        #     '''
        #     INSERT INTO people(username,password,role)
        #         VALUES(?,?,?)
        #     ''',(tname,tpass,trole)
        # )
        
    elif check==2:
        user_name=input('Enter username:')
        password=input('Enter password:')
        cursor.execute(
            '''
            SELECT role FROM people WHERE username=? AND password=?
            ''',(user_name,password)
        )
        result=cursor.fetchone()
        if result:
            role=result[0]
            if role=="Admin":
                print("Admin login successful!")
                admin_menu()
            elif role=="Manager":
                print("Manager login successful!")
                manager_menu()
            elif role=="Employee":
                print("Employee login successful!")
                employee_menu()
        else:
            print("Invalid username or password!")
    else:
        print("Invalid selection")

 #---------------------------------PROCESS--------------------------------------------------   
def add_product():
    pro_name=input("Product name:")
    pro_categ=input("Category:")
    pro_price=float(input("Price:"))
    pro_quant=input("Quantity:")
    cursor.execute(
        '''
        INSERT INTO products(name,category,price,quantity)
        VALUES(?,?,?,?)
        ''',(pro_name,pro_categ,pro_price,pro_quant)
    )
    conn.commit()
    print("Product added!")

def del_product():
    pro_del=input("Enter product:")
    cursor.execute(
        '''
        SELECT * FROM products WHERE name=?
        ''',(pro_del,)
    )
    prod=cursor.fetchone()
    if prod:
        cursor.execute(
            '''
            DELETE FROM products WHERE name=?
            ''',(pro_del,)
        )
        print("product deleted!")
    else:
        print("invalid product!")

def update_product():
    pro_upd=input("Name of product:")
    cursor.execute(
        '''
        SELECT * FROM products WHERE name=?
        ''',(pro_upd,)
    )
    prod=cursor.fetchone()
    if prod:
        pro_qty=input("New quantity:")
        cursor.execute(
            '''
            UPDATE products SET quantity=? WHERE name=?
            ''',(pro_qty,pro_upd)
        )
        conn.commit()
        print("Stock Updated!")
    else:
        print("invalid product!")

def sear_product():
    prdct=input("Enter the name of product")
    cursor.execute(
        '''
        SELECT *FROM products WHERE name=?
        ''',(prdct,)
    )
    data=cursor.fetchall()
    for i in data:
        print(i)

def view_product():
    cursor.execute(
        '''
        SELECT * FROM products
        '''
    )
    data=cursor.fetchall()
    for i in data:
        print(f"ID: {i[0]}, Product: {i[1]}, Category: {i[2]}, Price: {i[3]}, Quantity: {i[4]}")

def sell_product():
    pro_sold=input("Name of product:")
    pro_qty=input("Quantity sold:")
    cursor.execute(
        '''
        SELECT * FROM products WHERE name=?
        ''',(pro_sold,)
    )
    stock=cursor.fetchone()
    if stock:
        rem=stock[0]-pro_qty
        cursor.execute(
            '''
            UPDATE products SET quantity=? WHERE name=?
            ''',(rem,pro_sold)
        )
        conn.commit()
        print("Poduct sold,Stock Updated!")
    else:
        print("invalid product!")

def view_people():
    cursor.execute(
        '''
        SELECT * FROM people
        '''
    )
    data = cursor.fetchall()
    
    if data:
        print("\n--- USERS LIST ---")
        for i in data:
            print(f"ID: {i[0]}, Username: {i[1]}, Role: {i[3]}")
    else:
        print("No users found!")


def del_people():
    peop_del=input("Enter user name:")
    cursor.execute(
        '''
        SELECT * FROM people WHERE username=?
        ''',(peop_del,)
    )
    prod=cursor.fetchone()
    if prod:
        cursor.execute(
            '''
            DELETE FROM people WHERE username=?
            ''',(peop_del,)
        )
        print("user deleted!")
    else:
        print("invalid username!")

#-----------------------------------------ROLE------------------------------------------------------
def admin_menu():
    while True:
        print("\nADMIN")
        print("\n1:Add product")
        print("\n2:Delete product")
        print("\n3:Update product")
        print("\n4:Search product")
        print("\n5:View product")
        print("\n6:View people")
        print("\n7:Remove people")
        print("\n8:Exit")

        n=int(input("Enter the choice:"))
        if n==1:
            add_product()
        elif n==2:
            del_product()
        elif n==3:
            update_product()
        elif n==4:
            sear_product()
        elif n==5:
            view_product()
        elif n==6:
            view_people()
        elif n==7:
            del_people()
        elif n==8:
            break

def manager_menu():
    while True:
        print("\nMANAGER")
        print("\n1:Update product")
        print("\n2:Search product")
        print("\n3:View product")
        print("\n4:View people")
        print("\n5:Exit")

        m=int(input("Enter the choice:"))
        if m==1:
            update_product()
        elif m==2:
            sear_product()
        elif m==3:
            view_product()
        elif m==4:
            view_people()
        elif m==5:
            break

def employee_menu():
    while True:
        print("\nEMPLOYER")
        print("\n1:Add product")
        print("\n2:Search product")
        print("\n3:Sell product")
        print("\n4:Exit")

        x=int(input("Enter the choice:"))
        if x==1:
            add_product()
        elif x==2:
            sear_product()
        elif x==3:
            sell_product()
        elif x==4:
            break
  
login()