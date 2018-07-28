import re
import requests
import json
from bs4 import BeautifulSoup
import datetime
import html
import random
    
class Blagues:
    def __init__(self):
        self.file = "blagues.json"
        self.blagues = {}
        self.baseUrl = "https://www.blague-drole.net/blagues/"
        self.categories = ["alcoolique", "animaux","belge","belles-meres",
                            "blonde","chuck.norris","clash","combles",
                            "contrepèterie","corse","couple","courte",
                            "devinette","enfant","femmes","fou",
                            "geek","histoire.drole","hommes","humour.noir",
                            "lois.de.murphy","medecine","militaire","mr.et.mme",
                            "policier","politique","proverbe.et.citation","religion",
                            "sexe","ta.mere","toto","travail","van.damme"]
        try:
            self.load_file()
        except:
            print("Aucun fichier trouvé")
            pass
    
    def load_file(self):
        with open(self.file, "r") as f:
            self.blagues = json.loads(f.read())
            
    def save_file(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self.blagues, indent=4, sort_keys=True, ensure_ascii=False))
            
    def get_max_pages(self, category):
        page = requests.get(self.baseUrl+category+'-1.html').text
        soup_page = BeautifulSoup(page, "html.parser")
        pagination = soup_page.find("input", {"class": "pagination-input"})
        return int(pagination["max"])
            
            
    def parse_website(self, filter=None):
        now = datetime.datetime.now()
        search_cat = self.categories
        if filter!=None:
            search_cat = filter
        for cat in search_cat:
            pages = self.get_max_pages(cat)
            c_blagues = []
            for current_page in range(1, pages+1):
                print(cat+" : "+str(current_page))
                page = requests.get(self.baseUrl+cat+'-'+str(current_page)+'.html').text
                soup_mysite = BeautifulSoup(page, "html.parser")
                allDivs = soup_mysite.findAll("div", {"class": "blague"})
                for div in allDivs:
                    testDesc = BeautifulSoup(str(div), "html.parser").find("div", {"itemprop": "description"}).findAll("p")
                    if(len(testDesc) == 0):
                        boring = BeautifulSoup(str(div), "html.parser").find("div", {"itemprop": "description"})
                        dtd = boring.find("div", {"class": "lolBox"}).decompose()
                        blague = {'content': self.clean_str(boring.getText().replace("\r","\n").split("\n")), 'category':cat, 'date': now.isoformat()}
                    else:
                        blague = {'content':[], 'category':cat, 'date': now.isoformat()}
                        for item in testDesc:
                           blague['content'].append(html.unescape(str(item).replace("<p>","").replace("</p>","").replace(u'\xa0', u' ').replace('’',"'")))
                    if len(blague['content'])>0:
                        c_blagues.append(blague)
            self.blagues[cat] = c_blagues
    
    def __str__(self):
        return json.dumps(self.blagues, indent=4, sort_keys=True, ensure_ascii=False)
    
    def clean_str(self, listStrBase):
        finalList = []
        for t in listStrBase:
            t = re.sub(r'\s+',' ',t)
            t = re.sub(r'^\s+$','',t)
            t = re.sub(r'^\s','',t)
            if len(t)>1:
               finalList.append(t)
        return finalList
    
    def get_category(self, category, toJson=False):
        if category in self.blagues:
            if toJson:
                return json.dumps(self.blagues[category], indent=4, sort_keys=True, ensure_ascii=False)
            else:
                return self.blagues[category]
    
    def update_category(self, category):
        if category in self.blagues:
            self.parse_website([category])
            self.save_file()
    
    def get_total(self):
        tot = 0
        for k,v in self.blagues.items():
            tot = tot + len(v)
        return tot
    
    def get_random(self, filter=None):
        fullListe = []
        search_cat = self.categories
        if filter!=None:
            search_cat = filter
        for cat in search_cat:
            fullListe = fullListe+self.blagues[cat]
        return random.choice(fullListe)

if __name__ == "__main__":
    b = Blagues()
    print(str(b.get_total()))
    print(b.get_random(['travail']))                      