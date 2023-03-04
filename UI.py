import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sqlite3
import funcs

# Setting the window
window = tk.Tk()
window.title("Expense Tracker")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = int(screen_width / 2 + 75)
window_height = int(screen_height / 2 + 75)

x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2)) - 50

window.geometry(f'{window_width}x{window_height}+{x_coord}+{y_coord}')

# Setting the frames and their grids
main_menu = tk.Frame(window)
main_menu.pack(fill="both", expand=True)
for i in range(11):
    main_menu.columnconfigure(i, weight=1, minsize=int(window_width / 10))
    main_menu.rowconfigure(i, weight=1, minsize=int(window_height / 10))

entry_frame = tk.Frame(window)
data_frame = tk.Frame(window)

# Setting the labels

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS limiter 
                (limit_val integer) """)
limit = 100000000
c.execute("SELECT * FROM limiter")
c.execute(f"INSERT OR REPLACE INTO limiter VALUES ({limit})")

c.execute("SELECT limit_val FROM limiter")
lim = c.fetchone()
limit = lim[0] if lim else "-"
if limit == 100000000:
    limit = "-"
conn.close()

first_label = tk.Label(main_menu, text="Peace of mind with the expense tracker", font=('Helvetica', 28))
first_label.grid(row=2, column=1, columnspan=8)

label1 = tk.Label(entry_frame, text="Item:", font=("Helvetica", 12))
label2 = tk.Label(entry_frame, text="Price:", font=("Helvetica", 12))
label3 = tk.Label(entry_frame, text="Paid by:", font=("Helvetica", 12))
label4 = tk.Label(entry_frame, text="Date", font=("Helvetica", 12))
label5 = tk.Label(entry_frame, text="Expectation from this expenditure:", font=("Helvetica", 12))
disclaimer = tk.Label(entry_frame, text="*Should be a whole number*", font=("Helvetica", 10), fg="red")
disclaimer2 = tk.Label(entry_frame, text="*Format should be dd/mm/yyyy*", font=("Helvetica", 10), fg="red")
invalid_label = tk.Label(entry_frame, text="Invalid date format, format should be dd/mm/yyyy", font=("Helvetica", 10),
                         fg="red")
valid_label = tk.Label(entry_frame, text="Valid format", font=("Helvetica", 10), fg="green")
successful_label = tk.Label(entry_frame, text="Successfully recorded data", font=("Helvetica", 10), fg="green")
mark_label = tk.Label(data_frame, text="Set a starting point for major purchases", font=("Helvetica", 10))
limit_label = tk.Label(data_frame, text=f"Current point: {limit}", font=("Helvetica", 10))

label1.grid(row=1, column=2)
label2.grid(row=2, column=2)
label3.grid(row=3, column=2)
label4.grid(row=4, column=2)
label5.grid(row=5, column=0, columnspan=3)
disclaimer.grid(row=2, column=5, columnspan=2)
disclaimer2.grid(row=4, column=5, columnspan=2)
mark_label.grid(row=8, column=4, columnspan=7)
limit_label.grid(row=10, column=6, columnspan=3)

# Getting today's date
today = datetime.today()
today = today.strftime("%d/%m/%Y")


# Setting the input fields

input1 = tk.Entry(entry_frame, validate="key", font=("Helvetica", 10))
input2 = tk.Entry(entry_frame, validate="key", validatecommand=(entry_frame.register(funcs.validator), "%P"),
                  font=("Helvetica", 10))
input3 = tk.Entry(entry_frame, font=("Helvetica", 10))
input4 = tk.Entry(entry_frame, validate="focusout", validatecommand=(entry_frame.register(lambda: funcs.validate1(input4.get(), disclaimer2, invalid_label, valid_label))),
                  invalidcommand=(entry_frame.register(lambda: funcs.invalid(valid_label, disclaimer2, invalid_label))), font=("Helvetica", 10))
input5 = tk.Entry(entry_frame, validate="key", font=("Helvetica", 10))
input6 = tk.Entry(data_frame, validate="key", validatecommand=(data_frame.register(funcs.validator), "%P"), font=("Helvetica", 10))

input1.grid(row=1, column=3, pady=20, sticky="ew", columnspan=2)
input2.grid(row=2, column=3, pady=20, sticky="ew", columnspan=2)
input3.grid(row=3, column=3, pady=20, sticky="ew", columnspan=2)
input3.insert(0, "Me")
input4.grid(row=4, column=3, pady=20, sticky="ew", columnspan=2)
input4.insert(0, today)
input5.grid(row=5, column=3, sticky="ew", columnspan=3)
input6.grid(row=9, column=7)

input1['validatecommand'] = (entry_frame.register(lambda val, act, idx, event=None: funcs.validate2(20, val, act, idx, event)), '%P', '%d', '%i')
input5['validatecommand'] = (entry_frame.register(lambda val, act, idx, event=None: funcs.validate2(39, val, act, idx, event)), '%P', '%d', '%i')

# Setting the buttons

entry_button = tk.Button(main_menu, command=lambda: funcs.hide(main_menu, entry_frame, 8, window_width, window_height), text="Make a new entry", padx=130,
                         pady=75, font=("Helvetica", 15))
view_data = tk.Button(main_menu, command=lambda: funcs.hide(main_menu, data_frame, 11, window_width, window_height), text="Entries & Stats", padx=75,
                      pady=10, font=("Helvetica", 15))
menu = tk.Button(entry_frame, command=lambda: funcs.hide(entry_frame, main_menu, 10, window_width, window_height), text="Main menu",
                 font=("Helvetica", 13))
view_data1 = tk.Button(entry_frame, command=lambda: funcs.hide(entry_frame, data_frame, 11, window_width, window_height), text="Entries & Stats", padx=3,
                       pady=3, font=("Helvetica", 11))
confirm = tk.Button(entry_frame, command=lambda: funcs.confirm_values(successful_label, confirm, entry_frame, input1, input2,
                                                                input3, input4, input5), text="Confirm", font=("Helvetica", 14))
menu1 = tk.Button(data_frame, command=lambda: funcs.hide(data_frame, main_menu, 10, window_width, window_height),
                  text="Main menu", font=("Helvetica", 13))
entry1 = tk.Button(data_frame, command=lambda: funcs.hide(data_frame, entry_frame, 8, window_width, window_height), text="New entry",
                   font=("Helvetica", 13))
refresher = tk.Button(data_frame, command=lambda: funcs.refresh(tree, input6, data_frame, limit_label), text="refresh", font=("Helvetica", 13))


entry_button.grid(row=4, column=2, sticky="NSEW", columnspan=2)
view_data.grid(row=4, column=6, sticky="NSEW", columnspan=2)
menu.grid(row=6, column=3)
view_data1.grid(row=6, column=5)
confirm.grid(row=5, column=6)
menu1.grid(row=8, column=1, columnspan=2)
entry1.grid(row=9, column=1, columnspan=2)
refresher.grid(row=8, column=3)


# Disabling Confirm

funcs.disable(input1, input2, input3, input4, confirm, entry_frame)

# Setting up the data table

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
tree = ttk.Treeview(data_frame, height=10)

tree["columns"] = ("one", "two", "three", "four")
tree.column("#0", width=168, minwidth=168, stretch=tk.NO)
tree.column("one", width=120, minwidth=120, stretch=tk.NO)
tree.column("two", width=100, minwidth=100, stretch=tk.NO)
tree.column("three", width=120, minwidth=120, stretch=tk.NO)
tree.column("four", width=333, minwidth=333, stretch=tk.NO)

tree.heading("#0", text="Item", anchor=tk.W)
tree.heading("one", text="Price", anchor=tk.W)
tree.heading("two", text="Paid by", anchor=tk.W)
tree.heading("three", text="Date", anchor=tk.W)
tree.heading("four", text="Comments", anchor=tk.W)

tree.grid(row=0, column=0, sticky="nsew", columnspan=10, rowspan=8)

scrollbar = tk.Scrollbar(data_frame)
scrollbar.grid(row=0, column=9, sticky="ns", rowspan=8, columnspan=2)

tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)


funcs.table(tree, input6, entry_frame, limit_label)

