import json
import locale
import requests

locale.setlocale(locale.LC_ALL, "nl_NL.utf8")
URL = "https://opendata.cbs.nl/ODataApi/odata/85496NED/TypedDataSet"


def get_data(refresh=True):
    if not refresh:
        try:
            with open("data.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Bestand niet gevonden, downloaden")

            # Roep deze functie aan, met `refresh=True`
            return get_data(refresh=True)
    else:
        response = requests.get(URL)

        # Als de HTTP-code 400 of hoger is, zal er een uitzondering worden opgeworpen
        response.raise_for_status()
        data = response.json()

        # Sla bestand op
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)

    return data


def get_total_population():

    # Open het bestand
    with open("data.json") as f:
        data = json.load(f)  # data is nu een Python object (dict)

    # Bereid een lege lijst voor
    result = []

    # Loop door de rijen in de data
    for item in data["value"]:
        year = item["Perioden"].split("JJ")[0]  # Schoon het jaartal op
        value = item["TotaleBevolking_1"]

        # Voeg het jaartal en de waarde toe aan de lijst als een tuple
        result.append((year, value))

    return result


if __name__ == "__main__":
    data = get_data(refresh=True)  # Zet op False om niet steeds te downloaden
    total_population = get_total_population()

    for year, value in total_population:
        print(f"{year}: {value:n}")
