import urllib.request
import orjson
import sys
import lichess.api
from lichess.format import SINGLE_PGN
import json
import os
import datetime
import re

TOKEN = os.environ['TOKEN']

def types():
    return [
        'bullet',
        'blitz',
        'rapid',
        'classical',
        'correspondence',
        'chess960',
        'antichess',
        'atomic',
        'crazyhouse',
        'horde',
        'kingOfTheHill',
        'racingKings',
        'threeCheck'
    ]

def get_file_name(type):
    return type + '.md'

def get_all_bots_ratings():
    all_bots_ratings = []
    with open('available_bots.txt', 'r') as f:
        available_bots = [player.strip() for player in f.readlines()]

    batch_size = 100
    num_batches = (len(available_bots) + batch_size - 1) // batch_size

    for i in range(num_batches):
        batch_start = i * batch_size
        batch_end = (i + 1) * batch_size
        batch_usernames = available_bots[batch_start:batch_end]

        users_list = lichess.api.users_by_ids(batch_usernames)

        for user in users_list:
            all_bots_ratings.append({
                'title': user.get('title'),
                'username': user.get('username'),
                'id': user.get('id'),
                'perfs': user.get('perfs', {}),
                'seenAt': user.get('seenAt'),
                'tosViolation': user.get('tosViolation'),
                'disabled': user.get('disabled')
            })

    with open('bot_leaderboard.json', 'w') as f:
        json.dump(all_bots_ratings, f)
    print("Updated bot_leaderboard.json file.")

def get_bots_leaderboard(type):

    file_path = os.path.join(os.path.dirname(__file__), 'bot_leaderboard.json')
    with open(file_path, 'r') as f:
        bots_ratings = json.load(f)

    user_arr = []
    count = 1

    for d in bots_ratings:
        perfs = d['perfs'].get(type)
        if perfs is not None:
            result = [d['username'], perfs.get('rating')]
            print(f'{result[0]}: {result[1]} in {type}.')
            d['seenAt'] = datetime.datetime.utcfromtimestamp(d['seenAt'] / 100)
            if d.get('tosViolation', False) == True:
                print("Violated ToS")
            elif d.get('disabled', False) == True:
                print("Account Closed")               
            elif perfs.get('games', 0) > 0:
                user_arr.append(result)
            else:
                print(f" @{d['username']}: No {type} rating available")
        else:
            print(f"{d['title']} @{d['username']}: No {type} rating available")
    resulting_arr = sorted(user_arr, key=lambda x: x[1], reverse=True)
    with open(get_file_name(type), 'w') as f:
        print("Rank|Bot|Rating", file=f)
        print("---|---|---", file=f)
        for j in resulting_arr:
            print(f"#{str(count)}|{j[0]}|{str(j[1])}", file=f)
            count += 1

    print(f"Finished generating leaderboard for {type}")

if __name__ == "__main__":
    try:
        get_all_bots_ratings()
        for i in types():
            get_bots_leaderboard(i)
    except KeyboardInterrupt:
        sys.exit()