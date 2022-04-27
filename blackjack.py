#  ___
# |8  |
# | ! |
# |__8|

# https://inventwithpython.com/charactermap)

import sys
import random

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES   = chr(9824)
CLUBS    = chr(9827)

BACKSIDE = 'backside'

def main():
    money = 5000

    while True:
        if money <= 0:
            print("Ты проиграл")
            sys.exit()
        
        print(f"money: {money}")
        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print("Твоя ставка: ", bet)

        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break

            move = getMove(playerHand, money - bet)

            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # The player has busted:
                    continue

            if move in ('S', 'D'):
                # Stand/doubling down stops the player's turn.
                break

        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                 # The dealer hits:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break  # The dealer has busted.
                input('Press Enter to continue...')
                print('\n\n')
        
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # Handle whether the player won, lost, or tied:
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')

        input('Press Enter to continue...')
        print('\n\n')


def getBet(money):
    while True:
        print(f"Какую ставку вы хотите сделать? (1-{money} or QUIT)")
        bet = input('> ').upper().strip()

        if bet == 'QUIT':
            print("Спасибо за игру!")
            sys.exit()

        if not bet.isdecimal():
            print("Вы ввели что-то не то, товарищ. Мяу")
            continue

        bet = int(bet)
        if 1 <= bet <= money:
            return bet


def getDeck():
    """Возвращает список котрежей (номинал, масть) для всех 52 карт"""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards([BACKSIDE] + dealerHand[1:])

    print("Player: ", getHandValue(playerHand))
    displayCards(playerHand)


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


def displayCards(cards):
    """Отрисовать карты на экране"""
    rows = ['', '', '', '', '',]

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


def getMove(playerHand, money):
    """Спрашиваем, какой ход хочет сделать игрок, и возвращаем 'H', если он
    хочет взять еще карту, 'S', если ему хватит, и 'D', если он удваивает."""
    while True:
        moves = ['(H)it', '(S)tand']

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Get the player's move:
        movePrompt = ', '.join(moves) + '> '
    
        move = input(movePrompt).upper() # x =  input("Введите что-то: ")

        if move in ('H', 'S'):
            return move  # Player has entered a valid move.
        if move == 'D' and '(D)ouble down' in moves:
            return move  # Player has entered a valid move.
        
        print('Введите корректное значение!')



#if __name__ == "__main__":
#    main()




