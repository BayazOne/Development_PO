import datetime
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import re


class File_txt():
    name_file = ''
    def __init__(self, name_file):
        self.name_file = name_file
        function_create = open(name_file, "w")
        function_create.close()

    def write_text_in_file(self, address):
        f = open(self.name_file, 'r')
        info_in_file = f.read()
        f.close()
        if address in info_in_file:
            print("текст уже есть в файле.")
        else:
            write_in_file = open(self.name_file, "a")
            write_in_file.write(address + '\n')
            write_in_file.close()
            print("записано в файл")

    def text(self, text):
        write_in_file = open(self.name_file, "a")
        # добавить сюда что-то вроде внести запись информация записывается в такое-то время, такую-то дату
        current_time = datetime.datetime.now().time()
        current_time = str(current_time)
        info = "News added in " + current_time
        write_in_file.write(info + '\n')
        write_in_file.write(text + '\n')
        write_in_file.close()
        print("записала в файл")

class Parsing_of_site():

    def __init__(self, name_file, url_first_path, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')


        for link in links:
            text = link.text
            if "emocrat" in text or 'epublic' in text:
                try:
                    address = url_first_path + link.get('href')
                    print(address)
                    File_txt.write_text_in_file(File_txt, address)
                except Exception as e:
                    print(f'Ошибка при извлечении новостей: {e}')

        # функция, которая считывает информацию со страницы, где именно упоминается новость и превращает
        # в текст, который готов для записи в файл
    def read_news_internet_page(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            new_heading = soup.title.text
            new_annotation = soup.p.text
            new_author = soup.find('span', 'byline__name').text
            text = url + "\nHeading: " + new_heading + "\nAnnotation: " + new_annotation + "\nAuthor: " + new_author
            return text
        except Exception as e:
            print(f'Ошибка при извлечении новостей: {e}')



# Основная функция для запуска скрипта на определенное время
def run_script(duration_hours, name_file):
    end_time = datetime.now() + timedelta(hours=duration_hours)
    print(f'Скрипт запущен на {duration_hours} часов. Время окончания: {end_time}')


    while datetime.now() < end_time:
        # URL новостного агентства https://ria.ru/organization_Respublikanskaja_partija_SSHA/
        url_first_path = 'https://edition.cnn.com'
        url = "https://edition.cnn.com/politics"
        Parsing_of_site.__init__(Parsing_of_site, name_file, url_first_path, url)
        write_in_file = open(name_file, "a")
        write_in_file.write('Addresses were found' + '\n')
        write_in_file.close()
        # Пауза перед следующим запросом (например, 10 минут(2))
        time.sleep(600)
        current_time = datetime.now().time()
        current_time = str(current_time)
        print('Новый запуск поиска в \n' + current_time)



    f = open(name_file, 'r+')
    info_in_file = f.readlines()
    f.truncate(0)
    f.close()
    key = 'Addresses were found\n'
    index = info_in_file.index(key)
    del info_in_file[:index]
    for i in range(len(info_in_file)):
        if info_in_file[i] == key:
            print('just key')
        else:
            text = Parsing_of_site.read_news_internet_page(Parsing_of_site, info_in_file[i])
            f = open(name_file, 'a')
            f.write(text)
            f.close()



# Запуск скрипта на 4 часа
name_file = "News.txt"
File_txt.__init__(File_txt, name_file)
run_script(4, name_file)

