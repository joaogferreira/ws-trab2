from SPARQLWrapper import SPARQLWrapper, JSON

from .WikiConnection import WikiDB

import datetime

class WikiRepository:
    director_name = """
        SELECT DISTINCT ?director ?birthDate
        WHERE
        {
          ?director wdt:P1559 ?directorLabel;
            wdt:P569 ?birthDate .
            FILTER(STRSTARTS(?directorLabel, 'Steven Spielberg')) .
        }
    """

    def __init__(self, endpoint):
        self.wikiDB = WikiDB(endpoint)

    def director_name(self, name):
        query_base = "SELECT DISTINCT ?director ?birthDate WHERE  { ?director wdt:P1559 ?actorLabel; wdt:P569 ?birthDate . FILTER(STRSTARTS(?actorLabel, '" + name + "')) .}"
        #query_base = "Select * where{ ?s ?p ?o} limit 5"
        res = self.wikiDB.getResults(query_base)
        #print(res)
        return res

    def director_description(self, id):
        query_base = "Select ?o where{ wd:"+id+"  schema:description ?o . filter(lang(?o) = 'en') }"
        res = self.wikiDB.getResults(query_base)
        print(res)
        return res

    def director_awards(self,id):
        query_base = 'SELECT ?awardsReceivedLabel ' \
              'WHERE { wd:' + id + ' wdt:P166 ?awardsReceived . ' \
              'SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".} 	' \
              '}'
        res = self.wikiDB.getResults(query_base)
        print(res)
        return res
