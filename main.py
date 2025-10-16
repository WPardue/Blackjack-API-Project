import requests
from fastapi import FastAPI
from deck import deck
from draw import draw
from hand import hand

def get_hand_value(cards):
    ace_count = 0
    while ("ACE" in cards):
        cards.remove("ACE")
        ace_count += 1
    if(ace_count > 0):
        for i in range(ace_count):
            cards.append("ACE")

    value = 0
    for i in cards:
        try:
            value += int(i)
        except:
            if(i != "ACE"):
                value += 10
            else:
                if(value + 11 > 21):
                    value += 1
                else:
                    value += 11
    return value

BASE_URL = "https://deckofcardsapi.com/"

another_round = True
while(another_round):
    not_validated = True
    while(not_validated):
        try:
            player_count = int(input("Enter the number of players. (Between 2 and 5): "))
            if (player_count < 2 or player_count > 5):
                raise
            not_validated = False
        except:
            print("Enter a number between 2 and 5")

    deck_results = requests.get(BASE_URL + "/api/deck/new/shuffle/?deck_count=1").json()
    play_deck = deck(**deck_results)

    deck_id = play_deck.deck_id

    for k in range(2): #Deals each player 2 cards
        for i in range(player_count):

            draw_results = requests.get(BASE_URL + "/api/deck/" + deck_id + "/draw/?count=1").json()
            drawn_cards = draw(**draw_results)

            card_drawn_code = drawn_cards.cards[0].code

            pile_name = f"player_{i+1}"
            add_to_hand = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/" + pile_name + "/add/?cards=" + card_drawn_code).json()

    stand = False
    while(stand == False):
        hand_result = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/player_1/list/").json()
        p1_hand = hand(**hand_result)

        hand_string = ""
        for i in range(len(p1_hand.piles["player_1"].cards)):
            hand_string += f'{p1_hand.piles["player_1"].cards[i].value} of {p1_hand.piles["player_1"].cards[i].suit}, '

        print(f"Your cards are: {hand_string}")
        not_validated = True
        while(not_validated):
            choice = input("Hit (h) or Stand (s): ")
            if(choice.lower() == "h" or choice.lower() == "s" ):
                not_validated = False
            else:
                print("Enter h to hit or s to stand.")
            
        if(choice == "h"):
            draw_results = requests.get(BASE_URL + "/api/deck/" + deck_id + "/draw/?count=1").json()
            drawn_cards = draw(**draw_results)

            card_drawn_code = drawn_cards.cards[0].code

            pile_name = "player_1"
            add_to_hand = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/" + pile_name + "/add/?cards=" + card_drawn_code).json()
        if(choice == "s"):
            stand = True

    for i in range(player_count-1):
        stand = False
        while(stand == False):
            hand_result = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/" + f"player_{i+2}" +"/list/").json()
            current_hand = hand(**hand_result)

            values_list = []
            for k in range(len(current_hand.piles[f"player_{i+2}"].cards)):
                values_list.append(current_hand.piles[f"player_{i+2}"].cards[k].value)
            
            hand_value = get_hand_value(values_list)
            if(hand_value > 17):
                stand = True
            else:
                draw_results = requests.get(BASE_URL + "/api/deck/" + deck_id + "/draw/?count=1").json()
                drawn_cards = draw(**draw_results)

                card_drawn_code = drawn_cards.cards[0].code

                pile_name = f"player_{i+2}"
                add_to_hand = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/" + pile_name + "/add/?cards=" + card_drawn_code).json()

    winning_player = ""
    winning_score = 0
    for i in range(player_count):
        final_hand_result = requests.get(BASE_URL + "/api/deck/"+ deck_id + "/pile/" + f"player_{i+1}" +"/list/").json()
        final_hands = hand(**final_hand_result)
        final_hand_string = ""
        final_hand_list = []
        for k in range(len(final_hands.piles[f"player_{i+1}"].cards)):
            final_hand_string += f'{final_hands.piles[f"player_{i+1}"].cards[k].code}, '
            final_hand_list.append(final_hands.piles[f"player_{i+1}"].cards[k].value)

        if(winning_player == "" and get_hand_value(final_hand_list) < 22):
            winning_player = f"player {i+1}"
            winning_score = get_hand_value(final_hand_list)
        elif(get_hand_value(final_hand_list) > winning_score and get_hand_value(final_hand_list) < 22):
            winning_player = f"player {i+1}"
            winning_score = get_hand_value(final_hand_list)
        elif(get_hand_value(final_hand_list) == winning_score):
            winning_player = f"{winning_player} and {i+1}"
        elif(winning_player == ""):
            winning_player = "Draw"

        print(f"player {i+1}: {final_hand_string} {get_hand_value(final_hand_list)}")
    print(f"Winner: {winning_player}")

    not_validated = True
    while(not_validated):
        choice = input("Would you like to play another round? (y/n): ")
        if(choice.lower() == "n"):
            not_validated = False
            another_round = False
        elif(choice.lower() == "y"):
            not_validated = False
        else:
            print("Enter y for Yes or n for No")

    return_cards = requests.get(BASE_URL + "/api/deck/"+ deck_id +"/return/").json()
    shuffle_cards = requests.get(BASE_URL + "/api/deck/"+ deck_id +"/shuffle/").json()