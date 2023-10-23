import aiohttp
from config import available_sports

class Fonbet:
    def __init__(self):
        self.host = 'https://www.fon.bet'
        self.sports = ['Хоккей', 'Футбол', 'Баскетбол', 'Теннис', 'Волейбол']
        self.leagues = {}
        self.line = {}

    async def get_line_list_base(self):
        url = 'https://line02w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                response = await request.json()

                self.parse_leagues(response['sports'])

                for event in response['events']:
                    if event['level'] == 1:
                        try:
                            self.line[f'{event["team1"]} — {event["team2"]}'] = self.parse_event(event)
                        except Exception:
                            ...

    def parse_leagues(self, data):
        sport_mapping = {'Хоккей': 'hockey', 'Футбол': 'football', 'Баскетбол': 'basketball', 'Теннис': 'tennis', 'Волейбол': 'volleyball'}
        sports = {}
        for row in data:
            if 'parentId' not in row.keys() and row['name'] in available_sports:
                sports[row['id']] = {
                    'name_ru': row['name'],
                    'name_en': sport_mapping[row['name']]
                }
            elif 'parentId' in row.keys():
                if row['parentId'] in sports.keys():
                    self.leagues[row['id']] = {
                        'name': row['name'],
                        'sport_id': row['parentId'],
                        'sport_name_ru': sports[row['parentId']]['name_ru'],
                        'sport_name_en': sports[row['parentId']]['name_en']
                    }


    def parse_event(self, event):
        sport_sub_url = self.leagues[event['sportId']]['sport_name_en']
        return {
            'id': event['id'],
            'url': f'{self.host}/sports/{sport_sub_url}/{event["sportId"]}/{event["id"]}',
            'start_time': event['startTime'],
        }




