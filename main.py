import sqlite3 as s
import customtkinter as ct
import pathlib as ptl

app = ct.CTk()

app.title("SQL-Learning-Tool")
app.geometry("1400x800")

dbs_created = ptl.Path('.').glob("*.db")
cmb_dbs_values = ['---Select db here---']
for db in dbs_created:
    db_name = db.name
    cmb_dbs_values.append(db_name)

cmb_tbls_values = ['---Select db tbls here---']

def get_db_tbls(selected_cmb_db_value):
    if selected_cmb_db_value == '---Select db here---' : 
        textbox_result.configure(state="normal")
        textbox_result.insert("1.0", "PLEASE PICK A DATABASE FIRST!!!")
        textbox_result.configure(state="disabled")
        cmb_tbls.configure(values=['---Select db tbls here---'])
    else:
        tbls_to_add = []
        selected_db_name = selected_cmb_db_value
        db_conn = s.connect(selected_db_name)
        db_cursor = db_conn.cursor()
        tables = db_cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        for table in tables:
            tbls_to_add.append(table[0])
        cmb_tbls.configure(values=['---Select db tbls here---'])
        cmb_tbls.configure(values=tbls_to_add)


def clear():
    textbox_entry.delete("0.0", "end")
    textbox_result.configure(state="normal")
    textbox_result.delete("0.0", "end")
    textbox_result.configure(state="disabled")
    cmb_tbls.configure(values=['---Select db tbl here----'])
    cmb_dbs.configure(values=['---Select db here---'])

def execute_query():
    if textbox_result.get("0.0", "end") != "" :
        textbox_result.configure(state="normal")
        textbox_result.delete("0.0", "end")
        textbox_result.configure(state="disabled")
    if cmb_dbs.get() != "---Select db here---" :
        chosen_db = cmb_dbs.get()
    query_text = textbox_entry.get("0.0", "end-1c")
    if query_text.__contains__("DATABASE") : 
        try:
            query_db_name = query_text.split(" ").__getitem__(-1)
            if query_db_name.endswith(".db"):
                db_conn = s.connect(query_db_name)
                cmb_dbs_values.append(query_db_name)
            else:
                textbox_result.configure(state="normal")
                textbox_result.insert("1.0", "Please make sure that your database name ends in '.db'!")
                textbox_result.configure(state="disabled")
            db_conn.close()
        except Exception as e:
            textbox_result.configure(state="normal")
            textbox_result.insert("0.0", type(e).__name__ + "\n")
            textbox_result.insert("1.0", e)
            textbox_result.configure(state="disabled")
            return 0
        textbox_result.configure(state="normal")
        textbox_result.insert("1.0", query_text.split(" ")[-1] + " database successfully created!")
        textbox_result.configure(state="disabled")
    elif query_text.__contains__('CREATE TABLE') :
        try:
            db_conn = s.connect(chosen_db)
            db_cursor = db_conn.cursor()
            db_cursor.execute(query_text)
            db_conn.close()
        except Exception as e:
            textbox_result.configure(state="normal")
            textbox_result.insert("0.0", type(e).__name__ + "\n")
            textbox_result.insert("1.0", e)
            textbox_result.configure(state="disabled")
            return 0
        textbox_result.configure(state="normal")
        textbox_result.insert("1.0", "Table " + query_text.split(" ")[-1] +" successfully created")
    elif query_text.__contains__('INSERT') :
        try:
            db_conn = s.connect(chosen_db)
            db_cursour = db_conn.execute(query_text)
            db_conn.commit()
            db_conn.close()
        except Exception as e:
            textbox_result.configure(status="normal")
            textbox_result.insert("1.0", type(e).__name__ + "\n")
            textbox_result.insert("2.0", e)
            textbox_result.configure(status="disabled")
            return 0
        textbox_result.configure(state="normal")
        textbox_result.insert("1.0", "Your record was successfully inserted")
        textbox_result.configure(state="disabled")
    elif query_text.__contains__('SELECT') :
        try:
            db_conn = s.connect(chosen_db)
            db_cursor = db_conn.cursor()
            rows = db_cursor.execute(query_text)
            if rows:
                i = 1 
                textbox_result.configure(state="normal")
                for row in rows:
                    textbox_result.insert(str(i)+".0", str(row) + "\n")
                    i = i + 1
                textbox_result.configure(state="disabled")
            else:
                textbox_result.configure(state="normal")
                textbox_result.insert("0.0", "No records found")
                textbox_result.configure(state="disabled")
            db_conn.close()
        except Exception as e:
            textbox_result.configure(state="normal")
            textbox_result.insert("1.0", type(e).__name__ + "\n")
            textbox_result.insert("2.0", e)
            textbox_result.configure(state="disabled")
    elif query_text.__contains__("UPDATE") :
        try:
            db_conn = s.connect(chosen_db)
            db_cursor = db_conn.cursor()
            db_cursor.execute(query_text)
            db_conn.commit()
            db_conn.close()
        except Exception as e:
            textbox_result.configure(state="normal")
            textbox_result.insert("1.0", type(e).__name__ + "\n")
            textbox_result.insert("2.0", str(e))
            textbox_result.configure(state="disabled")
            return 0
        textbox_result.configure(state="normal")
        textbox_result.insert("1.0", "Changes have been successfully saved")
        textbox_result.configure(state="disabled")


app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

win_title = ct.CTkLabel(app, text="SQL Learning Tool", font=("Arial", 48, "bold"))
win_title.grid(row=0, column=0, padx=20, pady=(30, 20), columnspan=3)
instruction_label = ct.CTkLabel(app, text="NB! All your databases should have a '.db' extention.", font=("Courier New", 16, "italic"))
instruction_label.grid(row=1, column=0, sticky="nsew", columnspan=3)
entry_label = ct.CTkLabel(app, text="Enter your SQL here", font=("Arial", 14))
entry_label.grid(row=2, column=0, pady=(10, 0))
result_label = ct.CTkLabel(app, text="Result Area", font=("Segeo UI", 14, "bold"))
result_label.grid(row=2, column=1, columnspan=2, pady=(10, 0))
textbox_entry = ct.CTkTextbox(app, width=300, height=500)
textbox_entry.grid(row=3, column=0, sticky="nsew", padx=(20, 10))
textbox_result = ct.CTkTextbox(app, width=300, height=500)
textbox_result.grid(row=3, column=1, sticky="nsew", padx=(10, 20), columnspan=2)
textbox_result.configure(state="disabled")
run_button = ct.CTkButton(app, text="Run Query", command=execute_query)
run_button.grid(row=4, column=0, pady=10)
cmb_dbs = ct.CTkComboBox(app, width=200, values=cmb_dbs_values, command=get_db_tbls)
cmb_dbs.grid(row=4, column=1, sticky="e", padx=10)
cmb_tbls = ct.CTkComboBox(app, width=200, values=cmb_tbls_values)
cmb_tbls.grid(row=4, column=2, sticky="w")
clear_button = ct.CTkButton(app, text="Clear", command=clear)
clear_button.grid(row=5, column=0, pady=10)

app.mainloop()