import json
import math
import ast

def save_new_nick(nick: str):
    status = check_nickname(nick)
    if status:
        with open("app/data/used_nicknames.txt", "w") as file:
            file.write(nick)
            return True
    else:
        print("Nickname exist.")
        return False

def check_nickname(nick: str):
    with open("app/data/used_nicknames.txt", "r") as file:
        nicknames = file.read().split("\n")
        print(nicknames)
        if nick in nicknames:
            return False
        else: 
            return True

def saved_user_score(nick: str, score: float):
    scores = check_score(nick, score)
    if scores:
        with open("app/data/users_scores.json", 'w') as json_file:
            json.dump(scores, json_file, indent=4)
            return 1
    else:
        return 0

def check_score(nick: str, score: float):
    scores = {}
    with open("app/data/users_scores.json") as json_file:
        scores = json.load(json_file)
        if nick in scores.keys():
            if scores[nick] > score:
                scores[nick] = score
                return scores
            else:
                return 0
        else:
            scores[nick] = score
            return scores

def get_scores() -> dict():
    scores = {}
    with open("app/data/users_scores.json") as json_file:
        scores = json.load(json_file)
        return scores

def convert_to_time(num: int) -> str():
    ms = num % 1000
    s = math.floor((num / 1000) % 60)
    m = math.floor((num / 60000) % 60)
    result = ""
    if m < 10:
        result = "0" + str(m) + ":"
    else: 
        result = str(m) + ":"
    
    if s < 10:
        result += "0" + str(s) + ":"
    else:
        result += str(s) + ":"

    if ms < 10:
        result += "00" + str(ms)
    elif ms < 100:
        result += "0" + str(ms)
    else:
        result += str(ms)
    return result

def sort_scores() -> dict():
    scores = get_scores()
    scores = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1])}
    for key in scores:
        new_value = convert_to_time(scores[key])
        scores[key] = new_value
    with open("app/data/times.json", 'w') as json_file:
            json.dump(scores, json_file, indent=4)
            return 1
    return scores

def get_times_json() -> dict():
    scores = {}
    sort_scores()
    with open("app/data/times.json") as json_file:
        scores = json.load(json_file)
    return scores