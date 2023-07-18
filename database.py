import sqlite3


#Invoice Table Creatation and Functions
def create_database():
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS invoice (
                invoice_id integer PRIMARY KEY,
                invoice_number text,
                invoice_date text,
                invoice_amount real,
                invoice_practice text,
                invoice_glcode number
                )""")
    conn.commit()
    conn.close()

def insert_invoice(invoice_number, invoice_date, invoice_amount, invoice_practice, invoice_glcode):
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()
    c.execute("INSERT INTO invoice VALUES (NULL, ?, ?, ?, ?, ?)",
            (invoice_number, invoice_date, invoice_amount, invoice_practice, invoice_glcode))
    conn.commit()
    conn.close()

def view_all_invoices():
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()
    c.execute("SELECT * FROM invoice")
    rows = c.fetchall()
    conn.close()
    return rows

def search_invoice(invoice_number="", invoice_date="", invoice_amount="", invoice_practice="", invoice_glcode=""):
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()
    c.execute("SELECT * FROM invoice WHERE invoice_number=? OR invoice_date=? OR invoice_amount=? OR invoice_practice=? OR invoice_glcode=?",
                (invoice_number, invoice_date, invoice_amount, invoice_practice, invoice_glcode))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_invoice(invoice_id):
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()
    c.execute("DELETE FROM invoice WHERE invoice_id=?", (invoice_id,))
    conn.commit()
    conn.close()

def update_invoice(invoice_id, invoice_number, invoice_date, invoice_amount, invoice_practice, invoice_glcode):
    conn = sqlite3.connect('invoice.db')
    c = conn.cursor()
    c.execute("UPDATE invoice SET invoice_number=?, invoice_date=?, invoice_amount=?, invoice_practice=?, invoice_glcode=? WHERE invoice_id=?",
                (invoice_number, invoice_date, invoice_amount, invoice_practice, invoice_glcode, invoice_id))
    conn.commit()
    conn.close()

#Item Table Creatation and Functions
def item_query_table():
    conn = sqlite3.connect('item.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS item (
                item_id text PRIMARY KEY,
                item_name text
                )""")
    conn.commit()
    conn.close()

def insert_item_data(item_name,item_id):
    conn = sqlite3.connect('item.db')
    c = conn.cursor()
    c.execute("INSERT INTO item VALUES (?, ?)",
            (item_name,item_id))
    conn.commit()
    conn.close()

def get_item_name(item_id):
    conn = sqlite3.connect('item.db')
    c = conn.cursor()
    c.execute("SELECT item_name FROM item WHERE item_id=?", (item_id,))
    item_name = c.fetchall()
    conn.close()
    return item_name

def get_item_id(item_name):
    conn = sqlite3.connect('item.db')
    c = conn.cursor()
    c.execute("SELECT item_id FROM item WHERE item_name=?", (item_name,))
    item_id = c.fetchall()
    conn.close()
    return item_id

def view_all_items():
    conn = sqlite3.connect('item.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM item")
    rows = c.fetchall()
    conn.close()
    return rows


item_query_table()

insert_item_data('VS56614911 7KW75A#BGJ|H','HP LaserJet Pro M283 M283fdw Wireless Laser Multifunction Printer')

for i in view_all_items():
    print(i['item_name'])
    print(i['item_id'])





