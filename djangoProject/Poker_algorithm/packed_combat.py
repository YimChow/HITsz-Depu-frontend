import Poker_algorithm.MCTS_frame_new.action_packages as action_packages
import random
import Poker_algorithm.MCTS_frame_new.MCTS as MCTS
import Poker_algorithm.MCTS_frame_new.preflop_data as preflop_data
import Poker_algorithm.EHS_compare.compare_func as cmp
import os

def show_board(game,set):
    os.system("cls")
    print("______________________________\n"
          "|                            |\n"
          "board:                       |")
    print("|",MCTS.cards_visualize(game.board_cards+game.add_card).center(26),"|")
    print("______________________________")
    print("computer               you    ")
    print("[?, ?]----------------",MCTS.cards_visualize(set[1].card))
    print("chips____________________chips")
    print(str(set[0].model.chips)+"____________________"+str(set[1].model.chips))
    print("bet________________________bet")
    print(str(set[0].bet)+"______________________"+str(set[1].bet))
    print("total_bet:".center(30))
    print(str(game.bet_amount).center(30))



class Player(object):
    def __init__(self):
        self.deck = []
        self.card = []
        self.bet = 0
        self.model = MCTS.Opponent_Model()

    def make_action(self, game, opponent, preflop_table):
        print("game status: round "+str(game.round)+" turn "+str(game.counter))
        x = action_packages.action_choice(game, self.card, self.deck, self.model, opponent.model, game.board_cards,
                                      game.add_card, preflop_table)
        # 9.5 修改：对调self.model和opponent.model位置
        # 9.5 修改2：再对调回来。因为action_set会加反。

        if x >= 1:
            add_amount = opponent.bet - self.bet
            print("add_amount  "+str(add_amount))
            self.model.chips -= add_amount
            self.bet = opponent.bet
            game.bet_amount += add_amount

        if x == 2:
            #print("bet!")
            self.model.chips -= self.model.bet_amount[-1] * game.set_amount
            game.bet_amount += self.model.bet_amount[-1] * game.set_amount
            self.bet += self.model.bet_amount[-1] * game.set_amount
        #print("bet amount: "+str(game.bet_amount))

        return x

    def non_auto_action(self, opponent, game, action, amount):
        print("game status: round "+str(game.round)+" turn "+str(game.counter))
        action = int(input("your action: "))
        self.model.action_set.append(action)
        if action >= 1:
            add_amount = opponent.bet-self.bet
            self.bet += add_amount
            self.model.chips -= add_amount
            game.bet_amount += add_amount
        if action == 2:
            amount = float(input("your amount: "))
            self.model.bet_amount.append(amount)
            game.bet_amount += game.set_amount * amount
            self.model.chips -= game.set_amount * amount
            self.bet += self.model.bet_amount[-1] * game.set_amount

        return action

    def self_action(self, opponent, game, action, amount):
        self.model.action_set.append(action)
        self.bet += amount
        self.model.chips -= amount
        game.bet_amount += amount

def card_allocate(player_set, game):
    if game.counter != 1:
        return
    if game.round == 1:
        init_deck = [i for i in range(52)]
        for player in player_set:
            player.deck = list(init_deck)
            player.card = random.sample(init_deck, 2)
            #MCTS.cards_visualize(player.card)
            for card in player.card:
                init_deck.remove(card)
                player.deck.remove(card)
        game.deck = init_deck
        game.board_cards = []
        game.add_card = []
    if game.round == 2:
        board = random.sample(game.deck, 3)
        for card in board:
            game.deck.remove(card)
        for player in player_set:
            for card in board:
                player.deck.remove(card)
        game.board_cards = board
    if game.round == 3:
        add_card = random.sample(game.deck,1)
        game.deck.remove(add_card[0])
        game.add_card = add_card
        for player in player_set:
            player.deck.remove(add_card[0])
    if game.round == 4:
        game.board_cards.append(game.add_card[0])
        game.add_card = random.sample(game.deck, 1)
        for player in player_set:
            player.deck.remove(game.add_card[0])
    #print("boards: "+str(game.board_cards))
    #MCTS.cards_visualize(game.board_cards)
    #print("add_card: "+str(game.add_card))
    #MCTS.cards_visualize(game.add_card)



