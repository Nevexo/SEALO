print("\nNevexo's Website Monitor Serive\nV:0.1\n")
class isup:
    def isup(url):
        try:
            if "http://" in url or "https://" in url or "www." in url:
                tmp = requests.get(url)
            else:
                try:
                    tmp = requests.get("https://" + url)
                except:
                    tmp = requests.get("https://" + url)
                return True
        except:
            return False
