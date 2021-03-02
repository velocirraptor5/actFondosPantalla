import requests
import bs4
from common import config

class MoviesPage:
    def __init__(self,movies_site_uid,url):
        self._config = config()['movies_sites'][movies_site_uid]
        self._queries = self._config['queries']
        self._html= None
        self._visit(url)
    
    def _select(self,query_string):
        return self._html.select(query_string)
    
    def _visit(self,url):
        response = requests.get(url)
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text,'html.parser')


class HomePage(MoviesPage):
    def __init__(self,movies_site_uid,url):
        super().__init__(movies_site_uid,url)
    @property
    def movies_links(self):
        links_list = []
        for link in self._select(self._queries['homepage_movie_link']):
            if link and link.has_attr('href'):
                links_list.append(link) 
        return set(link['href'] for link in links_list)

class MoviePage(MoviesPage):
    def __init__(self,movies_site_uid,url):
        super().__init__(movies_site_uid,url)
    
    @property
    def poster(self):
        result = self._select(self._queries['movie_poster'])

        return result[0].text if len(result) else ''
    
    @property
    def title(self):
        result = self._select(self._queries['movie_title'])

        return result[0].text if len(result) else ''
    


