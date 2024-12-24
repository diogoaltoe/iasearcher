from bs4 import BeautifulSoup
import requests


def get_country_details(url: str) -> dict:
    """
    Fetches specific country information (eg.: flag, president, currency, capital) from a Wikipedia page.

    Args:
        url (str): The Wikipedia page URL.

    Returns:
        dict: A dictionary containing the country data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})

        if not infobox:
            return {"error": "Infobox not found on the page."}

        flag_url = _extract_flag_url(infobox)
        capital = _extract_field_value(infobox, "Capital")
        president = _extract_field_value(infobox, "President") or _extract_field_value(
            infobox, "Prime Minister"
        )
        language = _extract_field_value(
            infobox, "Official language"
        ) or _extract_field_value(infobox, "Official languages")
        currency = _extract_field_value(infobox, "Currency")
        timezone = _extract_field_value(infobox, "Time zone")
        largest_city = _extract_field_value(infobox, "Largest city")
        drives_on = _extract_field_value(infobox, "Drives on")

        return _convert_to_json(
            flag_url,
            capital,
            president,
            language,
            currency,
            timezone,
            largest_city,
            drives_on,
        )

    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def _convert_to_json(
    flag_url=None,
    capital=None,
    president=None,
    language=None,
    currency=None,
    timezone=None,
    largest_city=None,
    drives_on=None,
):
    return {
        key: value
        for key, value in {
            "Flag URL": flag_url,
            "Capital": capital,
            "President": president,
            "Language": language,
            "Currency": currency,
            "Timezone": timezone,
            "Largest City": largest_city,
            "Drives On": drives_on,
        }.items()
        if value
    }


def _extract_flag_url(infobox):
    flag_image = infobox.find("img")
    if flag_image and flag_image.get("src"):
        return "https:" + flag_image.get("src")
    return None


def _extract_field_value(infobox, keyword):
    row = None
    for th in infobox.find_all("th"):
        if keyword in th.get_text():
            row = th
            break

    if row:
        value = row.find_next("td")
        first_value = (
            value.contents[0].get_text(strip=True)
            if hasattr(value.contents[0], "get_text")
            else str(value.contents[0]).strip()
        )
        return first_value
    return None


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/France"

    country_info = get_country_details(url)
    for key, value in country_info.items():
        print(f"{key}: {value}")
