import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
# Dictionary of values per rank
values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":11}

# Variable to control the main while loop
playing = True


class Card():
    """
    General class with suit and rank attributes
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck():
    """
    Class to create the deck using the Card class
    """
    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                # Create the card object
                create_card = Card(suit, rank)
                # Add the card to the deck
                self.deck.append(create_card)

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return f"The deck has {deck_comp}"
    
    def shuffle(self):
        """
        Method to shuffle the deck
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        Returns a single card
        """
        return self.deck.pop(0)


class Hand:
    """
    Class to set the total of the Hand based on the cards
    """
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        """
        Add a card from Deck.deal to the hand
        and sums the value
        """
        self.cards.append(card)
        self.value += values[card.rank]

        # Track aces
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        """
        If the player gets busted and has an ace, the ace's value will be 1
        """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total=100):
        """
        Class to save the bets and check if the player has enough chips 
        to make the bet. Then increase the total if the player wins the 
        hand or decrease it if the player loses
        """
        self.total = total
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    """
    Asks for an integer that will be the player's bet
    """
    while True:
        try:
            chips.bet = int(input("How many chips do you want to bet?: "))
        except:
            print("You should enter a valid number")
        else:
            if chips.bet > 0: 
                if chips.bet > chips.total:
                    print(f"Sorry, you don't have enough chips. You have {chips.total}")
                else:
                    print("Your bet has been taken")
                    break
            else:
                print("The bet must be more than 0")


def hit(deck, hand):
    """
    Deal another card when the player asks for it or the Dealer's hand is less than 17
    """
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    """
    Check if the player wants to hit or stand in order to control de loop
    """
    global playing
    while True:
        choice = input("Hit or Stand? Enter H or S: ").upper()
        if choice[0] == "H":
            hit(deck, hand)
        elif choice[0] == "S":
            print("Player stands, dealer's turn")
            playing = False
        else:
            print("Sorry, I didn't understand. Please enter your choice again")
        break


def show_some(player, dealer):
    """
    Show only one of the dealer's cards and all the player's cards
    """
    print("\nDealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    """
    Show all the dealer's and player's card, calculate and display the value
    """
    print("\nDealer's Hand: ")
    for card in dealer.cards:
        print(card)
    print(f"Value of Dealer's hand is: {dealer.value}")
    
    print("\nPlayer's Hand: ")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")


def player_busts(player, dealer, chips):
    print("Bust player")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Bust dealer")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and player tie! Push!")


if __name__ == "__main__":
    print("*** Welcome to Blackjack!!! ***")
    # Set up the player's chips
    player_chips = Chips(200)

    print(f"You start with {player_chips.total} chips")

    game_on = True 
    while game_on:

        # Create and shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Prompt the player for their bet
        take_bet(player_chips)

        # Show cards, but keep one dealer card hidden
        show_some(player_hand, dealer_hand)

        while playing and player_hand.value < 21:
            # Prompt for player to hit or stand
            hit_or_stand(deck, player_hand)
            # Show cards, but keep one dealer card hidden
            show_some(player_hand, dealer_hand)
            # If player's hand exceeds 21, run player_busts() and break out of loop
        # If player hasn't busted, play dealer's hand until dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winnin scenarios
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
        # Inform player of their chips total
        print(f"\nPlayer total chips are at: {player_chips.total}")
        if player_chips.total == 0:
            print("Player runs out of chips")
            break
        # Ask to play again
        new_game = ""
        while new_game != "Y" and new_game != "N":
            new_game = input("Would you like to play another hand? (Y/N) ").upper()
            if new_game[0] == "Y":
                playing = True
            elif new_game[0] == "N":
                print("Thank you for playing!")
                game_on = False
        

