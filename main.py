import tkinter as tk
from tkinter import ttk
import threading
import requests
import time

API_URL = "http://127.0.0.1:5000/tasks"

# Globální seznam pro kávové záznamy
coffee_log = []

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

def auto_sync_tasks():
    """Pravidelná synchronizace úkolů se serverem."""
    while True:
        fetch_tasks()
        time.sleep(5)

def auto_sync_coffee():
    """Pravidelná aktualizace přehledu kávy v GUI."""
    while True:
        update_coffee_overview()
        time.sleep(5)

def show_main_window():
    """Nastavení hlavního okna Tkinter."""
    global combobox_coffee_type, combobox_amount, combobox_strength, entry_task_description
    global text_coffee_overview, text_task_overview

    root = tk.Tk()
    root.title("Úkoly a kávové záznamy")

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

    # Načtení úkolů při spuštění
    fetch_tasks()

    # Spuštění vlákna pro synchronizaci úkolů
    sync_thread = threading.Thread(target=auto_sync_tasks, daemon=True)
    sync_thread.start()

    # Spuštění vlákna pro synchronizaci kávy
    coffee_sync_thread = threading.Thread(target=auto_sync_coffee, daemon=True)
    coffee_sync_thread.start()

    root.mainloop()

if __name__ == "__main__":
    # Spuštění Flask serveru na pozadí
    start_server()

    # Počká chvíli na spuštění serveru
    time.sleep(2)

    # Zobrazení hlavního okna GUI
    show_main_window()
