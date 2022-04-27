import sys
import random

#from blackjack import displayHands, getBet, getHandValue, getMove

"""
Player
Dealer
Card
Deck
"""
# Set up the constants:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
# (A list of chr codes is at https://inventwithpython.com/charactermap)
BACKSIDE = 'backside'

class Dealer():
    def __init__(self):
        self.dealerHand = [] 

class Player():
    def __init__(self, money=5000):
        self.money = money # далее ошибка type object 'Player' has no attribute 'money' 
        self.playerHand = [] 
        self.bet = 0
        
    def getBet(self):
        while True:
            print(f"Какую ставку вы хотите сделать? (1-{self.money} or QUIT)")
            self.bet = input('> ').upper().strip()

            if self.bet == 'QUIT':
                print("Спасибо за игру!")
                sys.exit()

            if not self.bet.isdecimal():
                print("Вы ввели что-то не то, товарищ. Мяу")
                continue

            self.bet = int(self.bet)
            if 1 <= self.bet <= self.money:
                # return self.bet
                break

    def getMove(self): 
        """Спрашиваем, какой ход хочет сделать игрок, и возвращаем 'H', если он
        хочет взять еще карту, 'S', если ему хватит, и 'D', если он удваивает."""
        while True:
            moves = ['(H)it', '(S)tand']

            if len(self.playerHand) == 2 and self.money > 0:
                moves.append('(D)ouble down')

            # Get the player's move:
            movePrompt = ', '.join(moves) + '> '
        
            move = input(movePrompt).upper() # x =  input("Введите что-то: ")

            if move in ('H', 'S'):
                return move  # Player has entered a valid move.
            if move == 'D' and '(D)ouble down' in moves:
                return move  # Player has entered a valid move.
            
        print('Введите корректное значение!')
        


class Card():
    @staticmethod
    def displayCards(cards):
        """Отрисовать карты на экране"""
        rows = ['', '', '', '', '',]
        BACKSIDE = 'backside'
        for i, card in enumerate(cards):
            rows[0] += ' ___  '
            if card == BACKSIDE:
                rows[1] += '|## | '
                rows[2] += '|###| '
                rows[3] += '|_##| '
            else:
                rank, suit = card # ('5', '@')
                rows[1] += '|{} | '.format(rank.ljust(2))
                rows[2] += '| {} | '.format(suit)
                rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

        for row in rows:
            print(row)

    @staticmethod
    def getHandValue(cards):
        """Возвращаем стоимость карт. Фигурные карты стоят 10, тузы — 11
        или 1 очко (эта функция выбирает подходящую стоимость карты)."""
        value = 0
        numberOfAces = 0

        for card in cards:
            rank = card[0]
            if rank == 'A':
                numberOfAces += 1
            elif rank in ('K', 'Q', 'J'):
                value += 10
            else:
                value += int(rank)

        value += numberOfAces
        for i in range(numberOfAces):
            if value + 10 <= 21:
                value += 10
        return value

    @staticmethod
    def displayHands(playerHand, dealerHand, showDealerHand):
        if showDealerHand:
            print('DEALER:', Card.getHandValue(dealerHand))
            Card.displayCards(dealerHand)
        else:
            print('DEALER: ???')
            Card.displayCards([BACKSIDE] + dealerHand[1:])

        print("Player: ", Card.getHandValue(playerHand))
        Card.displayCards(playerHand)


class Deck():
    def __init__(self):
        self.card = Card()
        self.deck = []

    def getDeck(self):
        """Возвращает список котрежей (номинал, масть) для всех 52 карт"""
        HEARTS = chr(9829)
        DIAMONDS = chr(9830)
        SPADES   = chr(9824)
        CLUBS    = chr(9827)
 
        for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
            for rank in range(2, 11):
                self.deck.append((str(rank), suit))
            for rank in ('J', 'Q', 'K', 'A'):
                self.deck.append((rank, suit))
        random.shuffle(self.deck)
        return self.deck




class Game():
    def __init__(self):
        self.game_deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    def run(self):
        # Цикл игры
        while True:
            if self.player.money <= 0:
                print("Ты проиграл")
                sys.exit()

            self.game_deck.getDeck()
            print(self.game_deck.deck)

            self.player.playerHand = [self.game_deck.deck.pop(), self.game_deck.deck.pop()]
            self.dealer.dealerHand = [self.game_deck.deck.pop(), self.game_deck.deck.pop()]
            
            print(f"money: {self.player.money}")
            self.player.getBet()

            print("Твоя ставка: ", self.player.bet)

            # Цикл хода
            while True:
                Card.displayHands(self.player.playerHand, self.dealer.dealerHand, False)
                print()

                if Card.getHandValue(self.player.playerHand) > 21:
                    break

                move = self.player.getMove()

                if move == 'D':
                    additionalBet = self.getBet(min(self.player.bet, (self.player.money - self.player.bet)))
                    self.player.bet += additionalBet # ! ****************************************************************
                    print('Bet increased to {}.'.format(self.player.bet))
                    print('Bet:', self.player.bet)

                if move in ('H', 'D'):
                    # Hit/doubling down takes another card.
                    newCard = self.game_deck.deck.pop()
                    rank, suit = newCard
                    print('You drew a {} of {}.'.format(rank, suit))
                    self.player.playerHand.append(newCard)

                if Card.getHandValue(self.player.playerHand) > 21:
                    # The player has busted:
                    continue

                if move in ('S', 'D'):
                    # Stand/doubling down stops the player's turn.
                    break 


            if Card.getHandValue(self.player.playerHand) <= 21:
                while Card.getHandValue(self.dealer.dealerHand) < 17:
                    # The dealer hits:QUIT
                    
                    print('Dealer hits...')
                    self.dealer.dealerHand.append(self.deck.pop())
                    Card.displayHands(self.player.playerHand, self.dealer.dealerHand, False)

                    if Card.getHandValue(self.dealer.dealerHand) > 21:
                        break  # The dealer has busted.
                    input('Press Enter to continue...')
                    print('\n\n')
            
            Card.displayHands(self.player.playerHand, self.dealer.dealerHand, True)

            playerValue = Card.getHandValue(self.player.playerHand)
            dealerValue = Card.getHandValue(self.dealer.dealerHand)
            # Handle whether the player won, lost, or tied:
            if dealerValue > 21:
                print('Dealer busts! You win ${}!'.format(self.player.bet))
                self.player.money += self.player.bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost!')
                self.player.money -= self.player.bet
            elif playerValue > dealerValue:
                print('You won ${}!'.format(self.player.bet))
                self.player.money += self.player.bet
            elif playerValue == dealerValue:
                print('It\'s a tie, the bet is returned to you.')

            input('Press Enter to continue...')
            print('\n\n')


if __name__ == "__main__":
   game = Game()
   game.run()