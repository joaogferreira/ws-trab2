from app.graphDBConnection import GraphDB


class Repository:

    #Get the number of movies
    nMovies= """
           PREFIX net:<http://netflix-titles.com/pred/>
            Select (COUNT(?movie) as ?n_movies)
                where{
                    ?movies net:type ?movie .
                        Filter(?movie = 'Movie')
                }	 
    """

    # Get the number of movies
    nTVShows = """
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select (COUNT(?tv_show) as ?n_tvShow)
        where{
            ?tv_shows net:type ?tv_show .
                Filter(?tv_show = 'TV Show')
        }	
    """

    # Get movies
    movies = """
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type "Movie" .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        }
        Limit 10
    """

    tvShows ="""
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type "TV Show" .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        }
        Limit 10
    """

    directors = """
    PREFIX net:<http://netflix-titles.com/pred/>
    
    Select distinct ?director
        where{
            ?film net:directed_by ?director .
        }
    """

    titles = """
    PREFIX net:<http://netflix-titles.com/pred/>
    
    Select distinct ?title
        where{
            ?film net:title ?title .
        }
    """

    categories = """
    PREFIX net: < http: // netflix - titles.com / pred / >

    Select distinct ?listed_in
        where{ 
        ?film net: listed_in ?listed_in.
    }
    """

    actores = """
    PREFIX net:<http://netflix-titles.com/pred/>

    Select distinct ?cast
        where{
            ?film net:cast ?cast .
        }
    """

    search = """
    PREFIX net:<http://netflix-titles.com/pred/>

    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type ?type .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        filter ( contains (?title, 'Casa') || contains (?directed_by, 'Casa') || contains (?cast, 'Casa') || contains(?listed_in, 'Casa'))
    
        }
    """

    search_by_title = """
    PREFIX net:<http://netflix-titles.com/pred/>

    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type ?type .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        filter ( contains (?title, 'Casa'))

        }
    """
    edit = """
        #Editar campos
        PREFIX net: <http://netflix-titles.com/pred/>
        PREFIX n: <http://netflix-titles.com/>
        
        DELETE { 
           ?title net:title "Web Semantica" .
           ?type net:type "Movie" .
           ?directed net:directed_by "Magalhães" .
           ?cast net:cast "Ferreira" .
           ?year net:release_year "FM" .
         }
        INSERT {
           ?title net:title "Novo Web Semantica" .
           ?type net:type "TV Show" .
           ?directed net:directed_by "Magalhães" .
           ?cast net:cast "Ferreira" .
           ?year net:release_year "FM Novo" .
        }
        WHERE { 
           ?title net:title "Web Semantica" .
           ?type net:type "Movie" .
           ?directed net:directed_by "Magalhães" .
           ?cast net:cast "Ferreira" .
           ?year net:release_year "FM" .
        }
    """

    person_movies= """
    PREFIX net: <http://netflix-titles.com/pred/>
    PREFIX pred: <http://netflix-titles.com/pred/>
    prefix xsd:<http://www.w3.org/2001/XMLSchema#> 
    
    select ?actor ?director ?film
    where{
        ?f net:directed_by ?director .
        ?f net:cast ?actor .
        ?f net:title ?film .
        Filter(regex (?director, 'Spielberg', 'i') || regex (?actor, 'Spielberg', 'i'))
    }
    """

    del_movies="""
    
    PREFIX net:<http://netflix-titles.com/pred/>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    PREFIX n: <http://netflix-titles.com/>
    
    delete where { 
       ?t net:title "Web Semantica" .
    }
    """

    #Inferencias

    inf_country = """
        PREFIX net: <http://netflix-titles.com/pred/>
        
        select ?s1n ?s2n ?country
        where{
            ?s1 net:worked_in_country ?s2 .
            ?s1 net:country ?country .
            ?s1 net:title ?s1n .
            ?s2 net:title ?s2n .
            filter (regex (?country, 'United States', 'i'))
        }limit 15
    """
    inf_actor = """
        PREFIX net: <http://netflix-titles.com/pred/>

        select ?p1n ?p2n
        where{
            ?p1 net:worked_with ?p2 .
            ?p1 net:name ?p1n .
            ?p2 net:name ?p2n .
            filter (regex (?p1n, 'João', 'i'))
        }limit 15
    """

    def inf_actor (self, name):
        create_query = "PREFIX net: <http://netflix-titles.com/pred/> Construct {?p1 net:worked_with ?p2} WHERE { ?p1 net:acted_in ?mov . ?p2 net:acted_in ?mov . FILTER (?p1 != ?p2)}"
        self.graphDB.add(create_query)
        query_base = "PREFIX net: <http://netflix-titles.com/pred/> select ?p1n ?p2n where{ ?p1 net:worked_with ?p2 . ?p1 net:name ?p1n . ?p2 net:name ?p2n . filter (regex (?p1n, '"+name+"', 'i')) }limit 15"
        list = []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['actor1'] = i['p1n']['value']
            dic['actor2'] = i['p2n']['value']
            list.append(dic)
        return list

    def inf_country(self, country):
        create_query = "PREFIX net: <http://netflix-titles.com/pred/> Insert {?p1 net: worked_in_country ?p2} WHERE { ?p1 net: country ?mov. ?p2 net: country ?mov. FILTER(?p1 != ?p2 & & ?p2 !=?p1)}"
        self.graphDB.add(create_query)
        query_base = "PREFIX net: <http://netflix-titles.com/pred/>  select ?s1n ?s2n ?country where{ ?s1 net:worked_in_country ?s2 . ?s1 net:country ?country . ?s1 net:title ?s1n . ?s2 net:title ?s2n . filter (regex (?country, '"+country+"', 'i')) }limit 15"
        list = []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['title1'] = i['s1n']['value']
            dic['title2'] = i['s2n']['value']
            dic['country'] = i['country']['value']
            list.append(dic)
        return list

    def del_movies(self, title):
        title = title.strip()
        query_base = "PREFIX net:<http://netflix-titles.com/pred/> delete where { ?t net:title '"+title+"' . }"
        res = self.graphDB.add(query_base)
        return res

    def person_movies(self, name):
        query_base = "PREFIX net: <http://netflix-titles.com/pred/> select ?actor ?director ?film where{ ?f net:directed_by ?director . ?f net:cast ?actor .  ?f net:title ?film . Filter(regex (?director, '"+name+"', 'i') || regex (?actor, '"+name+"', 'i')) }"
        list = []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['actor'] = i['actor']['value']
            dic['title'] = i['film']['value']
            dic['directed_by'] = i['director']['value']
            list.append(dic)
        return list

    def edit(self, old_title, old_directed, old_year, old_category, old_cast, new_title, new_directed, new_year, new_category, new_cast):
        query_base1 = "PREFIX net:<http://netflix-titles.com/pred/> DELETE { ?title net:title '"+old_title+"'.  ?directed net:directed_by '"+old_directed+"'. ?cast net:cast '"+old_cast+"'. ?year net:release_year '"+old_year+"'. ?category net:listed_in '"+old_category+"'.}"
        query_base2 = "INSERT { ?title net:title '"+new_title+"'.  ?directed net:directed_by '"+ new_directed+"'. ?cast net:cast '"+new_cast+"'. ?year net:release_year '"+new_year+"'. ?category net:listed_in '"+new_category+"'.}"
        query_base3 = "WHERE { ?title net:title '"+old_title+"'.  ?directed net:directed_by '"+old_directed+"'. ?cast net:cast '"+old_cast+"'. ?year net:release_year '"+old_year+"'. ?category net:listed_in '"+old_category+"'.}"
        query_base = query_base1 + query_base2 + query_base3

        res = self.graphDB.add(query_base)
        #print(res)




    def search_title(self, title):
        query_base = "PREFIX net:<http://netflix-titles.com/pred/> Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in where{ ?film net:type ?type . ?film net:title ?title . ?film net:directed_by ?directed_by . ?film net:cast ?cast . ?film net:country ?country . ?film net:date_added ?date_added . ?film net:release_year ?release_year . ?film net:duration ?duration . ?film net:listed_in ?listed_in . filter ( contains (?title,'" +title+"'))}"
        list= []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['type'] = i['type']['value']
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def build_search(self, keyword):
        query_base = "PREFIX net:<http://netflix-titles.com/pred/> Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in where{ ?film net:type ?type . ?film net:title ?title . ?film net:directed_by ?directed_by . ?film net:cast ?cast . ?film net:country ?country . ?film net:date_added ?date_added . ?film net:release_year ?release_year . ?film net:duration ?duration . ?film net:listed_in ?listed_in ."
        aux = " filter ( regex (?title, '" + keyword +"', 'i' ) || regex (?directed_by, '" + keyword +"', 'i') || regex (?cast, '" + keyword +"', 'i') || regex (?listed_in, '" + keyword +"', 'i'))}"
        query_base = query_base + aux

        list= []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['type'] = i['type']['value']
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list
    def search_year(self, year1, year2):
        query_base = "PREFIX net:<http://netflix-titles.com/pred/> Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in where{ ?film net:type ?type . ?film net:title ?title . ?film net:directed_by ?directed_by . ?film net:cast ?cast . ?film net:country ?country . ?film net:date_added ?date_added . ?film net:release_year ?release_year . ?film net:duration ?duration . ?film net:listed_in ?listed_in . filter(?release_year >= '"+ year1 +"' && ?release_year <='"+ year2 +"' )} order by asc (?release_year)"
        list = []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['type'] = i['type']['value']
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def addTitle(self, id, type, title, directed_by, cast, country, date_added, release_year, duration, listed_in ):
        query = "PREFIX net:<http://netflix-titles.com/pred/> Insert data{ net:"+id+" net:type '"+ type +"'^^xsd:string; net:title '"+ title + "'^^xsd:string; net:directed_by '"+ directed_by +"'^^xsd:string; net:cast '"+ cast +"'^^xsd:string; net:country '"+ country +"'^^xsd:string; net:date_added '"+ date_added +"'^^xsd:string; net:release_year '"+ release_year +"'^^xsd:string; net:duration '"+ duration +"'^^xsd:string; net:listed_in '"+ listed_in +"'^^xsd:string. }"
        #print(query)
        return self.graphDB.add(query)

    def __init__(self, repo_name, endpoint):
        self.graphDB = GraphDB(endpoint, repo_name)

    def getNumberMovies(self):
            list = []
            res = self.graphDB.getResults(self.nMovies)
            for i in res[:5]:
                dic = {}
                dic['n_movies'] = i['n_movies']['value']
                list.append(dic)
            return list

    def getNumberTvShows(self):
        list = []
        res = self.graphDB.getResults(self.nTVShows)
        for i in res[:5]:
            dic = {}
            dic['n_tvShow'] = i['n_tvShow']['value']
            list.append(dic)
        return list

    def getMovies(self):
        list = []
        res = self.graphDB.getResults(self.movies)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def getTvShows(self):
        list = []
        res = self.graphDB.getResults(self.tvShows)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def getDirectors(self):
        list = []
        res = self.graphDB.getResults(self.directors)
        for i in res:
            dic = {}
            dic['director'] = i['director']['value']
            list.append(dic)
        return list

    def getTitles(self):
        list = []
        res = self.graphDB.getResults(self.titles)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            list.append(dic)
        return list

    def getCategories(self):
        list = []
        res = self.graphDB.getResults(self.categories)
        for i in res:
            dic = {}
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def getActors(self):
        list = []
        res = self.graphDB.getResults(self.actores)
        for i in res:
            dic = {}
            dic['cast'] = i['cast']['value']
            list.append(dic)
        return list