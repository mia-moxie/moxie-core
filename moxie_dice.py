import requests
import re
import os
import json

api_key = os.getenv("MOXIE_RANDOM_ORG_KEY")

def get_random_numbers(min_val, max_val, num, api_key):
    url = "https://www.random.org/integers/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    params = {
        "num": num,
        "min": min_val,
        "max": max_val,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new"
    }
    response = requests.get(url, params=params, headers=headers)
    return list(map(int, response.text.strip().split('\n')))

def roll_dice(dice_code):
    global api_key

    dice_pattern = re.compile(r'([+-]?\d*)d(\d+)|([+-]?\d+)')
    dice_matches = dice_pattern.findall(dice_code)
    results = []
    total = 0
    for dice_match in dice_matches:
        if dice_match[0]:  # This is a dice roll
            num_dice = int(dice_match[0]) if dice_match[0] not in ['-', '+'] else 1
            num_sides = int(dice_match[1])
            roll_results = get_random_numbers(1, num_sides, abs(num_dice), api_key)
            if num_dice < 0:
                roll_results = [-i for i in roll_results]
            results.extend([f"1d{num_sides} -> {roll}" for roll in roll_results])
            total += sum(roll_results)
        else:  # This is a static bonus/penalty
            bonus = int(dice_match[2])
            total += bonus
    return ' '.join(results) + f" TOTAL: {total}"

def roll_dice_from_json(json_string):
    dice_list = json.loads(json_string)

    if len(dice_list) == 0:
        return None

    results = []
    for dice in dice_list:
        dice_code = dice["dice_code"]
        comment = dice.get("comment", "")
        roll_results = roll_dice(dice_code)
        results.append({
            "dice_code": dice_code,
            "comment": comment,
            "roll_results": roll_results
        })
    return str(results)

if __name__ == "__main__":
    json_string = """
    [
        { "dice_code": "2d10+3", "comment": "Damage roll" },
        { "dice_code": "1d20+5", "comment": "Attack roll" }
    ]
    """
    print(str(roll_dice_from_json(json_string)))