import re

import requests
from bs4 import BeautifulSoup


HOST = 'https://tw.movies.yahoo.com'

def get_theaters():
    """ yield theater's meta data.

    Yield:
        {
            'id': theater id,
            'name': name,
            'area_id': area_id,
            'address': address,
            'url': url,
            'tel': tel
        }
    """
    for area in get_areas():
        for theater in area_theater_parser(area[0]):
            yield theater

def get_areas():
    """ return area's id and name in Yahoo movie.

    Return:
        [(area_id, area_name),...]

        area_id: Parameter for /theater_list.html .
    """
    res = requests.get(HOST + '/theater_list.html')
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return [(opt['value'], opt.get_text()) for opt in soup.find(id='area').find_all('option')][1:]

def area_theater_parser(area_id):
    """ parsing theater query result.
    """
    data = {'area':area_id}
    res = requests.post(HOST + '/theater_list.html', data=data)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    for g in soup.find_all(class_='group'):
        for theater in g.find('tbody').find_all('tr'):
            td = theater.find_all('td')
            name = td[0].get_text()
            url = td[0].find('a')['href'].split('*')[1]
            t_id = re.search(r'\d+', url).group()
            address = td[1].contents[0]
            tel = td[1].contents[1].get_text()
            yield {
                'id': t_id,
                'name': name,
                'area_id': area_id,
                'address': address,
                'url': url,
                'tel': tel
                }