def start_pve_game(money):
    p1 = Player()
    p2 = Player()
    p1.model.chips = money[0]
    p2.model.chips = money[1]
    p1.bet = 0
    p2.bet = 0
    game = action_packages.Game()
    game.bet_amount = 15*(int(sum(money)/100)/10)
    game.set_amount = 10*(int(sum(money)/100)/10) # basic settigs
    preflop_table = preflop_data.get_table()
    set = [p1, p2]
    game.act_num = 0
    rdact = random.randint(0, 1)
    if rdact == 0:
        p1.model.chips -= 1 * game.set_amount
        p1.bet = game.set_amount
        p2.model.chips -= 0.5 * game.set_amount
        p2.bet = 0.5 * game.set_amount
        # p1先手
    else:
        p1.model.chips -= 0.5 * game.set_amount
        p1.bet = game.set_amount * 0.5
        p2.model.chips -= 1 * game.set_amount
        p2.bet = game.set_amount
    x = 1
    while game.round < 5:
        if (game.act_num + rdact) % 2 == 1:
            card_allocate(set, game)
            #print(game.act_num)
            show_board(game,set)
            x = p1.make_action(game, p2, preflop_table)
            os.system("pause")
            if x == 0:
                p2.model.chips += game.bet_amount
                print("you win, now computer has: "+str(p1.model.chips)+"  you have: "+str(p2.model.chips))
                os.system("pause")
                break

        else:
            game.act_num += 1
            card_allocate(set, game)
            show_board(game,set)
            #print("board_card: ", end=" ")
            MCTS.cards_visualize(game.board_cards + game.add_card)
            #print("your_card: ", end=" ")
            MCTS.cards_visualize(p2.card)
            x = p2.non_auto_action(p1, game)
            #print("bet amount: " + str(game.bet_amount))
            if x == 2:
                game.counter += 1
            elif x == 1 and game.counter >= 2:
                game.round += 1
                game.counter = 1
            else:
                game.counter += 1
            os.system("pause")

            if x == 0:
                p1.model.chips += game.bet_amount
                print("computer wins, now computer has: " + str(p1.model.chips) + "  you have: " + str(p2.model.chips))
                os.system("pause")
                break
        #print("p1 chips & p2 chips  " + str(p1.model.chips)+"  "+str(p2.model.chips))

    if x:
        print("computer's card: ",end=" ")
        MCTS.cards_visualize(p1.card)
        judge = cmp.Judgement(p1.card, p2.card, game.board_cards + game.add_card)
        if judge.status == 0:
            print("computer wins!")
        elif judge.status == 1:
            print("draw!")
        else:
            print("you_win!")
        print("computer: action and amount set:" + str(p1.model.action_set) + "\n" + str(p1.model.bet_amount))
        print("you: action and amount set:" + str(p2.model.action_set) + "\n" + str(p2.model.bet_amount))
        if judge.status == 2:
            p2.model.chips += game.bet_amount
            print("you win, now computer has: " + str(p1.model.chips) + "  you have: " + str(p2.model.chips))
        elif judge.status == 0:
            p1.model.chips += game.bet_amount
            print("computer wins, now computer has: " + str(p1.model.chips) + "  you have: " + str(p2.model.chips))
        else:
            p1.model.chips += 0.5*game.bet_amount
            p2.model.chips += 0.5*game.bet_amount
        os.system("pause")

    return [p1.model.chips,p2.model.chips]



if __name__ == "__main__":
    money = [500,500]
    # computer // player
    for i in range(5):
        set = start_pve_game(money)
        money = set
        if money[0] == 0:
            print("computer is broken up, You win")
        if money[1] == 0:
            print("you are broken up, Game Over")
    if money[0]>money[1]:
        print("computer wins")
    if money[1]>money[0]:
        print("you win")
    else:
        print("draw")

