# Responses that will be randomly selected to add flavor to the game
import openai
import random

"""
openai.api_key = "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"

prompts = [
    "Player {} grabs the gun, eager to get it over with...",
    "Player {} slowly drags the gun towards themselves, dread strewn across their face...",
    "Player {} exhales then hesitates before grabbing the gun...",
    "Player {} hand trembles while reaching for the gun...",
    "Player {} has a facade of confidence as they bruskly grab the gun...",
    "Player {} wipes beads of sweat from their face before grabbing the gun...",
    "Player {} reaches with bloody fingers from ripping their cuticles for the gun..."
  ]

def generate_response(current_player, prompts):
  prompt = random.choice(prompts).format(current_player)
  response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=50
  )
  return response.choices[0].text
"""


def next_turn_responses(current_player):
    next_turn_responses_list = [
        f"Player {current_player} grabs the gun, eager to get it over with...",
        f"Player {current_player} slowly drags the gun towards themselves, dread strewn across their face...",
        f"Player {current_player} exhales then hesitates before grabbing the gun...",
        f"Player {current_player}'s hand trembles while reaching for the gun...",
        f"Player {current_player} has a facade of confidence as they bruskly grab the gun...",
        f"Player {current_player} wipes beads of sweat from their face before grabbing the gun...",
        f"Player {current_player} reaches with bloody fingers from ripping their cuticles for the gun..."
    ]

    return random.choice(next_turn_responses_list)


def alive_responses(current_player):
    alive_responses_list = [
        f"Player {current_player} let's out a sigh of relief",
        f"Player {current_player} yells in anger and fear",
        f"Player {current_player} whimpers to themselves quietly",
        f"Player {current_player} let's out a nervous laugh",
        f"Player {current_player} doesn't make a sound and softly places the gun down",
        f"Player {current_player} grunts in triumph",
    ]

    return random.choice(alive_responses_list)


def dead_responses(current_player):
    dead_responses_list = [
        f"Player {current_player}'s head falls weightlessly to the side...",
        f"Player {current_player} has a gaping hole in the side of their head...",
        f"Player {current_player}'s blood splatters on the wall behind them...",
        f"Player {current_player}'s eyes roll back into their head as their body goes limp...",
        f"Player {current_player}'s body slumps forward onto the table with the gun still in their hand",
    ]

    return random.choice(dead_responses_list)