import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import time

API_URL = "http://127.0.0.1:5000/tasks"

# Globální seznam pro kávové záznamy
coffee_log = []
current_user = None

# Tkinter widgety
combobox_coffee_type = None
combobox_amount = None
combobox_strength = None
entry_task_description = None
text_coffee_overview = None
text_task_overview = None

def start_server():
    """Spustí Flask server na pozadí."""
    from server import run_flask
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()

def fetch_tasks():
    """Načte úkoly ze serveru a aktualizuje GUI."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        tasks = response.json()
        update_task_overview(tasks)
    except requests.exceptions.RequestException as e:
        print(f"Chyba při synchronizaci úkolů: {e}")

def add_task():
    """Přidá nový úkol na server."""
    task_description = entry_task_description.get()
    if task_description:
        try:
            response = requests.post(API_URL, json={"description": task_description})
            response.raise_for_status()
            fetch_tasks()
            entry_task_description.delete(0, tk.END)
            print(f"Úkol '{task_description}' přidán.")
        except requests.exceptions.RequestException as e:
            print(f"Chyba při odesílání úkolu: {e}")

def add_coffee():
    """Přidá záznam kávy do lokálního seznamu."""
    coffee_type = combobox_coffee_type.get()
    amount = combobox_amount.get()
    strength = combobox_strength.get()

    if coffee_type and amount and strength:
        record = f"Kafe: {coffee_type}, Množství: {amount} ml, Síla: {strength}"
        coffee_log.append(record)
        update_coffee_overview()
        combobox_coffee_type.set("")
        combobox_amount.set("")
        combobox_strength.set("")
        print(f"Nové kafe přidáno: {record}")

def assign_task(task_id, user="admin"):
    """Přiřazuje úkol uživateli."""
    try:
        response = requests.put(f"{API_URL}/{task_id}/assign", json={"user": user})
        response.raise_for_status()
        fetch_tasks()
        print(f"Úkol {task_id} přiřazen uživateli {user}.")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při přiřazení úkolu: {e}")

def complete_task(task_id):
    """Označuje úkol jako dokončený."""
    try:
        response = requests.put(f"{API_URL}/{task_id}/complete")
        response.raise_for_status()
        fetch_tasks()
        print(f"Úkol {task_id} označen jako dokončený.")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při dokončování úkolu: {e}")

def update_coffee_overview():
    """Aktualizuje přehled kávy v GUI."""
    text_coffee_overview.delete(1.0, tk.END)
    for record in coffee_log:
        text_coffee_overview.insert(tk.END, record + "\n")

def update_task_overview(tasks):
    """Aktualizuje přehled úkolů v GUI."""
    text_task_overview.delete(1.0, tk.END)
    for task in tasks:
        task_status = (
            f"ID: {task['id']}, "
            f"Popis: {task['description']}, "
            f"Přiřazeno: {task['assigned_to'] or 'Nikdo'}, "
            f"Dokončeno: {'Ano' if task['completed'] else 'Ne'}\n"
        )
        text_task_overview.insert(tk.END, task_status)

        # Přidáme tlačítka "Přiřadit" a "Dokončit" ke každému úkolu
        button_frame = tk.Frame(text_task_overview)
        assign_button = ttk.Button(button_frame, text="Přiřadit", command=lambda tid=task["id"]: assign_task(tid))
        assign_button.pack(side=tk.LEFT, padx=5)

        complete_button = ttk.Button(button_frame, text="Dokončit", command=lambda tid=task["id"]: complete_task(tid))
        complete_button.pack(side=tk.LEFT, padx=5)

        text_task_overview.window_create(tk.END, window=button_frame)
        text_task_overview.insert(tk.END, "\n")

def auto_sync_tasks():
    """Pravidelná synchronizace úkolů se serverem."""
    while True:
        fetch_tasks()
        time.sleep(5)

def login():
    """Zobrazí dialogové okno pro přihlášení."""
    login_window = tk.Toplevel()
    login_window.title("Přihlášení")

    ttk.Label(login_window, text="Uživatelské jméno:").pack(pady=5)
    username_entry = ttk.Entry(login_window)
    username_entry.pack(pady=5)

    ttk.Label(login_window, text="Heslo:").pack(pady=5)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        # Pro jednoduchost hardcoded ověření
        valid_users = {"admin": "password123", "user": "mypassword"}
        if username in valid_users and valid_users[username] == password:
            global current_user
            current_user = username
            login_window.destroy()
            print(f"Přihlášen uživatel: {username}")
        else:
            messagebox.showerror("Chyba", "Neplatné přihlašovací údaje!")

    login_button = ttk.Button(login_window, text="Přihlásit", command=attempt_login)
    login_button.pack(pady=10)

    login_window.transient()  # Nastaví okno jako modální
    login_window.grab_set()
    login_window.wait_window()

def show_main_window():
    """Nastavení hlavního okna Tkinter."""
    global combobox_coffee_type, combobox_amount, combobox_strength, entry_task_description
    global text_coffee_overview, text_task_overview

    root = tk.Tk()
    root.title("Úkoly a kávové záznamy")

    # Vyžaduje přihlášení před zobrazením hlavního okna
    login()

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Tab 1: Zadání kávy a úkolů
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Zadání kávy a úkolu")

    label_coffee_type = ttk.Label(tab1, text="Typ kávy:")
    label_coffee_type.pack(pady=5)
    combobox_coffee_type = ttk.Combobox(tab1, values=["Espresso", "Cappuccino", "Latte", "Americano"])
    combobox_coffee_type.pack(pady=5)

    label_amount = ttk.Label(tab1, text="Množství (ml):")
    label_amount.pack(pady=5)
    combobox_amount = ttk.Combobox(tab1, values=["100", "200", "300", "400"])
    combobox_amount.pack(pady=5)

    label_strength = ttk.Label(tab1, text="Síla:")
    label_strength.pack(pady=5)
    combobox_strength = ttk.Combobox(tab1, values=["Slabá", "Střední", "Silná"])
    combobox_strength.pack(pady=5)

    button_add_coffee = ttk.Button(tab1, text="Přidat kafe", command=add_coffee)
    button_add_coffee.pack(pady=10)

    label_task_description = ttk.Label(tab1, text="Popis úkolu:")
    label_task_description.pack(pady=5)
    entry_task_description = ttk.Entry(tab1)
    entry_task_description.pack(pady=5)

    button_add_task = ttk.Button(tab1, text="Přidat úkol", command=add_task)
    button_add_task.pack(pady=10)

    # Tab 2: Přehled kávy
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Přehled káv")

    text_coffee_overview = tk.Text(tab2, wrap="word", height=15, width=50)
    text_coffee_overview.pack(padx=10, pady=10)

    # Tab 3: Přehled úkolů
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Přehled úkolů")

    text_task_overview = tk.Text(tab3, wrap="word", height=15, width=50)
    text_task_overview.pack(padx=10, pady=10)

    # Automatická synchronizace úkolů
    threading.Thread(target=auto_sync_tasks, daemon=True).start()

    # Spuštění hlavní smyčky
    root.mainloop()

if __name__ == "__main__":
    # Spuštění Flask serveru na pozadí
    start_server()

    # Počká chvíli na spuštění serveru
    time.sleep(2)

    # Zobrazení hlavního okna GUI
    show_main_window()
