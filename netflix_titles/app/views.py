from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import requests
import random
import string

from .wikiRepository import WikiRepository

from app.repository import Repository

from .DbpediaRepository import DbpediaRepository



repo_name = "netflix"
endpoint = "http://localhost:7200"
repository = Repository(repo_name, endpoint)

# Wikidata Connection
wiki_endpoint = "https://query.wikidata.org/sparql"
wikiRepository = WikiRepository(wiki_endpoint)

#Dbpedia Connection
dbpedia_endpoint = "https://dbpedia.org/sparql"
dbpedia = DbpediaRepository(dbpedia_endpoint)


# Create your views here.
def home(request):
    assert isinstance(request, HttpRequest)

    movies = repository.getNumberMovies()
    tvShows = repository.getNumberTvShows()

    tparams = {
        'base': 'base.html',
        'movies': movies[0]['n_movies'],
        'tv_shows': tvShows[0]['n_tvShow']
    }

    return render(request, 'home.html', tparams)


def movies(request):
    assert isinstance(request, HttpRequest)

    if 'directed' in request.POST:
        new_title = request.POST['title']
        new_directed = request.POST['directed']
        new_year = request.POST['year']
        new_category = request.POST['category']
        new_cast = request.POST['cast']

        repository.edit(old_title, old_directed, old_year, old_category, old_cast, new_title, new_directed, new_year,
                        new_category, new_cast)

    moviesInfo = repository.getMovies()
    movies = len(moviesInfo)

    tparams = {
        'movies': [],
        'base': 'base.html'
    }

    for i in range(movies):
        aux = {'title': moviesInfo[i].get('title'), 'director': moviesInfo[i].get('directed_by'),
               'release_year': moviesInfo[i].get('release_year'), 'listed_in': moviesInfo[i].get('listed_in'),
               'cast': moviesInfo[i].get('cast'), 'duration': moviesInfo[i].get('duration')}

        tparams['movies'].append(aux)

    return render(request, 'movies.html', tparams)


def tvshows(request):
    assert isinstance(request, HttpRequest)

    if 'directed' in request.POST:
        new_title = request.POST['title']
        new_directed = request.POST['directed']
        new_year = request.POST['year']
        new_category = request.POST['category']
        new_cast = request.POST['cast']

        repository.edit(old_title, old_directed, old_year, old_category, old_cast, new_title, new_directed, new_year,
                        new_category, new_cast)
    tvShowsInfo = repository.getTvShows()
    tvShows = len(tvShowsInfo)
    tparams = {
        'tvShows': [],
        'base': 'base.html'
    }

    for i in range(tvShows):
        aux = {'title': tvShowsInfo[i].get('title'), 'director': tvShowsInfo[i].get('directed_by'),
               'release_year': tvShowsInfo[i].get('release_year'), 'listed_in': tvShowsInfo[i].get('listed_in'),
               'cast': tvShowsInfo[i].get('cast'), 'duration': tvShowsInfo[i].get('duration')}
        tparams['tvShows'].append(aux)

    return render(request, 'tvshows.html', tparams)


def search(request):
    assert isinstance(request, HttpRequest)

    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            results = repository.build_search(keyword)

            #
            # FAZER QUERY PARA VER O LIVRO
            #
            book = dbpedia.get_book(keyword)
            if book != []:
                book = book[0]['book']['value'].replace('_', ' ').replace('http://dbpedia.org/resource/','')+(' (source: '+book[0]['book']['value']+')')
            if not book:
                book = 'Not available'

            return render(request, 'search_results.html',
                          {'keyword': keyword, 'base': 'base.html', 'results': results, 'nResults': len(results) , 'book': book})
        else:
            return render(request, 'search.html', {'error': True, 'base': 'base.html'})
    else:
        return render(request, 'search.html', {'error': False, 'base': 'base.html'})


