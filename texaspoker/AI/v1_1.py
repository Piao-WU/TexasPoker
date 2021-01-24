'''
    AI: v1_1版本
    详见AI-v1.1_interpretation.txt
'''
from lib.client_lib import State
from lib.client_lib import Player
from lib.client_lib import Hand
from lib.client_lib import Decision
import random

def ai(id, state):
    weight = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    remain_card = list(range(0, 52))
    cards = state.sharedcards + state.player[id].cards
    num_cards = [i//4 for i in cards]
    color_cards = [i%4 for i in cards]
    num = len(cards)
    big_blind = 40
    alpha = 1 
    # 波动系数 3人局并且求稳定 正常打法 
    # 在需要修改时 提高alpha
    for x in cards:
        remain_card.pop(remain_card.index(x))
    cnt = [0 for col in range(11)]
    # 模拟发牌1000次
    for i in range(2000):
        heap = remain_card[:]
        mycards = cards[:]
        random.shuffle(heap)
        while len(mycards) != 7:
            mycards.append(heap.pop())
        hand = Hand(mycards)
        level = hand.level
        cnt[level] += weight[level]

    # sum为评估值
    sum = 0
    for x in cnt:
        sum += x / 2000

    decision = Decision()
    totalbet = 0
    delta = state.minbet - state.player[state.currpos].bet
    if delta >= state.player[state.currpos].money:
        totalbet = 2000
    else:
        totalbet = state.player[state.currpos].totalbet + state.minbet
    

    def decide_1(decision, state, totalbet, upper_bet):
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        else:
            decision.allin = 1
        return decision
    
    def decide_2(decision, state, totalbet, upper_bet):
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        else:
            decision.callbet = 1
        return decision
    def decide_3(decision, state, totalbet, upper_bet):
        if totalbet < upper_bet:#4倍Big Blind
            decision = add_bet(state, upper_bet)
        elif totalbet < 3*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
#    def decide_4(decision, state, totalbet, upper_bet):
#        if totalbet < upper_bet:#2倍Big Blind
#            decision = add_bet(state, upper_bet)
#        elif totalbet < 2.5*upper_bet:
#            decision.callbet = 1
#        else:
#            decision.giveup = 1
#        return decision
    def decide_4(decision, state, totalbet, upper_bet):
        if delta <= 40: #加一倍大盲注以内
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_5(decision, state, totalbet, upper_bet):
        if delta <= 20:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_6(decision, state, totalbet, upper_bet):
        if delta == 0:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
      
    if num==2:
        if num_cards[0] == num_cards[1]:
            # 对子
            if max(num_cards) >= 10:
                # QQ KK AA 一等牌力
                upper_bet = 8*big_blind*alpha
                decision = decide_1(decision, state, totalbet, upper_bet)

            if max(num_cards) >=8 and max(num_cards) <=9:
                # TT JJ 二等牌力
                upper_bet = 8*big_blind*alpha
                decision = decide_2(decision, state, totalbet, upper_bet)
                
            if max(num_cards) >=6 and max(num_cards) <=7:
                #  88 99 三等牌力
                upper_bet = 4*big_blind*alpha
                decision = decide_3(decision, state, totalbet, upper_bet)
            else:
                # 77以下对子 四等牌力
                upper_bet = 2*big_blind*alpha
                decision = decide_3(decision, state, totalbet, upper_bet)                
        else:            
            #非对子
            if color_cards[0] != color_cards[1]:
                # 非同花
                if num_cards in [[12,11],[11,12]]:
                    upper_bet = 8*big_blind*alpha
                    decision = decide_1(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,10],[10,12],[11,10],[10,11]]:
                    upper_bet = 8*big_blind*alpha
                    decision = decide_2(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,9],[11,9],[10,9],[9,10],[9,11],[9,12]]:
                    upper_bet = 4*big_blind*alpha
                    decision = decide_3(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,8],[12,7],[12,6],[12,5],[12,4],[12,3],[11,8],[10,8],[9,8],[8,9],[8,10],[8,11],[3,12],[4,12],[5,12],[6,12],[7,12],[8,12]]:
                    upper_bet = 2*big_blind*alpha
                    decision = decide_4(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,2],[12,1],[12,0],[0,12],[1,12],[2,12],[11,7],[10,7],[9,7],[8,7],[7,8],[7,9],[7,10],[7,11],[6,9],[9,6],[8,6],[7,6],[6,7],[6,8],[5,7],[7,5],[5,6],[6,5],[4,6],[4,5],[5,4],[6,4],[3,4],[4,3]]:
                    upper_bet = big_blind*alpha
                    decision = decide_5(decision, state, totalbet, upper_bet)
                else:
                    upper_bet = big_blind*alpha
                    decision = decide_6(decision, state, totalbet, upper_bet)                   
            else:
                # 同花
                if num_cards in [[12,11],[11,12]]:
                    upper_bet = 8*big_blind*alpha
                    decision = decide_1(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,10],[10,12],[11,10],[10,11],[12,9],[9,12]]:
                    upper_bet = 8*big_blind*alpha
                    decision = decide_2(decision, state, totalbet, upper_bet)
                elif num_cards in [[12,8],[12,7],[12,6],[12,5],[12,4],[12,3],[11,9],[10,9],[9,10],[9,11],[3,12],[4,12],[5,12],[6,12],[7,12],[8,12],[11,8],[8,11]]:
                    upper_bet = 4*big_blind*alpha
                    decision = decide_3(decision, state, totalbet, upper_bet)
                elif num_cards in [[10,8],[9,8],[8,9],[8,10],[11,7],[10,7],[9,7],[8,7],[7,8],[7,9],[7,10],[7,11],[6,9],[9,6],[8,6],[7,6],[6,7],[6,8],[5,7],[7,5],[5,6],[6,5],[4,6],[4,5],[5,4],[6,4],[3,4],[4,3]]:
                    upper_bet = 2*big_blind*alpha
                    decision = decide_4(decision, state, totalbet, upper_bet)
                elif num_cards in [[11,6],[10,6],[9,6],[8,5],[7,5],[7,4],[6,4],[5,3],[4,2],[3,2],[2,1],[1,2],[2,3],[2,4],[3,5],[4,6],[4,7],[5,7],[5,8],[6,9],[6,10],[6,11]]:
                    upper_bet = big_blind*alpha
                    decision = decide_5(decision, state, totalbet, upper_bet)
                else:
                    upper_bet = big_blind*alpha
                    decision = decide_6(decision, state, totalbet, upper_bet)      
                        

    elif num == 5:
        # 五张牌
        if sum < 4:
            # 直接放弃
            decision.giveup = 1
        elif sum >= 4 and sum < 10:
            # 若跟注后超过150，放弃。否则跟注
            # 若已下的注额大于200, 且本次需跟注额不大于50， 则跟注
            if totalbet < 300:
                    decision.callbet = 1
            elif state.player[state.currpos].totalbet + state.player[state.currpos].bet > 200 and delta < 50:
                decision.callbet = 1
            else:
                decision.giveup = 1
        elif sum >= 10 and sum < 20:
            # 跟注。若跟注后低于300，加注到300
            if totalbet < 600:
                decision = add_bet(state, 600)
            else:
                decision.callbet = 1
        elif sum >= 20 and sum < 50:
            # 跟注。若跟注后低于600，加注到600
            if totalbet < 1200:
                decision = add_bet(state, 1200)
            else:
                decision.callbet = 1
        else:
            # allin
            decision.allin = 1

    elif num == 6:
        # 六张牌
        if sum < 2:
            # 直接放弃
            decision.giveup = 1
        elif sum >= 2 and sum < 8:
            # 若跟注后超过300，放弃。否则跟注
            # 若已下的注额大于200, 且本次需跟注额不大于50， 则跟注
            if totalbet < 600:
                    decision.callbet = 1
            elif state.player[state.currpos].totalbet + state.player[state.currpos].bet > 200 and delta < 50:
                decision.callbet = 1
            else:
                decision.giveup = 1
        elif sum >= 8 and sum < 20:
            # 跟注。若跟注后低于300，加注到300
            if totalbet < 600:
                decision = add_bet(state, 300)
            else:
                decision.callbet = 1
        elif sum >= 20 and sum < 40:
            # 跟注。若跟注后低于600，加注到600
            if totalbet < 1200:
                decision = add_bet(state, 1200)
            else:
                decision.callbet = 1
        else:
            # allin
            decision.allin = 1

    elif num == 7:
        # 七张牌
        if level == 7:
            # allin
            decision.allin = 1
        elif level == 6:
            # 跟注，若跟注后低于600，加注到600
            if totalbet < 1200:
                decision = add_bet(state, 1200)
            else:
                decision.callbet = 1
        elif level == 5:
            # 跟注，若跟注后低于500，加注到500
            if totalbet < 1000:
                decision = add_bet(state, 1000)
            else:
                decision.callbet = 1
        elif level == 4:
            # 跟注，若跟注后低于400，加注到400
            if totalbet < 800:
                decision = add_bet(state, 800)
            else:
                decision.callbet = 1

        elif level == 3:
            # 若跟注后超过500，放弃。否则跟注。若跟注后低于300，加注到300
            # 若已下的注额大于200, 且本次需跟注额不大于50， 则跟注
            if totalbet < 600:
                decision = add_bet(state, 600)
            elif totalbet < 1000:
                decision.callbet = 1
            elif state.player[state.currpos].totalbet + state.player[state.currpos].bet > 200 and delta < 50:
                decision.callbet = 1
            else:
                decision.giveup = 1
        elif level == 2:
            if cards.count(0) == 2 or cards.count(12) == 2:
                # 双A双K 若跟注后超过200，放弃。否则跟注
                # 若已下的注额大于200, 且本次需跟注额不大于50， 则跟注
                if totalbet < 400:
                    decision.callbet = 1
                elif state.player[state.currpos].totalbet + state.player[state.currpos].bet > 200 and delta < 50:
                    decision.callbet = 1
                else:
                    decision.giveup = 1
            else:
                # 不超过双Q 若跟注后超过200，放弃。否则跟注
                if totalbet > 400:
                    decision.giveup = 1
                else:
                    decision.callbet = 1
        elif level == 1:
            decision.giveup = 1
        else:
            print('the num of cards is {}'.format(num))
            assert(0)
            
    if decision.callbet == 1 and delta == state.player[state.currpos].money:
        decision.callbet = 0
        decision.allin = 1
    if decision.callbet == 1 and state.minbet == 0:
        t = random.randint(0,2)
        if t == 0:
            decision.callbet = 0
            decision.raisebet = 1
            decision.amount = state.bigBlind
    return decision
# add_bet: 将本局总注额加到total

def add_bet(state, total):
    # amount: 本局需要下的总注
    amount = total - state.player[state.currpos].totalbet
    assert(amount > state.player[state.currpos].bet)
    # Obey the rule of last_raised
    minamount = state.last_raised + state.minbet
    real_amount = max(amount, minamount)
    # money_needed = real_amount - state.player[state.currpos].bet
    decision = Decision()
    decision.raisebet = 1
    decision.amount = real_amount
    return decision
