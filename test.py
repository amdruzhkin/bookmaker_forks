import json
from difflib import SequenceMatcher
import time

import numpy as np

with open('fonbet_result.json', 'r', encoding='utf-8') as file:
    fonbet = json.loads(file.read())

# with open('onexbet_result.json', 'r', encoding='utf-8') as file:
#     onexbet = json.loads(file.read())

with open('leon_result.json', 'r', encoding='utf-8') as file:
    leon = json.loads(file.read())

def is_fork(a, b):
    p = 1 / a + 1 / b
    if p < 1:
        return True, p
    else:
        return False, 1

def search_forks(b1c, b2c):
    forks = {
        'fork_exist': False,
    }
    for factor, coef in b1c.items():
        if 'TLT' in factor:
            score = factor.split('_')[1]
            try:
                a = coef
                b = b2c[f'TMT_{score}']
                p = 1 / a + 1 / b
                if p < 1:
                    p = (1 - p) * 100
                    forks['fork_exist'] = True
                    forks[str(p)] = {
                        f'B1_TLT_{score}': a,
                        f'B2_TMT_{score}': b
                    }
            except Exception as e:
                ...

    for factor, coef in b2c.items():
        if 'TLT' in factor:
            score = factor.split('_')[1]
            try:
                a = coef
                b = b1c[f'TMT_{score}']
                p = 1 / a + 1 / b
                if p < 1:
                    p = (1 - p) * 100
                    forks['fork_exist'] = True
                    forks[str(p)] = {
                        f'B1_TMT_{score}': b,
                        f'B2_TLT_{score}': a
                    }
            except Exception as e:
                ...

    if forks['fork_exist'] is True:
        return forks
    else:
        return {}


for fb_event, fb_data in fonbet.items():
    for leon_event, leon_data in leon.items():
        if SequenceMatcher(None, leon_event, fb_event).ratio() >= 0.8:
            # print(SequenceMatcher(None, ob_event, fb_event).ratio(), ob_event, fb_event)
            forks = search_forks(leon_data['coefficients'], fb_data['coefficients'])
            if forks != {}:
                print(leon_event, fb_event, forks)
            break

