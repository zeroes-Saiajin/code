# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Servant:
    def __init__(self, data):
        self.name = data.contents[4].contents[0].contents[2]
        self.max_hp = int(data.contents[9].text.strip().replace(',', ''))
        self.max_atk = int(data.contents[10].text.strip().replace(',', ''))

    def calc_value(self):
        return (self.max_atk + self.max_hp) / 2 #у

    def __repr__(self):
        return self.name + (" Max HP(%d), Max ATK(%d)" % (self.max_hp, self.max_atk))

if __name__ == '__main__':
    url = r"http://fate-go.cirnopedia.org/servant_all.php"
    data = requests.get(url)
    if data.status_code != 200: 
        raise ConnectionError("Connection interrupted")
    html = data.text
    tree = BeautifulSoup(html, 'lxml')  # may require to `pip install lxml`
    servants_data = tree.find('tbody') #поиск в сайте tbody
    servants = dict()#создаём словарь,записывает в себя имя серванта и его хр и атк(тут не понял как работает)
    for servant_data in servants_data.find_all('tr'):
        if 'class' in servant_data.contents[4].attrs:
            continue  # unplayable
        if servant_data.attrs['class'][0] == ('JP'):
            continue  # skip JP servants
        servant_name = servant_data.contents[4].contents[0].contents[2]
        servant_max_hp = int(servant_data.contents[9].text.strip().replace(',', ''))
        servant_max_atk = int(servant_data.contents[10].text.strip().replace(',', ''))
        servant_value = (servant_max_atk + servant_max_hp) / 2
        servants[servant_name] = servant_value
    max_val = max(servants.values())
    max_len = max(len(name) for name in servants)
    ordered_servants = list(sorted(servants, key=lambda x: servants[x], reverse=True))
    for servant in ordered_servants:
        print(servant + '.' * (max_len - len(servant)), '%.02f' % ((servants[servant] / max_val) * 100) + '%')
