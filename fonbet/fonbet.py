import json
import time

import requests as requests

available_sports = ['Хоккей', 'Футбол', 'Баскетбол', 'Теннис', 'Волейбол']

class Fonbet:
    def __init__(self):
        self.line_events = {}

    def run(self):
        self.get_line_events()
        print(f'Fonbet events: {len(self.line_events)}')
        with open('fonbet_result.json', 'w', encoding='utf-8') as f:
            json.dump(self.line_events, f, ensure_ascii=False, indent=4)

    def get_line_events(self):
        url = 'https://line02w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600'
        response = requests.get(url).json()

        for event in response['events']:

            if event['level'] == 1:
                try:
                    event_id = int(event['id'])
                    start_time = event['startTime']

                    team_1 = str(event["team1"]).replace('(жeн)', '')
                    team_1 = team_1.replace('(ж)', '')
                    team_1 = team_1.lstrip()
                    team_1 = team_1.rstrip()

                    team_2 = str(event["team2"]).replace('(жeн)', '')
                    team_2 = team_2.replace('(ж)', '')
                    team_2 = team_2.lstrip()
                    team_2 = team_2.rstrip()

                    event_name = f'{team_1} — {team_2}'


                    if start_time <= time.time():
                        continue

                    if event_name in self.line_events.keys():
                        # print(f'{event_name} already exist')
                        continue
                    else:
                        self.line_events[event_name] = {
                            'id': event_id,
                            'start_time': start_time,
                        }
                except Exception as e:
                    ...

        for event_name, event_data in self.line_events.items():
            event_data['coefficients'] = self.get_coefficients(event_data['id'])


    def get_coefficients(self, event_id):
        tmt = [930, 1696, 1727, 1730, 1733, 1736, 1739, 1793, 1796, 1799, 1802, 1848]
        tlt = [931, 1697, 1728, 1731, 1734, 1737, 1791, 1794, 1797, 1800, 1803, 1849]
        url = f'https://line32w.bk6bba-resources.com/events/event?lang=ru&eventId={event_id}&scopeMarket=1600&version=0'
        response = requests.get(url).json()
        if 'customFactors' not in response.keys():
            return {}
        else:
            if len(response['customFactors']) == 0:
                return {}

        coefficients = {}
        for factor in response['customFactors'][0]['factors']:
            if factor['f'] in tlt:
                coefficients[f'TLT_{factor["pt"]}'] = factor['v']
            elif factor['f'] in tmt:
                coefficients[f'TMT_{factor["pt"]}'] = factor['v']
            elif factor['f'] == 921:
                coefficients['WRT_1'] = factor['v']
            elif factor['f'] == 923:
                coefficients['WRT_2'] = factor['v']
            elif factor['f'] == 7035:
                coefficients['WM_1'] = factor['v']
            elif factor['f'] == 7036:
                coefficients['WM_2'] = factor['v']

        return coefficients



        #     sport = event['skName']
        #     if sport not in available_sports:
        #         continue
        #
        #     if sport not in self.line_events:
        #         self.line_events[sport] = {}
        #
        #     league = event['competitionName']
        #     if league not in self.line_events[sport]:
        #         self.line_events[sport][league] = []
        #
        #     self.line_events[sport][league].append(
        #         {
        #             'id': int(event['id']),
        #             'start_time': event['startTimeTimestamp'],
        #             'event_name': event['eventName'],
        #         }
        #     )
        #
        # for sport, event in self.line_events.items():
        #     print(sport, event)