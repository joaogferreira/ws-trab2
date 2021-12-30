from SPARQLWrapper import JSON, SPARQLWrapper


class DbpediaDB:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    # Get query results
    def getResults(self, query):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            result = sparql.query().convert()['results']['bindings']
        except:
            result = []
        return result