import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io
from datetime import datetime, timedelta

# Globální proměnné
tasks = []  # Seznam úkolů
assigned_tasks = {}  # Slouží k ukládání přiřazených úkolů (uživatel -> úkol)
task_notifications = []  # Zprávy pro push notifikace
user_tokens = {}  # Ukládání tokenů pro uživatele a jejich expirace


# Funkce pro generování QR kódu
def generate_qr_code():
    user_token = str(random.randint(100000, 999999))  # Generování náhodného tokenu
    expiration_time = datetime.now() + timedelta(minutes=10)  # Platnost 10 minut
    user_tokens[user_token] = expiration_time
    qr_data = f"{user_token}|{expiration_time}"

    qr = qrcode.make(qr_data)

    # Uložení QR kódu do souboru
    qr_path = "invite_qr.png"
    qr.save(qr_path)
    return qr_path, user_token, expiration_time


# Funkce pro skenování QR kódu (načítání tokenu)
def scan_qr_code(image_path):
    # Načtení obrázku QR kódu
    img = Image.open(image_path)
    decoded_data = decode(img)

    if decoded_data:
        qr_data = decoded_data[0].data.decode('utf-8')
        token, expiration = qr_data.split('|')
        expiration_time = datetime.fromisoformat(expiration)

        if datetime.now() < expiration_time:
            messagebox.showinfo("Úspěch", f"Úspěšná registrace s tokenem {token}.")
            return token
        else:
            messagebox.showerror("Chyba", "Token vypršel.")
    else:
        messagebox.showerror("Chyba", "Nebylo možné dekódovat QR kód.")
    return None


# Funkce pro simulaci připojení a práci s úkoly
def reconnect_server():
    attempts = 0
    while attempts < 10:
        attempts += 1
        print(f"Pokouším se připojit k serveru... Pokus {attempts}/10")
        if random.choice([True, False]):  # Simulace náhodného úspěchu připojení
            print("Úspěšně připojeno k serveru.")
            return True
        time.sleep(2)
    print("Nepodařilo se připojit k serveru po 10 pokusech.")
    return False


# Worker pro správu úkolů
def task_worker():
    while True:
        time.sleep(5)  # Čeká na novou akci (simulace čekání)
        if not reconnect_server():
            messagebox.showerror("Chyba připojení", "Nelze se připojit k serveru, zkuste to později.")
            break

        if tasks:
            task = tasks.pop(0)  # Získej první úkol
            task_notifications.append(f"Nový úkol: {task}")
            print(f"Nový úkol na burze: {task}")


# Funkce pro přidání úkolu do burzy
def add_task_to_burza():
    task = entry_task.get()
    if task:
        tasks.append(task)
        update_task_burza()  # Aktualizace listboxu
        notify_users(f"Nový úkol na burze: {task}")
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Varování", "Musíte zadat úkol.")


# Funkce pro zobrazení aktuálních úkolů na burze
def update_task_burza():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)


# Funkce pro převzetí úkolu
def take_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task = task_listbox.get(selected_task)
        if task not in assigned_tasks:
            username = entry_username.get()
            if username:
                assigned_tasks[task] = username
                notify_users(f"{username} převzal úkol: {task}")
                task_listbox.delete(selected_task)  # Odstranění úkolu z burzy
                update_assigned_tasks()  # Aktualizace seznamu přiřazených úkolů
            else:
                messagebox.showwarning("Varování", "Zadejte své uživatelské jméno.")
        else:
            messagebox.showinfo("Info", f"Úkol již převzal {assigned_tasks[task]}")

    else:
        messagebox.showwarning("Varování", "Vyberte úkol k převzetí.")


# Funkce pro zobrazení přiřazených úkolů
def update_assigned_tasks():
    assigned_listbox.delete(0, tk.END)
    for task, user in assigned_tasks.items():
        assigned_listbox.insert(tk.END, f"{task} - Převzal: {user}")


# Funkce pro notifikace
def notify_users(message):
    task_notifications.append(message)
    print(f"Notifikace: {message}")
    # V tuto chvíli jenom vypisujeme do terminálu


# Funkce pro zobrazení a skenování QR kódu
def show_qr_code():
    qr_path, token, expiration_time = generate_qr_code()
    messagebox.showinfo("QR kód generován", f"QR kód byl vygenerován. Platnost: {expiration_time}")
    qr_image = Image.open(qr_path)
    qr_image.show()  # Zobrazí QR kód ve výchozím prohlížeči obrázků


def register_user_from_qr():
    qr_file_path = 'invite_qr.png'  # Předpokládáme, že QR kód je uložen v tomto souboru
    token = scan_qr_code(qr_file_path)
    if token:
        messagebox.showinfo("Registrace", f"Registrace úspěšná s tokenem {token}")


# Hlavní okno
root = tk.Tk()
root.title("Burza úkolů a správa údržby")
root.geometry("500x500")

# Vytvoření záložek
tab_control = ttk.Notebook(root)

# Záložka pro přidání úkolů
tab_burza = ttk.Frame(tab_control)
tab_control.add(tab_burza, text="Burza úkolů")

label_task = tk.Label(tab_burza, text="Přidej nový úkol (např. Mléko, Kávovar):")
label_task.pack(pady=10)

entry_task = tk.Entry(tab_burza, width=30)
entry_task.pack(pady=5)

button_add_task = tk.Button(tab_burza, text="Přidat úkol", command=add_task_to_burza)
button_add_task.pack(pady=10)

task_listbox = tk.Listbox(tab_burza, height=10, width=40)
task_listbox.pack(pady=10)

# Záložka pro přiřazené úkoly
tab_assigned = ttk.Frame(tab_control)
tab_control.add(tab_assigned, text="Přiřazené úkoly")

label_username = tk.Label(tab_assigned, text="Zadejte vaše jméno:")
label_username.pack(pady=10)

entry_username = tk.Entry(tab_assigned, width=30)
entry_username.pack(pady=5)

button_take_task = tk.Button(tab_assigned, text="Převzít úkol", command=take_task)
button_take_task.pack(pady=10)

assigned_listbox = tk.Listbox(tab_assigned, height=10, width=40)
assigned_listbox.pack(pady=10)

# Spuštění workeru pro úkoly
task_worker_thread = threading.Thread(target=task_worker, daemon=True)
task_worker_thread.start()

# Zobrazení záložek
tab_control.pack(expand=1, fill="both")

# Spuštění aplikace
root.mainloop()
