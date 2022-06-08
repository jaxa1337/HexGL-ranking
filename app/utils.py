import json

def save_new_nick(nick: str):
    status = check_nickname(nick)
    if status:
        with open("./data/used_nicknames.txt", "w") as file:
            file.write(nick)
            return True
    else:
        print("Nickname exist.")
        return False

def check_nickname(nick: str):
    with open("./data/used_nicknames.txt", "r") as file:
        nicknames = file.read().split("\n")
        print(nicknames)
        if nick in nicknames:
            return False
        else: 
            return True

def saved_user_score(nick: str, score: float):
    scores = check_score(nick, score)
    if scores:
        with open("./data/users_scores.json", 'w') as json_file:
            json.dump(scores, json_file, indent=4)
            print('Score saved!')
            return 1
    else:
        return 0

def check_score(nick: str, score: float):
    scores = {}
    with open("./data/users_scores.json") as json_file:
        scores = json.load(json_file)
        if nick in scores.keys():
            if scores[nick] < score:
                scores[nick] = score
                print(scores)
                return scores
            else:
                print('Score is lower than previous one.')
                return 0
        else:
            scores[nick] = score
            print(scores)
            return scores

def get_scores() -> dict():
    scores = {}
    with open("./data/users_scores.json") as json_file:
        scores = json.load(json_file)
        return scores

        

    
    