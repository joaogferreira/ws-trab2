from SPARQLWrapper import SPARQLWrapper, JSON

from .DbpediaConnection import DbpediaDB

import datetime

class DbpediaRepository:
    book= """
    select distinct *
    { 
    ?movie dbo:basedOn ?book .
    ?movie foaf:name 'Catch Me If You Can'@en .
    ?book a dbo:Book .
    }
    """

    def get_book(self,name):
        query_base = "select distinct * { ?movie dbo:basedOn ?book . ?movie foaf:name ?name . filter (regex(?name, '"+name+"', 'i')) . ?book a dbo:Book .}"
        print(query_base)
        res = self.DbpediaDB.getResults(query_base)
        print(res)
        return res

    def __init__(self, endpoint):
        self.DbpediaDB = DbpediaDB(endpoint)