def add(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        type = request.POST['type']
        title = request.POST['title']
        directed = request.POST['directed_by']
        cast = request.POST['cast']
        country = request.POST['country']
        date = request.POST['date']
        release = request.POST['release']
        duration = request.POST['duration']
        listed_in = request.POST['listed_in']

        letters = string.ascii_lowercase
        id = (''.join(random.choice(letters) for i in range(10)))

        results = repository.addTitle(id, type, title, directed, cast, country, date, release, duration, listed_in)

    return render(request, 'add.html', {'base': 'base.html'})


def search_by_release_year(request):
    assert isinstance(request, HttpRequest)

    if 'from' in request.POST and 'to' in request.POST:
        from_year = request.POST['from']
        to = request.POST['to']

        if from_year and to and from_year.isnumeric() and to.isnumeric():
            if from_year > to:
                return render(request, 'year.html', {'error': True, 'base': 'base.html'})
            results = repository.search_year(from_year, to)

            return render(request, 'year_results.html',
                          {'from': from_year, 'to': to, 'base': 'base.html', 'results': results,
                           'nResults': len(results)})
        else:
            return render(request, 'year.html', {'error': True, 'base': 'base.html'})
    else:
        return render(request, 'year.html', {'error': False, 'base': 'base.html'})


def edit(request, title="", directed_by=""):
    assert isinstance(request, HttpRequest)

    if title:

        results = repository.search_title(title)

        if results[0]['type'] == 'TV Show':
            results[0]['type'] = 'tvshow'
        elif results[0]['type'] == 'Movie':
            results[0]['type'] = 'movie'

        results[0]['category'] = results[0]['listed_in']

        results = results[0]

        global old_title
        old_title = results['title']

        global old_directed
        old_directed = results['directed_by']

        global old_category
        old_category = results['category']

        global old_year
        old_year = results['release_year']

        global old_cast
        old_cast = results['cast']

        return render(request, 'edit_results.html', {'results': results, 'base': 'base.html'})

    return render(request, 'edit.html', {'error': False, 'base': 'base.html'})


def person(request, name=''):
    results = repository.person_movies(name)

    results_final = []
    for result in results:
        if name in result['actor'] and name in result['directed_by']:
            results_final.append([result['title'], result['actor'], result['directed_by'], 'Actor'])
            results_final.append([result['title'], result['actor'], result['directed_by'], 'Director'])
        elif name in result['actor']:
            results_final.append([result['title'], result['actor'], result['directed_by'], 'Actor'])
        elif name in result['directed_by']:
            results_final.append([result['title'], result['actor'], result['directed_by'], 'Director'])

    """"[{'director': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q103646'},
      'birthDate': {'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime', 'type': 'literal',
                    'value': '1954-03-01T00:00:00Z'}}]
    """

    director_name = wikiRepository.director_name(name)

    id = ""
    desc = ""
    birth = ""
    awards = ""

    if director_name !=  []:
        id = director_name[0]['director']['value'].split("/")[-1]
        description = wikiRepository.director_description(id)
        desc = description[0]['o']['value'] # fazer query para ter descrição
        birth = director_name[0]['birthDate']['value'][:10]# fazer query para ter data de nascimento
        awards = wikiRepository.director_awards(id)  # fazer query para awards
        #awards = awards[0]['awardsReceivedLabel']

        aux = ""
        for award in awards:
            aux += award['awardsReceivedLabel']['value']+"; "
        awards = aux

    if desc == "":
        desc = "No description available"
    if birth == "":
        birth = "No birth date available"
    if awards == "":
        awards = "No awards available"

    return render(request, 'person_results.html',
                  {'base': 'base.html', 'results': results_final, 'desc': desc, 'birth': birth, 'awards': awards})


def delete_movie(request, title=''):
    # print(title)

    results = repository.del_movies(title)

    # query para obter os filmes
    moviesInfo = repository.getMovies()
    movies = len(moviesInfo)

    tparams = {
        'movies': [],
        'base': 'base.html'
    }

    for i in range(movies):
        aux = {'title': moviesInfo[i].get('title'), 'director': moviesInfo[i].get('directed_by'),
               'release_year': moviesInfo[i].get('release_year'), 'listed_in': moviesInfo[i].get('listed_in'),
               'cast': moviesInfo[i].get('cast'), 'duration': moviesInfo[i].get('duration')}

        tparams['movies'].append(aux)

    return render(request, 'movies.html', tparams)


def delete_tvshow(request, title=''):
    # print(title)

    results = repository.del_movies(title)

    # query para obter os filmes
    tvShowsInfo = repository.getTvShows()
    tvShows = len(tvShowsInfo)
    tparams = {
        'tvShows': [],
        'base': 'base.html'
    }

    for i in range(tvShows):
        aux = {'title': tvShowsInfo[i].get('title'), 'director': tvShowsInfo[i].get('directed_by'),
               'release_year': tvShowsInfo[i].get('release_year'), 'listed_in': tvShowsInfo[i].get('listed_in'),
               'cast': tvShowsInfo[i].get('cast'), 'duration': tvShowsInfo[i].get('duration')}
        tparams['tvShows'].append(aux)

    return render(request, 'tvshows.html', tparams)

def country(request):

    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            results = repository.inf_country(keyword)

            return render(request, 'country_results.html',
                          {'keyword': keyword, 'base': 'base.html', 'results': results, 'nResults': len(results) })
        else:
            return render(request, 'country.html', {'error': True, 'base': 'base.html'})
    else:
        return render(request, 'country.html', {'error': False, 'base': 'base.html'})


def work(request):

    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            results = repository.inf_actor(keyword)
            print(results)

            current_actor = ""
            new_results = {}
            for i in results:
                new_results[i['actor1']] = []

            for i in results:
                new_results[i['actor1']].append(i['actor2'])

            results = new_results

            """results = {
                'João Assunção' : ['A', 'B', 'C'],
                'Paulo Santos' : ['D', 'E', 'F']
            }
            """
            return render(request, 'work_results.html',
                          {'keyword': keyword, 'base': 'base.html', 'results': results, 'nResults': len(results) })
        else:
            return render(request, 'work.html', {'error': True, 'base': 'base.html'})
    else:
        return render(request, 'work.html', {'error': False, 'base': 'base.html'})