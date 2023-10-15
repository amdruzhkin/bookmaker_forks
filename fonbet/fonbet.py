import requests as requests


class Fonbet:
    def __init__(self):
        self.line_events = {}

    def get_line_events(self):
        url = 'https://line51w.bk6bba-resources.com/line/desktop/topEvents3?place=line&sysId=1&lang=ru&salt=1hv7zi2eb8xlnqcl5zb&supertop=4&scopeMarket=1600'
        response = requests.get(url).json()

        for event in response['events']:
            sport = event['skName']
            if sport not in self.line_events:
                self.line_events[sport] = {}

            league = event['competitionName']
            if league not in self.line_events[sport]:
                self.line_events[sport][league] = []

            self.line_events[sport][league].append(
                {
                    'id': event['id'],
                    'start_time': event['startTimeTimestamp'],
                    'event_name': event['eventName'],
                }
            )

        for sport, event in self.line_events.items():
            print(sport, event)



if __name__ == '__main__':
    fonbet = Fonbet()
    fonbet.get_line_events()