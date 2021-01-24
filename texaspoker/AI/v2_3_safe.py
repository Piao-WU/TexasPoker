# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 01:20:03 2021

@author: 85716
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 02:12:02 2021

@author: 85716
"""

'''
    AI: v2_2版本
    在2_1基础上 对5,6,7cards进行了一定修改，提高了一定的阈值，让打法不因过于奔放而狂野输钱
'''
from lib.client_lib import State
from lib.client_lib import Player
from lib.client_lib import Hand
from lib.client_lib import Decision
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

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
    
    ########################################
    ###################################
    def cards2newcards(cards):
        num_list = [2,3,4,5,6,7,8,9,'T','J','Q','K','A']
    #    name = ['spade', 'heart', 'diamond', 'club']
        color_list = ['S','H','D','C']
        new_cards = []
        for i in range(len(cards)):
            num = cards[i] // 4
            color = cards[i] % 4
            one_card = color_list[color]+str(num_list[num])
            new_cards.append(one_card)
        return new_cards
    hand_ = cards2newcards(state.player[id].cards)
    shared_ = cards2newcards(state.sharedcards)
    hole_card = gen_cards(hand_)
    community_card = gen_cards(shared_)
    estimate = estimate_hole_card_win_rate(nb_simulation=10000, nb_player=3, hole_card=hole_card, community_card=community_card)
    

    decision = Decision()
    totalbet = 0
    delta = state.minbet - state.player[state.currpos].bet

    if delta >= state.player[state.currpos].money:
        totalbet = 2000
    else:
        totalbet = state.player[state.currpos].totalbet + state.minbet

    def decide_1(decision, state, totalbet):
        upper_bet = 8*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        elif totalbet < 2050:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_2(decision, state, totalbet):
        upper_bet = 8*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        elif totalbet < 1200:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_3(decision, state, totalbet):
        upper_bet = 4*big_blind*alpha
        if totalbet < upper_bet:#4倍Big Blind
            decision = add_bet(state, upper_bet)
        elif totalbet < 3*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_4(decision, state, totalbet):
        upper_bet = 2*big_blind*alpha
        if totalbet < upper_bet:#2倍Big Blind
            decision = add_bet(state, upper_bet)
        elif totalbet < 2.5*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_5(decision, state, totalbet):
        if delta <= 40: #加一倍大盲注以内
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_6(decision, state, totalbet):
        if delta <= 20:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7(decision, state, totalbet):
        if delta == 0:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    
#################################     
### 5 cards        
    def decide_5_1(decision, state, totalbet):
        upper_bet = 7*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 3*upper_bet:
            decision = add_bet(state, 6*upper_bet)
        elif totalbet < 2050:
            decision.callbet = 1
        else:
            decision.giveup = 1

        return decision
    
    def decide_5_2(decision, state, totalbet):
        #小于280 加到280
        #大于280 小于420 加到840
        #大于420 callbet
        upper_bet = 7*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        elif totalbet < 1200:
            decision.callbet = 1
        else:
            decision.giveup = 1

        return decision
    
    
    def decide_5_3(decision, state, totalbet):
        # 小于10倍大盲 加到10倍
        # delta<20倍时 跟注
        upper_bet = 10*big_blind*alpha
        if totalbet < upper_bet:#4倍Big Blind
            decision = add_bet(state, upper_bet)
        elif delta < 20*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    
    def decide_5_4(decision, state, totalbet):
        upper_bet = 3*big_blind*alpha
        if totalbet < upper_bet:#2倍Big Blind
            decision = add_bet(state, upper_bet)
        elif totalbet < 2.5*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_5_5(decision, state, totalbet):
        if delta <= 80: #加一倍大盲注以内
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_5_6(decision, state, totalbet):
        if delta <= 40:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_5_7(decision, state, totalbet):
        if delta == 0:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision    
    
#################################    
# 6cards
#################################     
    def decide_6_1(decision, state, totalbet):
        upper_bet = 7*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 3*upper_bet:
            decision = add_bet(state, 6*upper_bet)
        elif totalbet < 2050:
            decision.callbet = 1
        else:
            decision.giveup = 1

        return decision
    
    def decide_6_2(decision, state, totalbet):
        #小于280 加到280
        #大于280 小于420 加到840
        #大于420 callbet
        upper_bet = 7*big_blind*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.5*upper_bet:
            decision = add_bet(state, 3*upper_bet)
        elif totalbet < 1200:
            decision.callbet = 1
        else:
            decision.giveup = 1

        return decision
    
    def decide_6_3(decision, state, totalbet):
        # 小于10倍大盲 加到10倍
        # delta<20倍时 跟注
        upper_bet = 10*big_blind*alpha
        if totalbet < upper_bet:#4倍Big Blind
            decision = add_bet(state, upper_bet)
        elif delta < 20*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    
    def decide_6_4(decision, state, totalbet):
        upper_bet = 3*big_blind*alpha
        if totalbet < upper_bet:#2倍Big Blind
            decision = add_bet(state, upper_bet)
        elif totalbet < 2.5*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_6_5(decision, state, totalbet):
        if delta <= 80: #加一倍大盲注以内
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_6_6(decision, state, totalbet):
        if delta <= 40:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_6_7(decision, state, totalbet):
        if delta == 0:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision    
    
  ##############################  
  ########7cards  
    def decide_7_1(decision, state, totalbet):
        # 小于2000加到2000
        # 否则callbet
        upper_bet = 2000*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif totalbet < 1.1*upper_bet:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_2(decision, state, totalbet):
        # 小于800加到800
        # 小于1500callbet
        # 大于1500 givep
        upper_bet = 800*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif delta < 1500*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_3(decision, state, totalbet):
        upper_bet = 600*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif delta < 500*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_4(decision, state, totalbet):
        upper_bet = 300*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif delta < 300*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_5(decision, state, totalbet):
        upper_bet = 160*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif delta < 200*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_6(decision, state, totalbet):
        upper_bet = 80*alpha
        if totalbet < upper_bet:
            decision = add_bet(state, upper_bet)
        elif delta < 80*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision
    def decide_7_7(decision, state, totalbet):
        if delta < 40*alpha:
            decision.callbet = 1
        else:
            decision.giveup = 1
        return decision

    
    if num==2:
        if estimate >= 0.7:
            if totalbet < 2000:#4倍Big Blind
                decision = add_bet(state, 2000)
            else:
                decision.giveup = 1
            
        elif estimate < 0.7 and estimate >= 0.48+0.02:
            decision = decide_1(decision, state, totalbet)
        
        elif estimate < 0.48+0.02 and estimate >= 0.4+0.02:
            decision = decide_2(decision, state, totalbet)
            
        elif estimate>0.351+0.02 and estimate < 0.4+0.02:
            decision = decide_3(decision, state, totalbet)
            
        elif estimate>0.332+0.02 and estimate <=0.351+0.02:
            decision = decide_4(decision, state, totalbet)
            
        elif estimate>0.31 and estimate<=0.332+0.02:
            decision = decide_5(decision, state, totalbet)
        elif estimate>0.25 and estimate<=0.31:
            decision = decide_6(decision, state, totalbet)
        else:
            decision = decide_7(decision, state, totalbet)
            
                        

    elif num == 5:
        # 五张牌
        if estimate >= 0.74:
            decision = decide_5_1(decision, state, totalbet)
        
        elif estimate < 0.74 and estimate >= 0.55+0.05:
            decision = decide_5_2(decision, state, totalbet)
            
        elif estimate < 0.55+0.05 and estimate >= 0.39+0.03:
            decision = decide_5_3(decision, state, totalbet)
            
        elif estimate < 0.39+0.03 and estimate >= 0.34+0.03:
            decision = decide_5_4(decision, state, totalbet)
            
        elif estimate < 0.34+0.03 and estimate >= 0.25+0.05:
            decision = decide_5_5(decision, state, totalbet)
        elif estimate < 0.25+0.05 and estimate >= 0.18:
            decision = decide_5_6(decision, state, totalbet)
        else:
            decision = decide_5_7(decision, state, totalbet)

    elif num == 6:
        # 六张牌
        if estimate >= 0.78:

            decision = decide_6_1(decision, state, totalbet)
        
        elif estimate < 0.78 and estimate >= 0.56+0.05:
            decision = decide_6_2(decision, state, totalbet)
            
        elif estimate < 0.56+0.05 and estimate >= 0.41+0.05:
            decision = decide_6_3(decision, state, totalbet)
            
        elif estimate < 0.41+0.05 and estimate >= 0.29+0.04:
            decision = decide_6_4(decision, state, totalbet)
            
        elif estimate < 0.29+0.04 and estimate >= 0.24+0.04:
            decision = decide_6_5(decision, state, totalbet)
        elif estimate < 0.24+0.04 and estimate >= 0.115:
            decision = decide_6_6(decision, state, totalbet)
        else:
            decision = decide_6_7(decision, state, totalbet)
            

    elif num == 7:
        # 七张牌
        if estimate>=0.95:
            if totalbet < 2050:
                decision = add_bet(state, 2000)
            else:
                decision.giveup = 1       
        elif estimate < 0.9 and estimate >= 0.95:
            decision = decide_7_1(decision, state, totalbet)
        
        elif estimate < 0.75 and estimate >= 0.9:
            decision = decide_7_2(decision, state, totalbet)
            
        elif estimate>0.6 and estimate <= 0.75:
            decision = decide_7_3(decision, state, totalbet)
            
        elif estimate>0.35 and estimate <=0.6:
            decision = decide_7_4(decision, state, totalbet)
            
        elif estimate>0.333 and estimate<=0.35:
            decision = decide_7_5(decision, state, totalbet)
        elif estimate>0.3 and estimate<=0.333:
            decision = decide_7_6(decision, state, totalbet)
        else:
            decision = decide_7_7(decision, state, totalbet)

#        else:
#            print('the num of cards is {}'.format(num))
#            assert(0)
    if state.player[state.currpos].money <= 300:
        decision.callbet = 0
        decision.raisebet = 0
        decision.allin = 1
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
