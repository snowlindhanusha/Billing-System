import mysql.connector

def create_customer(cursor, customer_id, name, email, phone_no, address):
    query = """INSERT INTO Customers (Customer_ID, Name, Email, Phone_No, Address)
            VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (customer_id, name, email, phone_no, address))
    
def create_invoice(cursor, invoice_id, customer_id, payment_method, payment_date, payment_time):
    query = """INSERT INTO Invoices (Invoice_ID, Customer_ID, Payment_Method, Payment_Date, Payment_Time)
            VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (invoice_id, customer_id, payment_method, payment_date, payment_time))

def add_items_to_invoice(cursor, invoice_item_id, invoice_id, item_name, quantity, price):
    query = """INSERT INTO Invoice_Items (Invoice_Item_ID, Invoice_ID, Item_Name, Quantity, Price)
            VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (invoice_item_id, invoice_id, item_name, quantity, price))

def calculate_print_bill(cursor, invoice_id, carrybag, no_of_carrybag, carrybag_cost):
    print("\nGenerating bill for Invoice ID:", invoice_id)
    print("------------------------INVOICE--------------------------------")
    print("BILL")
    print(""" SMART SHOPPING SUPERMARKET
            No.4, Govindan Road, West Mambalam, Chennai-33
            Ph: 981XXXXXXX
            mail.care: smartshopping@gmail.com""")
    print("---------------------------------------------------------------")

    cursor.execute("SELECT * FROM Invoices WHERE Invoice_ID = %s", (invoice_id,))
    invoice = cursor.fetchone()
    if invoice:
        cursor.execute("SELECT Name, Email, Phone_No, Address FROM Customers WHERE Customer_ID = %s", (invoice[1],))
        customer = cursor.fetchone()
        if customer:
            print("Invoice ID:", invoice[0])
            print("Customer ID:", invoice[1])
            print("Customer Name:", customer[0])
            print("Customer Email:", customer[1])
            print("Customer Phone Number:", customer[2])
            print("Customer Address:", customer[3])
            print("Payment Method:", invoice[2])
            print("Payment Date:", invoice[3])
            print("Payment Time:", invoice[4])
            cursor.execute("""SELECT Item_Name, Quantity, Price FROM Invoice_Items
                               WHERE Invoice_ID = %s""", (invoice_id,))
            items = cursor.fetchall() 
            if items: 
                print("------------------------")
                for item in items:
                    print("Item Name:", item[0])
                    print("Quantity:", item[1])
                    print("Price:", item[2])

                subtotal = 0
                for item in items:  
                    subtotal += item[1] * item[2]

                tax_rate = 0.05
                tax_amount = subtotal * tax_rate
                print("Number of carrybags:", no_of_carrybag)
                print("Carrybag cost:", carrybag_cost)
                total = subtotal + tax_amount + carrybag_cost

                print("Subtotal:", subtotal)
                print("Tax Rate:", tax_rate)
                print("Tax Amount:", tax_amount)
                print("Carrybag Cost:", carrybag_cost)
                print("Total:", total)
                print("THANK YOU!!!,VISIT AGAIN")
            else:
                print("No items found for this invoice.")  

        else:
            print("Customer details not found.")
    else:
        print("Invoice not found.")

def main():
    connection = mysql.connector.connect(host="localhost",user="root",password="Snowsa@2007!",database="Bill")
    cursor = connection.cursor()
    
    while True:
        print("1. Add Customer")
        print("2. Create Invoice")
        print("3. Add Items to Invoice")
        print("4. Calculate and print bill")
        print("5.Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            customer_id = int(input("Enter Customer ID:"))
            name = input("Name: ")
            email = input("Email: ")
            phone_no = input("Phone No: ")
            address = input("Address: ")
            create_customer(cursor, customer_id, name, email, phone_no, address)
            connection.commit()
            print("Customer added successfully with ID:", customer_id)

        elif choice == 2:
            invoice_id = int(input("Enter Invoice ID:"))
            customer_id = int(input("Customer ID: "))
            payment_method = input("Payment Method: ")
            payment_date = input("Payment Date (YYYY-MM-DD): ")
            payment_time = input("Payment Time (HH:MM:SS): ")
            create_invoice(cursor, invoice_id, customer_id, payment_method, payment_date, payment_time)
            connection.commit()
            print("Invoice created successfully with ID:", invoice_id)


        elif choice == 3:
            invoice_id = int(input("Invoice ID: "))
            invoice_item_id = int(input("Enter Invoice Item ID:"))
            item_name = input("Item Name: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            add_items_to_invoice(cursor, invoice_item_id, invoice_id, item_name, quantity, price)
            connection.commit()
            print("Items added to invoice successfully.")
            print("Calculate")

        elif choice == 4:
            invoice_id = int(input("Invoice ID: "))
            carrybag = input("Does the customer want a carrybag? (Type Y for YES): ")
            if carrybag.lower() == "y":
                no_of_carrybag = int(input("Enter number of carrybags: "))
                carrybag_cost = 4 * no_of_carrybag
            else:
                carrybag_cost = 0
            print("\nWould you like to calulate and print the bill for this invoice? (yes/no):")
            calculate_print_bill_choice = input().lower()
            if calculate_print_bill_choice == 'yes':
                calculate_print_bill(cursor, invoice_id,carrybag,no_of_carrybag,carrybag_cost)


        elif choice == 5:
            break

        else:
            print("Invalid choice. Please try again.")

    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

if __name__=="__main__":
    
    main()

