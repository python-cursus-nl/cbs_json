import locale
import requests_cache

from datetime import datetime, timedelta
from pydantic import BaseModel, ValidationError

try:
    locale.setlocale(locale.LC_ALL, "nl_NL")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

now = datetime.now()
tonight = datetime(now.year, now.month, now.day) + timedelta(days=1)
URL = "https://opendata.cbs.nl/ODataApi/odata/85496NED/TypedDataSet"


class Response(BaseModel):
    value: list


class Data(BaseModel):
    jaar: str
    totale_bevolking: int


def get_data():
    session = requests_cache.CachedSession(expire_after=tonight)
    response = session.get(URL)

    # Als de HTTP-code 400 of hoger is, zal er een uitzondering worden opgeworpen
    response.raise_for_status()

    # Valideer de inkomende JSON, behoud alleen de `values`
    try:
        validated_response = Response.model_validate_json(response.content)
    except ValidationError as e:
        print(e)
        return

    return validated_response


def get_total_population(validated_response):
    # Bereid een lege lijst voor
    result = []

    # Loop door de rijen in de data
    for row in validated_response.value:
        jaar = row["Perioden"].split("JJ00")[0]  # Schoon het jaartal op
        totale_bevolking = row["TotaleBevolking_1"]

        try:
            data = Data(jaar=jaar, totale_bevolking=totale_bevolking)
        except ValidationError:
            print("Geen geldige data, sla rij over")
            continue

        # Voeg het jaartal en de waarde toe aan de lijst als een Data instantie
        result.append(data)

    return result


if __name__ == "__main__":
    validated_response = get_data()
    if validated_response:
        total_population = get_total_population(validated_response=validated_response)

        for row in total_population:
            print(f"{row.jaar}: {row.totale_bevolking:n}")
