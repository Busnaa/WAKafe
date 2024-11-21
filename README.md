README - Úkoly a Kávové Záznamy
Popis
Tento projekt je jednoduchá aplikace, která vám umožní spravovat úkoly a kávové záznamy. Aplikace běží na Flask serveru, který poskytuje API pro práci s úkoly, a zároveň využívá Tkinter pro grafické uživatelské rozhraní (GUI). Umožňuje přidávat úkoly, přiřazovat je uživatelům, označovat je jako dokončené a sledovat kávové záznamy.

Funkce
Přidávání úkolů: Můžete přidávat nové úkoly s popisem.
Přidávání kávových záznamů: Uživatelé mohou zadávat informace o kávě, jako je typ, množství a síla.
Přehled úkolů: Zobrazí seznam všech úkolů s možností přiřazení úkolu a označení jako dokončený.
Přehled káv: Zobrazuje všechny přidané kávové záznamy.
Automatická synchronizace: Úkoly se pravidelně synchronizují se serverem.
Přihlášení: Uživatel se musí přihlásit, aby mohl využívat funkce aplikace (pro jednoduchost je přihlašování hardcoded).

Technologie
Flask: Webový framework pro serverovou část.
Tkinter: Knihovna pro tvorbu grafického uživatelského rozhraní (GUI).
Requests: Knihovna pro HTTP komunikaci mezi klientem a serverem.
Threading: Pro běh serveru a synchronizaci úkolů na pozadí.
Instalace
Nainstalujte Python (verze 3.x):

Stáhnout Python
Vytvořte virtuální prostředí (doporučeno):

bash
Zkopírovat kód
python -m venv venv
source venv/bin/activate  # pro Linux/macOS
venv\Scripts\activate     # pro Windows
Nainstalujte požadované balíčky: Tento projekt vyžaduje následující balíčky:

Flask
Requests
Tkinter (standardně součástí Pythonu, ale na některých systémech je potřeba jej doinstalovat)
Waitress (pro server)
Instalujte je pomocí pip:

bash
Zkopírovat kód
pip install flask requests waitress
Stáhněte si soubory projektu:

client.py: Klientská aplikace (GUI pro práci s úkoly a kávou).
server.py: Flask server pro správu úkolů (API).
Spuštění projektu:

Nejprve spusťte server:
bash
Zkopírovat kód
python server.py
Poté spusťte klientskou aplikaci:
bash
Zkopírovat kód
python client.py
Aplikace otevře okno, kde se můžete přihlásit a začít zadávat úkoly a kávové záznamy.

Struktura souborů
bash
Zkopírovat kód
/project
    ├── server.py           # Flask server pro správu úkolů
    └── client.py           # Klientská aplikace s GUI pro úkoly a kávu
Použití
1. Přihlášení
Po spuštění klientské aplikace se zobrazí přihlašovací okno, kde musíte zadat uživatelské jméno a heslo. Uživatelé jsou přednastaveni na:

admin: heslo je password123
user: heslo je mypassword
2. Přidávání úkolů
V hlavním okně můžete přidat nový úkol. Stačí zadat popis úkolu a kliknout na tlačítko "Přidat úkol".

3. Přidávání kávových záznamů
V části pro kávu můžete zadat typ kávy, množství a sílu. Po kliknutí na tlačítko "Přidat kafe" se záznam přidá do přehledu káv.

4. Přehled úkolů
V záložce "Přehled úkolů" uvidíte všechny úkoly s možností přiřadit úkol uživateli nebo ho označit jako dokončený.

5. Synchronizace
Úkoly a kávové záznamy se automaticky synchronizují se serverem každých 5 sekund.

Poznámky
Tento projekt je určený pro ukázku základní interakce mezi klientem a serverem. Není určen pro použití ve velkých produkčních systémech.
Kód pro přihlášení je pro zjednodušení hardcoded, ale můžete si přidat vlastní databázi uživatelů pro větší flexibilitu.
Server používá knihovnu Waitress pro efektivní běh Flask aplikace.
Pokud máte jakékoli otázky, neváhejte mě kontaktovat!
