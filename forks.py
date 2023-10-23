import asyncio
from difflib import SequenceMatcher

from fonbet import Fonbet
from leon import Leon


class Forks:
    def __init__(self):
        self.fonbet = Fonbet()
        self.leon = Leon()

    async def run(self):
        tasks = []
        tasks.append(asyncio.create_task(self.fonbet.get_line_list_base()))
        tasks.append(asyncio.create_task(self.leon.get_line()))
        await asyncio.gather(*tasks)

        matching = {}
        for leon_event_name, leon_event_data in self.leon.line.items():
            for fonbet_event_name, fonbet_event_data in self.fonbet.line.items():
                if SequenceMatcher(None, leon_event_name, fonbet_event_name).ratio() >= 0.65 and leon_event_data['start_time'] == fonbet_event_data['start_time']:
                    matching[leon_event_name] = {
                        'matching': SequenceMatcher(None, leon_event_name, fonbet_event_name).ratio(),
                        'fonbet_id': fonbet_event_data['id'],
                        'fonbet_url': fonbet_event_data['url'],
                        'fonbet_start_time': fonbet_event_data['start_time'],
                        'leon_id': leon_event_data['id'],
                        'leon_url': leon_event_data['url'],
                        'leon_start_time': leon_event_data['start_time'],
                    }
                    break

        for name, data in matching.items():
            print(name, data)

        print(len(matching))