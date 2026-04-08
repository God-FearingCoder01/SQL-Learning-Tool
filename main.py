import sqlite3 as s
import customtkinter as ct 

app = ct.CTk()

app.title("SQL-Learning-Tool")
app.geometry("1400x800")

def clear():
    textbox_entry.delete("0.0", "end")
    textbox_result.configure(state="normal")
    textbox_result.delete("0.0", "end")
    textbox_result.configure(state="disabled")

def execute_query():
    query_text = textbox_entry.get("0.0", "end-1c")
    if query_text.__contains__("DATABASE") : 
        try:
            db_conn = s.connect(query_text.split(" ").__getitem__(-1))
        except Exception as e:
            textbox_result.configure(state="normal")
            textbox_result.insert("0.0", e)
            textbox_result.configure(state="disabled")


app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

win_title = ct.CTkLabel(app, text="SQL Learning Tool", font=("Arial", 48, "bold"))
win_title.grid(row=0, column=0, padx=20, pady=(30, 20), columnspan=2)
entry_label = ct.CTkLabel(app, text="Enter your SQL here")
entry_label.grid(row=1, column=0)
result_label = ct.CTkLabel(app, text="Result Area")
result_label.grid(row=1, column=1)
textbox_entry = ct.CTkTextbox(app, width=300, height=500)
textbox_entry.grid(row=2, column=0, sticky="nsew", padx=(20, 10))
textbox_result = ct.CTkTextbox(app, width=300, height=500)
textbox_result.grid(row=2, column=1, sticky="nsew", padx=(10, 20))
textbox_result.configure(state="disabled")
run_button = ct.CTkButton(app, text="Run Query")
run_button.grid(row=3, column=0, pady=10)
clear_button = ct.CTkButton(app, text="Clear")
clear_button.grid(row=4, column=0, pady=10)
app.mainloop()