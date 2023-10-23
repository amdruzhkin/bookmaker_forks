import asyncio
import time

import aiohttp
from config import available_sports


class Leon:
    def __init__(self):
        self.host = 'https://leon.ru'
        self.line = {}

    async def get_line(self):
        async with aiohttp.ClientSession() as session:
            leagues = await self.get_leagues(session)

            league_events_tasks = []
            for league_id in leagues:
                league_events_tasks.append(asyncio.ensure_future(self.get_league_events(session, league_id)))
            await asyncio.gather(*league_events_tasks)

        # for event_name, event_data in self.line.items():
        #     print(event_name, event_data)
        # print(len(self.line))

    async def get_leagues(self, session):
        url = 'https://leon.ru/api-2/betline/sports?ctag=ru-RU&flags=urlv2'
        async with session.get(url) as request:
            response = await request.json()
            leagues = []
            for sport in response:
                if sport['name'] in available_sports:
                    for region in sport['regions']:
                        for league in region['leagues']:
                            leagues.append(league['id'])
            return leagues

    async def get_league_events(self, session, league_id):
        url = f'https://leon.ru/api-2/betline/events/all?ctag=ru-RU&league_id={league_id}' \
              f'&hideClosed=true&flags=reg,urlv2,mm2,rrc,nodup'
        async with session.get(url) as request:
            response = await request.json()
            try:
                for event in response['events']:
                    start_time = event['kickoff']
                    if start_time <= time.time():
                        continue
                    # —
                    event_name = f'{event["competitors"][0]["name"]} — {event["competitors"][1]["name"]}'
                    self.line[event_name] = self.parse_event(event)

            except Exception:
                ...

    def parse_event(self, event):
        url = f'{self.host}/bets/' \
              f'{event["league"]["sport"]["url"]}/' \
              f'{event["league"]["region"]["url"]}/' \
              f'{event["league"]["url"]}/' \
              f'{event["id"]}-{event["url"]}'
        return {
            'id': event['id'],
            'url': url,
            'start_time': int(str(event['kickoff'])[:-3])
        }
