from random import shuffle
from os import system, name


class BlackJack:
    """
    BlackJack game
    """

    # Class attributes
    dealer = []
    player = []
    initial_deal = True

    def __init__(self, name, bank):
        self.name = name
        self.bank = bank

    def __str__(self):
        return "BlackJack Game\n\n\nThe Rules:\n\nby going over 21 you bust your hand and loose\n"\
                "By sticking on a hand lower in value to the dealers hand you loose\n"\
                "if the dealer busts their hand you win \n"\
                "if you get 21 in your have you win\n\n"

    @staticmethod
    def build_deck():
        """
        Build deck of cards in a random order
        :return: list
        """
        deck = []

        # Build deck
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:

            for index, card in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']):
                if card in ['J', 'Q', 'K']:
                    deck.append([suit, card, 10, True])
                elif card in ['A']:
                    deck.append([suit, card, 11, True])
                else:
                    deck.append([suit, card, (index + 2), True])

        # Shuffle deck
        shuffle(deck)

        return deck

    def play_game(self):
        """
        Deals cards to one player and the dealer
        :return: tuple
        """
        deal_sqe = 2
        counter = 0
        shuffled_deck = self.build_deck()
        bet = 0
        kill = True

        # Set bet value
        while True and kill:
            try:
                if self.bank > 0:
                    if bet <= 0:
                        bet = float(input('How much would you like to bet? '))

                        # if bet exceeds the balance, ask to change bet value
                        while True:
                            if bet > self.bank:
                                bet = float(input(f'Please enter a lower value! Your bet value exceeds your balance of {self.bank}\n\nHow much would you like to bet? '))
                                continue
                            else:
                                break

                        continue
                    else:
                        break
                else:
                    # Add more if balance is spent
                    print(f"{self.name} you are out of funds, please add more to continue playing")
                    self.bank = int(input(f"{self.name} how much funds would you like to add? "))

                    if self.bank > 0:
                        continue
                    else:
                        print('Game has just been killed, restart script if you want another game')
                        kill = False

            except ValueError:
                print("Invalid Input:  please only enter bet value as a number")
                continue

        # Start the initial deal
        while self.initial_deal and kill:
            counter += 1
            if deal_sqe == 2:
                self.player.append(shuffled_deck.pop(0))
                deal_sqe = 1
            else:
                if counter == 4:
                    popped_card = shuffled_deck.pop()
                    popped_card[3] = False
                    self.dealer.append(popped_card)
                else:
                    self.dealer.append(shuffled_deck.pop(0))
                deal_sqe = 2

            if counter >= 4:
                self.initial_deal = False

        # Print initial hand to console
        if kill:
            self.print_cards((self.player, self.dealer))

        # Start second phase of dealing
        if not self.initial_deal and len(self.player) and kill:
            hit_or_stick = ''
            while True:

                if deal_sqe == 2:
                    if self.check_if_bust(self.player):
                        for card in self.dealer:
                            card[3] = True
                        # Print hands to console
                        self.print_cards((self.player, self.dealer))
                        break

                    hit_or_stick = input(F'{self.name} do you want to HIT or STICK: ').upper()
                else:
                    if len(self.dealer) == 2:
                        for card in self.dealer:
                            card[3] = True
                    # Print hands to console
                    self.print_cards((self.player, self.dealer))
                    if self.check_if_bust(self.dealer):
                        break

                    if len(self.dealer) >= 2:
                        if self.get_hand_value(self.dealer) <= self.get_hand_value(self.player):
                            self.dealer.append(shuffled_deck.pop(0))
                            continue
                        else:
                            break

                # logic for players move
                if deal_sqe == 2:
                    if hit_or_stick == 'HIT':
                        self.player.append(shuffled_deck.pop(0))
                        # Print hands to console
                        self.print_cards((self.player, self.dealer))

                        continue
                    elif hit_or_stick == 'STICK':
                        deal_sqe = 1
                        continue
                    else:
                        print('I did\'t understand your choice, please tell me again')
                        continue

            print(self.bet(bet))
            self.replay()

        return self.player, self.dealer

    def bet(self, bet):
        """
        Calculate bet and add or deducted as required
        :param bet: float
        :return: float
        """

        while True:
            if bet > 0:

                player = self.get_hand_value(self.player)
                dealer = self.get_hand_value(self.dealer)

                if self.check_for_player_winner():
                    self.bank += bet
                    print(f"You won £{bet}\nYour score is {player}\nDealers score is {dealer}")
                else:
                    self.bank -= bet
                    print(f"You lost £{bet}\nYour score is {player}\nDealers score is {dealer}")
                break
            else:
                try:
                    bet = int(input('How much do you want to bet? '))
                    continue
                except ValueError:
                    print('Invalid Value: you need to enter a number please')
                    continue

        return self.bank

    def print_cards(self, hands):
        """
        Print out player's hand
        :param hands: tuple of list
        :return: none
        """
        show_hand = ''
        player, dealer = hands

        self.clear()

        show_hand += "\n\n{}'s hand: ".format(self.name)
        for p_card in player:
            show_hand += "{} {}\t".format(p_card[1], p_card[0])

        show_hand += "\nDealers hand: "

        for d_card in dealer:
            if d_card[3]:
                show_hand += "{} {}\t".format(d_card[1], d_card[0])
            else:
                show_hand += "Card down"

        show_hand += '\n\n'

        print(show_hand)

    def check_if_bust(self, hand):
        """
        Check if hand is bust
        :param self:
        :param hand:
        :return: boolean
        """

        return self.get_hand_value(hand) > 21

    @staticmethod
    def get_hand_value(hand):
        """
        Calculate hand's total value taking into account reduction when Ace is present and total goes over 21
        :param hand: list
        :return: int
        """

        gather_total = 0
        aces = 0
        for val in hand:
            if val[2] == 11:
                aces += 1

            gather_total += val[2]

        while gather_total > 21 and aces:
                gather_total -= 10
                aces -= 1

        return gather_total

    def check_for_player_winner(self):
        """
        Check to see if player won
        :return:
        """

        if self.check_if_bust(self.player):
            return False
        elif self.get_hand_value(self.player) > self.get_hand_value(self.dealer):
            return True
        elif self.check_if_bust(self.dealer):
            return True
        else:
            return False

    def replay(self):
        """
        Replay is a way to get the player the option to play another game
        :return: none
        """
        while True:
            is_replay = input(f"{self.name} would you like another game? (YES or NO)").upper()

            if is_replay == 'YES':
                self.reset()
                self.play_game()
                break
            elif is_replay == 'NO':
                self.reset()
                print(f"Hey {self.name} hope you had fun and look forward to seeing you play again")
                break
            else:
                print('Invalid input, please answer correctly: ')
                continue

    def reset(self):
        self.player = []
        self.dealer = []
        self.initial_deal = True

    @staticmethod
    def clear():
        if name == 'posix':
            _ = system('clear')
        else:
            _ = system('cls')


newGame = BlackJack('Chris', 500)

print(str(newGame))

newGame.play_game()
