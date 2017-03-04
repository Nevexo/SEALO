print("\nNevexo's Wikipedia and Urban Dictionary API Tool\nV:1.2")
import requests, wikipedia, json
class define:
    def urban(query):
        try:
            url = 'http://api.urbandictionary.com/v0/define?term=%s' % (query)
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.content.decode('utf-8'))
            definition = data['list'][0]['definition']
            return definition
        except:
            return False

    def wiki(query):
        try:
            defi = wikipedia.summary(query, sentences=2)
            return defi
        except:
            return False 
