import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
def my_parsing(flag, themes_dict, data):
    for theme in themes_dict:
        if flag == 'past':
            actions = "https://ict2go.ru/events/?list=past&event_theme=" + str(theme)
        else:
            actions = f"https://ict2go.ru/events/?region=&event_type=&event_theme={theme}&date_begin=&date_end=&list="
        try:
            r = requests.get(actions)
        except:
            print('error')
            time.sleep(10)
            r = requests.get(actions)
        soup = BeautifulSoup(r.text, "lxml")
        actions_list = soup.find('div', class_="main container").find('main').find_all('div', class_ = "index-events")[1].find_all('div', class_="index-events-item media")
        if len(actions_list) > 0:
            for item in actions_list:
                try:
                    r1 = requests.get('https://ict2go.ru'+item.find('a').get('href'))
                except requests.exceptions.ConnectionError:
                    print('error')
                    time.sleep(10)
                    r1 = requests.get('https://ict2go.ru' + item.find('a').get('href'))
                print('error ok')
                soup1 = BeautifulSoup(r1.text, "lxml")
                action_name = soup1.find('div', class_="main container").find('main').find('div',class_="main-content").find('h1',class_="event-h1").text
                action_category = themes_dict[theme]
                action_description = soup1.find('div', class_="main container").find('main').find('div', class_="main-content").find('div',class_='tabs').find('div',class_="tabs-content").find('div',class_= "tab-item description-info").text
                data.append({'id': item.find('a').get('href'),'action_name':action_name,'action_category':action_category,'action_description':action_description})
        break


#data = pd.DataFrame(columns=['action_name','action_category','action_description'])
def main_func():
    url="https://ict2go.ru/events/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"lxml")

    themes_list=soup.find('div', class_="main container").find('main').find('div', class_= "filter-form").find('form').find_all('div', class_= "filter-row")[1].find('select', {'name': "event_theme"}).find_all('option')[1:]
    themes_dict=dict({})
    for theme in themes_list:
        themes_dict[int(theme.get('value'))] = theme.text
    data = []
    my_parsing('past', themes_dict, data)
    my_parsing('future', themes_dict, data)
    return pd.DataFrame(data)
print(main_func())