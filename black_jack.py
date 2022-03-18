from audioop import add
from calendar import c
from copy import copy
import random
import matplotlib.pyplot as plt
# GLOBAL VARIABLES values, suits, and ranks ARE USED THROUGHOUT THE CODE. THE PART STILL UNCLEAR
# IS HOW TO ASSIGN A ONE OR 11 TO ACE
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight': 8, 
    'Nine':9, 'Ten':10, 'Jack': 10, 'Queen': 10, 'King':10, 'Ace': (1, 11)}
suits = ('Hearts', 'Diamonds', 'Spades', "Clubs")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

# CARD CLASS IS CALLED TO CONSTRUCT THE CARDS. THE ATTRIBUTE value IS A FUNCTION OF ranks.
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

# PLAYERS CLASS INPUTS THE NUMBER OF PLAYERS. CURRENTLY DOES NOT RE
class Players:

    while True:
        try:
            number_of_players = 1
            break
        except ValueError:
            print("Please input integer only...")
            continue

    def __init__(self, player_id, buyin_amount):

        self.player_id: str = player_id
        self.buyin_amount:int = buyin_amount
        

    @classmethod
    def input_player_info(cls):
        return cls(
            input('Player ID (please enter One Two, Three etc...) '),
            input('Buy in amount in dollars: '))
    
    def keep_playing(self):
        player_decide = input(f"Player {key.upper()}, keep playing? (y or n): ")
        return player_decide
    
    def new_hand(self):
        self.new_card = new_deck.deal_one()
        return self.new_card
    
    def deal_hand(self):
        deal_cards=[]
        dealt_card = Players.new_hand(new_deck)
        deal_cards.append((dealt_card.suit, dealt_card.rank,dealt_card.value))
        return deal_cards

    def betting(self):
        return (input(f'Player {key.upper()}, place your bets. The minimum bet is ${minimum_bet}: '))

    def h_s_f(self):
        return(int(input(f"Player {key.upper()}, hit(1)/stay(2)/fold(3)?: ")))
    
    def check_winner(self):
        pass

    def __str__(self):
        return "Player " + self.player_id + " enters game with " + "$" + self.buyin_amount + "."

class Decks:
    
    #specify number of decks to play with
    while True:
        try:
            number_of_decks = 3
            break
        except ValueError:
            print("Please input integer only...")
            continue
    

    def __init__(self):
       
        self.all_cards = []
        for _ in range(Decks.number_of_decks):
            for suit in suits:
                for rank in ranks:
                    # Create the Card Object
                    created_card = Card(suit,rank)
                    self.all_cards.append(created_card)
 #                   print(created_card)
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

    def insert_back(self):
        return self.all_cards.insert(0, Players.new_hand)

class DealerHand:
        
    def dealer_cards(self):
        reveal_card =Players.new_hand(new_deck)
        return reveal_card

    def play_next_hand(self):
        deal_cards=dealt_hand[key]
        if hit_stay_or_fold == 1:
            dealt_card = Players.new_hand(new_deck)
            deal_cards.append((dealt_card.suit, dealt_card.rank,dealt_card.value))
            return deal_cards
        elif hit_stay_or_fold == 2:
            deal_cards.append('stay')
            return deal_cards
        elif hit_stay_or_fold == 3:
            deal_cards.append('fold')
            return deal_cards
    

new_deck = Decks()
new_deck.shuffle()

# Input player name and buy in amount
players={'one':100}
#for _ in range(Players.number_of_players):
#    player_info = Players.input_player_info()
#    players[player_info.player_id] = int(player_info.buyin_amount)

# Players place minimum bets
minimum_bet = [5]
game_over = False

