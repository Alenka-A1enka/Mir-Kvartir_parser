#в файл: ссылку на объявление, контактный телефон, цену и описание
#отсортировать записи в файле по цене покупки

import requests
from bs4 import BeautifulSoup
import docx


class HabrPythonNews:
    def __init__(self, price_from, price_to, one_room = False, two_room = False, third_room = False):
        self.current_page = 0
        self.price_from = price_from
        self.price_to = price_to
        self.one_room = one_room
        self.two_room = two_room
        self.third_room = third_room
        
    def get_next_page(self):
        self.current_page += 1
        if self.current_page == 2:
            return False
        current_url = self.__get_next_url() #получаем ссылку
        html = self.__get_html(current_url)
        if html != False:
            return self.__get_python_news(html)
        else:
            print('done')
            return False
    
    def __get_next_url(self):
        if self.current_page < 1 or self.current_page > 1000:
            raise IndexError
        page = str(self.current_page)
        
        rooms = self.__rooms_check()
        
        url = 'https://www.mirkvartir.ru/listing/?locationIds=MK_Town%7C32557&p=' + page + '&by=2&sort=0&' + rooms + '&priceFrom=' + str(self.price_from) + '&priceTo=' + str(self.price_to)
        return url
    
    def __rooms_check(self):
        current_rooms = []
        rooms = ''
        if self.one_room:
            current_rooms.append('oneRoom=true')
        if self.two_room:
            current_rooms.append('twoRooms=true')
        if self.third_room:
            current_rooms.append('threeRooms=true')
            
        for room in current_rooms:
            if rooms == '':
                rooms += room
            else:
                rooms += '&' + room
        if rooms == '':
            return 'oneRoom=true&twoRooms=true&threeRooms=true'
        else:
            return rooms
    
    def __get_html(self, url):
        try:
            headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            result = requests.get(url, headers=headers)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            print('server error')
            return False
    
    def __get_python_news(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        lst0 = soup.find_all('a', class_='OffersListItem_offerTitle__3GQ_0')
        titles = []
        for title in lst0:
            titles.append(title.text)
        
        lst1 = soup.find_all('div', class_='OffersListItem_offerTitleContainer__2netd')
        hrefs = []
        for news in lst1:
            hrefs.append('Ссылка на объявление: ' + str(news.a['href']))
        
        lst2 = soup.find_all('div', class_ = 'OfferAddress_address__2O-MU')
        address = []
        for l in lst2:
            address.append('Адрес квартиры: ' + str(l.text))
        
        lst3 = soup.find_all('span', class_ = 'OfferPrice_price__1jdEj')
        price = []
        for l in lst3:
            string = l.text
            price.append('Цена: ' + string)
        
        
        return {'titles': titles, 'hrefs': hrefs, 'address': address, 'price': price}

class PrepareData:
    @staticmethod
    def prepare_data(dct):
        string = ''
        
        keys_ = []
        for key in dct:
            keys_.append(key)
        
        if len(keys_) == 0:
            return ''
        
        for i in range(len(dct[keys_[0]])):
            for j in range(len(keys_)):
                string += str(dct[keys_[j]][i]) + '\n'
            string += '\n'
        return string


class WorkWithDct:
    def __init__(self, data, path):
        self.__data = data
        self.path = path
    
    def write_to_file(self):
        mydoc = docx.Document()
        mydoc.add_paragraph(self.__data)
        mydoc.save(self.path)
        
        
class Parser:
    def __init__(self):
        self.__data = ''
        
    def get_last_data(self):
        return self.__data
        
    def parsing_mir_kvartir(self, price_from, price_to, one_room, two_room, third_room):
        habr = HabrPythonNews(price_from=price_from, price_to=price_to, one_room=one_room, two_room=two_room, third_room=third_room)
        result = {}
        while True:
            dct = habr.get_next_page()
            if dct != False:
                for key in dct:
                    if key not in result:
                        result[key] = dct[key]
                    else:
                        result[key] = result[key].extend(dct[key])
                pass
            else:
                break
        self.__data = PrepareData.prepare_data(result)

    def write_dct_to_docx(self):
        doc = WorkWithDct(self.__data, 'квартиры.docx')
        doc.write_to_file()
    
# parser = Parser()
# parser.parsing_mir_kvartir(price_from=3000000, price_to=4000000)
# print(parser.get_last_data())

