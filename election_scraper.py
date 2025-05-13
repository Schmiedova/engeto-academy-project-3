"""
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Michaela Schmiedová
email: michaela.schmiedova@email.cz
discord: misa_47996
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv


def validate_arguments():
    if len(sys.argv) != 3:
        print("Použití: python election_scraper.py <URL_územního_celku> <výstupní_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not url.startswith("https://www.volby.cz/pls/ps2017nss/ps32?"):
        print("Neplatný odkaz! Musí začínat https://www.volby.cz/pls/ps2017nss/ps32?")
        sys.exit(1)

    return url, output_file


def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)


def get_municipality_links(main_soup):
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    municipality_data = []

    tables = main_soup.find_all("table", class_="table")
    if not tables:
        print("Tabulky obcí nebyly nalezeny.")
        sys.exit(1)

    for table in tables:
        rows = table.find_all("tr")[2:]  # Přeskoč hlavičku
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                code = cells[0].text.strip()
                name = cells[1].text.strip()
                a_tag = cells[0].find("a")
                if a_tag and "href" in a_tag.attrs:
                    url = base_url + a_tag["href"]
                    municipality_data.append((code, name, url))
    return municipality_data


def get_party_names(soup):
    party_names = []
    tables = soup.find_all("table", class_="table")
    for table in tables[1:]:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                name = cells[1].text.strip()
                if name:
                    party_names.append(name)
    return party_names


def parse_municipality(soup):
    try:
        # Získání statistických údajů z první tabulky
        stats_table = soup.find("table", class_="table")
        stats_cells = stats_table.find_all("td")

        if len(stats_cells) < 8:
            print("[!] Nedostatek údajů v první tabulce.")
            return None

        # Získání správných hodnot podle pořadí
        registered = int(stats_cells[3].text.replace("\xa0", "").replace(" ", ""))
        envelopes = int(stats_cells[4].text.replace("\xa0", "").replace(" ", ""))
        valid = int(stats_cells[7].text.replace("\xa0", "").replace(" ", ""))

        # Hlasy pro strany (druhá a třetí tabulka)
        party_votes = []
        tables = soup.find_all("table", class_="table")[1:]
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    vote_text = cells[2].text.replace("\xa0", "").replace(" ", "")
                    if vote_text.isdigit():
                        party_votes.append(int(vote_text))

        return [registered, envelopes, valid] + party_votes

    except Exception as e:
        print(f"[CHYBA] Při zpracování detailu obce: {e}")
        return None


def scrape_data(main_url, output_file):
    main_soup = get_soup(main_url)
    municipality_list = get_municipality_links(main_soup)

    if not municipality_list:
        print("Nebyl nalezen žádný odkaz na obce.")
        sys.exit(1)

    # První obec: zjištění názvů stran
    first_soup = get_soup(municipality_list[0][2])
    party_names = get_party_names(first_soup)

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        headers = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + party_names
        writer.writerow(headers)

        for code, name, url in municipality_list:
            soup = get_soup(url)
            result = parse_municipality(soup)
            if result:
                writer.writerow([code, name] + result)

    print(f"\n✅ Výsledky byly uloženy do souboru: {output_file}")


if __name__ == "__main__":
    url, output_file = validate_arguments()
    scrape_data(url, output_file)