for min_bet in minimum_bet:
    rounds=0
    no_rounds = []
    dollars_per_round = []
    dealer_total=[]
    player_total = []
    while game_over == False:
        make_bet = {}
        for key in players:
            make_bet[key] = min_bet
            players[key]= players[key] - make_bet[key]
        print(players)

        # Deal the first card for dealer
        dealer_hand={}
        dealer_card_no=1
        card_no = 'card_no_' + str(dealer_card_no)
        dealer_hand[card_no]=DealerHand.dealer_cards(dealer_hand)
        new_deck.insert_back()
        dealer_first_card = dealer_hand[card_no]
        sum_of_cards = 0
        there_was_ace = False
        if dealer_first_card.rank == 'Ace':
                ace_tuple = dealer_first_card.value
                sum_of_cards=int(ace_tuple[1])
                there_was_ace = True
        else:
                sum_of_cards = int(dealer_first_card.value)

        #card_no = 'card_no_' + '2'
        #dealer_hand[card_no]=DealerHand.dealer_cards(dealer_hand)
        #dealer_next_card = dealer_hand[card_no]

        # Deal first two hands for players
        dealt_hand={}
        set_of_cards=[]
        player_card_no=1
        for key in players:
            card_no = 'card_no_' + str(player_card_no)
            player_card_sum=0
            add_cards = {}
            hit_stay_or_fold=1
            if player_card_sum >= 21:
                hit_stay_or_fold = 2
            while hit_stay_or_fold == 1:
                dealt_hand[key] = Players.deal_hand(key)
                set_of_hands=dealt_hand[key]
                temp_va = set_of_hands[0][1]
                if set_of_hands[0][1] == 'Ace':
                    if player_card_sum <= 10:
                        ace_1_or_11 = 11
                    else:
                        ace_1_or_11 = 1
                    player_card_sum = player_card_sum + int(ace_1_or_11)
                    temp_list = list(set_of_hands[0])
                    temp_list[2]= ace_1_or_11
                    set_of_hands[0]=temp_list
                else:
                    player_card_sum = player_card_sum + int(set_of_hands[0][2])
                add_cards[key]=player_card_sum
                set_of_cards.append(tuple(set_of_hands[0]))
                if player_card_sum >= 21:
                    hit_stay_or_fold = 2     
                print(add_cards)
            

        #    player_card_sum=0
        print(add_cards)
        dealer_sum ={}
    # Dealer turns dealer's next cards
        while sum_of_cards <= 16:
            dealer_card_no+=1
            card_no = 'card_no_' + str(dealer_card_no)
            dealer_hand[card_no]=DealerHand.dealer_cards(dealer_hand)
            dealer_next_card = dealer_hand[card_no]
            if dealer_next_card.rank == 'Ace' and there_was_ace == True:
                ace_tuple = dealer_next_card.value
                sum_of_cards=sum_of_cards + int(ace_tuple[0])
            elif dealer_next_card.rank == 'Ace' and there_was_ace == False:
                if sum_of_cards <=10:
                    ace_tuple = dealer_next_card.value
                    sum_of_cards=sum_of_cards + int(ace_tuple[1])
                elif sum_of_cards > 10:
                    ace_tuple = dealer_next_card.value
                    sum_of_cards=sum_of_cards + int(ace_tuple[0])
            else:
                sum_of_cards = sum_of_cards + int(dealer_next_card.value)
            dealer_sum['dealer_hand']=sum_of_cards
        
        for key, value in dealer_hand.items():
            print(key, value)

        if sum_of_cards > 21:
            for key, value in add_cards.items():
                if value <= 21:
                    players[key]=players[key]+make_bet[key]*2
        elif sum_of_cards == 21:
            for key, value in add_cards.items():
                if value == 21:
                    players[key] = players[key]+make_bet[key]
        elif sum_of_cards < 21:
            for key, value in add_cards.items():
                if value <= 21 and value > sum_of_cards:
                    players[key]=players[key]+make_bet[key]*2
                elif value <= 21 and value == sum_of_cards:
                    players[key]=players[key]+make_bet[key]


        print(dealer_sum)
        print(add_cards)
        print(players)               
        
#       for key in players.copy():
#          decide = 'y'
#           if decide == 'n':
#              players.pop(key)
        rounds+=1
        no_rounds.append(rounds)
        dollars_per_round.append(players[key])
        player_total.append(player_card_sum)
        dealer_total.append(sum_of_cards)
        if players[key] < 5:
            game_over=True
        print(no_rounds)
print(no_rounds, dollars_per_round, dealer_total, player_total)
plt.plot(no_rounds, dollars_per_round)