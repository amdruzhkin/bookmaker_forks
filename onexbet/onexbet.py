import asyncio
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Onexbet:
    def __init__(self, browser):
        self.browser = browser
        self.line_events = {}

    def run(self):
        self.get_line_events()
        print(f'1xBet events: {len(self.line_events)}')
        with open('onexbet_result.json', 'w', encoding='utf-8') as f:
            json.dump(self.line_events, f, ensure_ascii=False, indent=4)

    def get_line_events(self):
        endpoints = ['football', 'volleyball', 'basketball', 'tennis', 'ice-hockey']
        event_ids = []
        for endpoint in endpoints:
            url = f'https://1xstavka.ru/line/{endpoint}'
            try:
                self.browser.get(url)
                xpath = '//*[@id="games_content"]/div/div[2]/div/div[1]'
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except Exception as e:
                print('element not found')
                self.browser.quit()

            children = BeautifulSoup(self.browser.page_source, 'html.parser').findAll('div', re.compile(
                'c-events__item c-events__item_col dashboard-champ-content__event-item'))


            for child in children:
                try:
                    event_ids.append(child.find('a')['href'].split('/')[-1].split('-')[0])
                except Exception as e:
                    ...


        for event_id in event_ids:
            self.get_event(event_id)


    def get_event(self, event_id):
        url = f'https://1xstavka.ru/LineFeed/GetGameZip?id={event_id}&isSubGames=true&GroupEvents=true&allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1&gr=44&isNewBuilder=true'
        response = requests.get(url).json()['Value']
        try:
            team_1 = str(response["O1"]).replace('(жeн)', '')
            team_1 = team_1.replace('(жен)', '')
            team_1 = team_1.replace('(ж)', '')
            team_1 = team_1.lstrip()
            team_1 = team_1.rstrip()

            team_2 = str(response["O2"]).replace('(жeн)', '')
            team_2 = team_2.replace('(жен)', '')
            team_2 = team_2.replace('(ж)', '')
            team_2 = team_2.lstrip()
            team_2 = team_2.rstrip()

            event_name = f'{team_1} — {team_2}'

            if response['S'] <= time.time():
                return

            if event_name in self.line_events:
                # print(f'{event_name} already exist')
                ...
            else:
                self.line_events[event_name] = {
                    'id': int(event_id),
                    'start_time': response['S'],
                    'sport': response["SN"],
                    'league': response["L"],
                    'coefficients': self.get_coefficients(response)
                }
        except Exception as e:
            ...


    def get_coefficients(self, data):
        coefficients = {}
        mapping = {
            1: 'WRT_1',
            3: 'WRT_2',
            401: 'WM1',
            402: 'WM2',
            9: 'TLT',
            10: 'TMT',
        }
        for factor in data['GE']:
            for i in factor['E']:
                for j in i:
                    if j['T'] in mapping.keys():
                        if j['T'] == 9 or j['T'] == 10:
                            coefficients[f'{mapping[j["T"]]}_{j["P"]}'] = j['C']
                        else:
                            coefficients[mapping[j['T']]] = j['C']

        return coefficients