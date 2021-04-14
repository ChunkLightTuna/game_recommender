import requests
import mwparserfromhell

def getGameplay(game):

    # Get page based on serch
    session = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    search = game + " video game"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search
    }

    request = session.get(url=url, params=params)
    data = request.json()

    page = data['query']['search'][0]['title']

    # Get gameplay section
    params = {
        "action": "parse",
        "format": "json",
        "page": page,
        "prop": "sections"
    }

    request = session.get(url=url, params=params)
    data = request.json()

    index = False

    for section in data['parse']['sections']:
        if section['line'] == 'Gameplay':
            index = section['index']
            break

    if index==False:
        return False

    # Get section wikitext
    params = {
        "action": "parse",
        "format": "json",
        "page": page,
        "section": index,
        "prop": "wikitext"
    }

    request = session.get(url=url, params=params)
    data = request.json()


    wikicode = data['parse']['wikitext']['*']

    # Parse wikicode
    parsed_wikicode = mwparserfromhell.parse(wikicode).strip_code()

    return parsed_wikicode 
