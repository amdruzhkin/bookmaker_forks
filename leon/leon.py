import json
import time

import requests

available_sports = ['Хоккей', 'Футбол', 'Баскетбол', 'Теннис', 'Волейбол']

class Leon:
    def __init__(self):
        self.line_events = {}

    def run(self):
        self.get_line_events()
        print(f'Leon events: {len(self.line_events)}')
        with open('../leon_result.json', 'w', encoding='utf-8') as f:
            json.dump(self.line_events, f, ensure_ascii=False, indent=4)

    def get_line_events(self):
        leagues = self.get_leagues()
        for league_id, league_data in leagues.items():
            self.get_events(league_id)

        for event_name, event_data in self.line_events.items():
            # print(event_name, event_data)
            event_data['coefficients'] = self.get_coefficients(event_data['id'])


    def get_coefficients(self, event_id):
        url = f'https://leon.ru/api-2/betline/event/all?ctag=ru-RU&eventId={event_id}&flags=reg,urlv2,mm2,rrc,nodup,smg,outv2'
        response = requests.get(url).json()

        coefficients = {}

        try:
            for factor in response['markets']:
                if factor['name'] == 'Победитель':
                    coefficients['WRT_1'] = factor['runners'][0]['price']
                    coefficients['WRT_2'] = factor['runners'][2]['price']
                elif factor['name'] == 'Тотал':
                    coefficients[f'TLT_{factor["handicap"]}'] = factor['runners'][0]['price']
                    coefficients[f'TMT_{factor["handicap"]}'] = factor['runners'][1]['price']

            return coefficients
        except Exception as e:
            return coefficients

    def get_events(self, league_id):
        url = f'https://leon.ru/api-2/betline/events/all?ctag=ru-RU&league_id={league_id}&hideClosed=true&flags=reg,urlv2,mm2,rrc,nodup'
        response = requests.get(url).json()
        for event in response['events']:
            start_time = event['kickoff']
            event_name = event['name']
            event_id = event['id']
            if start_time <= time.time():
                continue

            self.line_events[event_name] = {
                'id': event_id,
                'start_time': start_time,
                'league_id': league_id
            }


    def get_leagues(self):
        url = 'https://leon.ru/api-2/betline/sports?ctag=ru-RU&flags=urlv2'
        response = requests.get(url).json()

        leagues = {}
        for sport in response:
            if sport['name'] in available_sports:
                for region in sport['regions']:
                    for league in region['leagues']:
                        leagues[league['id']] = {
                            'sport': sport['name'],
                            'sport_id': sport['id'],
                            'region': region['name'],
                            'region_id': region['id'],
                        }
        return leagues



if __name__ == '__main__':
    leon = Leon()
    leon.run()
