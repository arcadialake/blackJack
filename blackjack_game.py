import random
import time

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


# Building the cards

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+" of "+self.suit


# Building the deck

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return "\n".join(card.rank+" of "+card.suit for card in self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet():

    while True:
        try:
            player_chips.bet = int(input("You look the dealer in the eye and bet: \n"))

        except ValueError:
            print("We bet in numbers at this casino, man! \n ")

        else:
            if player_chips.bet > player_chips.total:
                print(f"You can't bet more than you have dude, lower your bet. You currently have {player_chips.total} chips on the table")
                continue

            else:
                print("Like a boss!!")
                return player_chips.bet


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):

    while True:
        choice = str(input("hit or stand? Enter 'h' or 's' "))
        if choice[0].lower() == "h":
            hit(deck, hand)
            show_some(player_hand, dealer_hand)
            if player_hand.value < 21:
                continue
        elif choice[0].lower() == "s":
            print("\n"+"You stand, Dealer's turn \n")
            return choice

        else:
            print("Dude, enter hit or stand only!")
            continue
        break


def show_some(player, dealer):
    print("DEALER'S HAND: ")
    print(dealer.cards[0])
    print("<Second card hidden>")

    if len(dealer.cards) > 2:
        print(*dealer.cards[2::], sep="\n")

    print("\n")
    print("YOUR HAND: ")
    for card in player.cards:
        print(card)
    print(f"Your hand has a value of {player.value}. \n")


def show_all(player, dealer):
    print("DEALER'S HAND: ")
    for card in dealer.cards:
        print(card)
    print(dealer.value)
    print("\n")
    print("YOUR HAND: ")
    for card in player.cards:
        print(card)
    print(player.value)


def player_busts(player, dealer, chips):
    print("YOU BUST! DEALER WINS!!")
    print("\n")
    chips.lose_bet()
    print("\n")
    print(f"You have {chips.total} chips remaining ")


def player_wins(player, dealer, chips):
    show_all(player_hand, dealer_hand)
    print("YOU WIN!!")
    chips.win_bet()
    print("\n")
    print(f"You have {chips.total} chips remaining ")


def dealer_busts(player, dealer, chips):
    print("DEALER BUSTS! YOU WIN!! ")
    chips.win_bet()
    print(f"You have {chips.total} chips remaining ")


def dealer_wins(player, dealer, chips):
    print("DEALER WINS!! ")
    print("\n")
    show_all(player_hand, dealer_hand)
    chips.lose_bet()
    print('\n')
    print(f"You have {chips.total} chips remaining")


def push(player, dealer, chips):
    print("You and the dealer tie, PUSH!! ")


def replay():
    ask = input("Would you like to play again? Y/N?")
    if ask.upper() == 'Y':
        return True
    else:
        print("Thank you for playing")
        return False

print("You have stepped into a casino and sat down at a Blackjack table. You give the dealer two thumbs up and a stupid smile. It's on...\n")
time.sleep(6)
print("The dealer shuffles the cards and deals, you raise an eyebrow, letting him know that you like to live dangerously. \n")
time.sleep(5)
player_chips = Chips()

while True:

    the_deck = Deck()
    the_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(the_deck.deal())
    dealer_hand.add_card(the_deck.deal())
    player_hand.add_card(the_deck.deal())
    dealer_hand.add_card(the_deck.deal())
    player_hand.adjust_for_ace()
    dealer_hand.adjust_for_ace()
    show_some(player_hand, dealer_hand)

    print(f"You have {player_chips.total} chips on the table. \n")
    time.sleep(3)

    take_bet()
    print("\n")

    while playing:

        hit_or_stand(the_deck, player_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            playing = False
            break

        while dealer_hand.value < 17:
            time.sleep(3)
            hit(the_deck, dealer_hand)
            print("Dealer hits \n")
            show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value and dealer_hand.value == 21:
            push(player_hand, dealer_hand, player_chips)

        break

    if not replay():
        playing = False
        break

    else:
        if player_chips.total == 0:
            print('You are out of chips!')
            more_chips = input('Would you like another 1000? Y/N? ')
            if more_chips.lower() == 'y':
                player_chips = Chips()
            else:
                print("You can't play without money, BYE!")
                break
        playing = True
        continue
