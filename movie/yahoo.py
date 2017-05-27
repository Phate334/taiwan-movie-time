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
    soup = get_soup(HOST + '/theater_list.html')
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
            theater = {}
            theater["name"] = td[0].get_text()
            theater["area_id"] = area_id
            theater["url"] = td[0].find('a')['href'].split('*')[1]
            theater["id"] = re.search(r'\d+', theater["url"]).group()
            theater["address"] = td[1].contents[0]
            theater["tel"] = td[1].contents[1].get_text()
            yield theater

def get_theater_time(theater_id):
    """ time data on the theater page.
    """
    soup = get_soup(HOST + "/theater_result.html/id=" + str(theater_id))
    movie_div_list = soup.find_all("div", {"class":["row", "row_last"]})
    result = []
    for div in movie_div_list:
        movie = {}
        movie["url"] = div.find("h4").a["href"].split('*')[1]
        movie["id"] = re.search(r'\d+', movie["url"]).group()
        movie["title_tw"] = div.find("h4").text
        movie["mvtype"] = []
        for img in div.find("span", class_="mvtype").find_all("img"):
            movie["mvtype"].append(
                re.search('icon_(.*).gif', img["src"]).group(1))
        movie["time"] = []
        for span in div.find_all("span", class_="tmt"):
            movie["time"].append(span.text)
        result.append(movie)
    return result

def get_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")