import pandas as pd
import tkinter as tk
import sqlite3
from datetime import datetime


# check if the price is valid
def validator(value):
    if len(value) == 0:
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False


# check if the date is valid
def validate1(entry, disc2, inv_lab, val_lab):
    try:
        disc2.grid_forget()
        inv_lab.grid_forget()
        datetime.strptime(entry, "%d/%m/%Y")
        val_lab.grid(row=4, column=5)
        return True
    except ValueError:
        return False


# limit number of characters
def validate2(lim, value, action, index, event=None):
    if len(value) >= lim and (not event or event.keysym != "BackSpace"):
        return False
    else:
        return True


# execute when the date format is invalid
def invalid(val_lab, disc2, inv_lab):
    val_lab.grid_forget()
    disc2.grid_forget()
    inv_lab.grid(row=4, column=5, columnspan=3)


# switch windows
def hide(frame, new_frame, n, win_w, win_h):
    frame.pack_forget()
    new_frame.pack(fill="both", expand=True)
    for c in range(n + 1):
        new_frame.columnconfigure(c, weight=1, minsize=int(win_w / n))
        new_frame.rowconfigure(c, weight=1, minsize=int(win_h / n))


# confirm the entries
def confirm_values(succ_lab, conf, frame, inp1, inp2, inp3, inp4, inp5):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS expenses(
            item text,
            price integer,
            paid_by text,
            date text,
            comments text
        )""")

    item_val = inp1.get()
    price_val = int(inp2.get())
    paid_by_val = inp3.get()
    date_val = inp4.get()
    comments_val = inp5.get()

    c.execute("""INSERT INTO expenses (item, price, paid_by, date, comments) 
    VALUES (?, ?, ?, ?, ?)""", (item_val, price_val, paid_by_val, date_val, comments_val))
    conn.commit()
    conn.close()

    succ_lab.grid(row=6, column=6, columnspan=2)
    conf.config(state=tk.DISABLED)

    def go_back():
        succ_lab.grid_forget()
        conf.config(state=tk.NORMAL)

    frame.after(3000, go_back)


# disable if the entry is invalid
def disable(inp1, inp2, inp3, inp4, conf, frame):
    input_list = [inp1, inp2, inp3, inp4]
    invalid_value = False
    for widget in input_list:
        if widget.get() == "":
            invalid_value = True
            break
        try:
            datetime.strptime(inp4.get(), "%d/%m/%Y")
        except ValueError:
            invalid_value = True

    if invalid_value:
        conf.config(state=tk.DISABLED)
    else:
        conf.config(state=tk.NORMAL)

    frame.after(1000, lambda: disable(inp1, inp2, inp3, inp4, conf, frame))


# count the sum of everything the user has spent money on in a given month
def data_an(mt):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["month"] = df["date"].dt.strftime("%B %Y")
    return df[df["month"] == mt]["price"].sum()


# count the number of entries
def data_an2(mt):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["month"] = df["date"].dt.strftime("%B %Y")
    df["count"] = 1
    return df[df["month"] == mt].count()['count']


# count the major purchases
def data_an3(mt, limit):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df["month"] = df["date"].dt.strftime("%B %Y")
    df["count"] = 1
    return df[(df["month"] == mt) & (df["price"] >= limit)].count()["count"]


# add values into the table
def table(tree, inp, frame, lim_lab):

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS expenses(
                item text,
                price integer,
                paid_by text,
                date text,
                comments text
            )""")

    c2 = conn.cursor()
    c2.execute("""CREATE TABLE IF NOT EXISTS limiter
                   (limit_val integer) """)

    limit = 100000000

    c2.execute("SELECT * FROM limiter")
    c2.execute(f"INSERT OR REPLACE INTO limiter VALUES ({limit})")

    # Get the current value of limit_val from the table
    cursor = conn.cursor()
    cursor.execute("SELECT limit_val FROM limiter")
    row = cursor.fetchone()
    limit = row[0] if row else 100000000

    # Update the value of limit_val using user input
    try:
        new_limit = int(inp.get())
        cursor.execute(f"UPDATE limiter SET limit_val = {new_limit}")
        limit = new_limit
    except ValueError:
        pass

    conn.commit()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    tree_items = {}

    for row in rows:
        date = row[3]
        date_str = datetime.strptime(date, "%d/%m/%Y")
        month = date_str.strftime("%B %Y")
        if month not in tree_items:
            node_id = tree.insert("", tk.END, text=month, values=(f"Total spent: {data_an(month)}",
                            f"Total records: {data_an2(month)}", f"major purchases: {data_an3(month, limit)}", ""), open=True)
            tree_items[month] = node_id

        item_id = tree.insert(tree_items[month], tk.END, text=row[0], values=row[1:])

        if row[1] >= limit:
            tree.item(item_id, tags=("Expensive",))
        tree.tag_configure("Expensive", background='red')

    datetime_objects = [datetime.strptime(item, "%B %Y") for item in tree_items.keys()]
    datetime_objects.sort()
    sorted_dates = [dt_obj.strftime("%B %Y") for dt_obj in datetime_objects]
    for d in sorted_dates:
        tree.move(tree_items[d], "", 0)

    conn.commit()
    conn.close()


def refresh(trees, inp, frame, lim_lab):
    for iid in trees.get_children():
        trees.delete(iid)

    table(trees, inp, frame, lim_lab)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT limit_val FROM limiter")
    lim1 = c.fetchone()
    limit1 = lim1[0] if lim1 else "-"
    if limit1 == 100000000:
        limit1 = "-"
    conn.close()

    lim_lab.config(text=f"Current point: {limit1}")
    lim_lab.grid_forget()
    lim_lab.grid(row=10, column=6, columnspan=3)
