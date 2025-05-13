# Scraper volebních výsledků 2017

Tento projekt byl vytvořen jako třetí závěrečný úkol v rámci Engeto Online Python Akademie. Jde o web scraper, který stáhne a uloží výsledky voleb do Poslanecké sněmovny 2017 z webu volby.cz pro zadaný územní celek. Výstupem je `.csv` soubor obsahující data za všechny obce daného celku.

---

## Popis

1. Program stáhne HTML stránku územního celku z webu volby.cz.  
2. Ze stránky vybere odkazy na jednotlivé obce a navštíví každý z nich.  
3. Z každé obecní stránky načte:
   - kód obce  
   - název obce  
   - počet registrovaných voličů  
   - počet vydaných obálek  
   - počet platných hlasů  
   - počet hlasů pro každou kandidující stranu  
4. Vše uloží do `.csv` souboru.

---

## Požadavky

- Python 3.6 nebo vyšší  
- Knihovny: `requests`, `beautifulsoup4`

---

## Instalace

1. Naklonujte nebo stáhněte repozitář se soubory:
   ```bash
   git clone https://github.com/Schmiedova/engeto-academy-project-3.git
   cd engeto-academy-project-3
   ```

2. Vytvořte a aktivujte virtuální prostředí:
   ```bash
   python -m venv nazev_prostedi
   source nazev_prostedi/bin/activate        # Linux/macOS
   nazev_prostedi\Scripts\activate.ps1       # Windows
   ```

3. Nainstalujte potřebné knihovny:
   ```bash
   pip install -r requirements.txt
   ```

---

## Použití

Spusťte skript v příkazové řádce se dvěma argumenty:

1. Odkaz na stránku s výsledky územního celku.  
2. Název výstupního `.csv` souboru.

```bash
python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" "vysledky_brno_venkov.csv"
```

- Pokud nejsou zadány správné argumenty, program zobrazí chybovou hlášku a ukončí se.

---

## Struktura výstupu

Výstupní CSV obsahuje jeden řádek pro každou obec:

| kód obce | název obce | voliči v seznamu | vydané obálky | platné hlasy | [hlasy pro každou stranu...] |
|----------|------------|------------------|----------------|---------------|------------------------------|

---

## Struktura kódu

1. **Hlavička**  
   - Informace o autorovi

2. **validate_arguments()**
   - Kontroluje počet a správnost argumentů  

3. **get_soup(url)**  
   - Načítá HTML a vrací objekt `BeautifulSoup`  

4. **get_municipality_links(main_soup)**  
   - Vytahuje odkazy na jednotlivé obce  

5. **get_party_names(soup)**  
   - Zjišťuje názvy všech kandidujících stran  

6. **parse_municipality(soup)**  
   - Získává statistiky a hlasy pro danou obec  

7. **scrape_data(main_url, output_file)**  
   - Hlavní řídicí funkce pro scraping a zápis do CSV

---

## Autor

Michaela Schmiedová  
- Engeto Online Python Akademie  
- email: michaela.schmiedova@email.cz  
- discord: misa_47996