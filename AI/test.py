# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 17:57:55 2021

@author: 85716
"""


from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

import sys
sys.path.append('D:\\德州\\Texaspoker1.6\\Texaspoker\\modules\\texaspoker')
#
#from client.client import printcard
#lst = [2,3,4,5,6,7,8,9,'T','J','Q','K','A']
#for i in range(13):
#    for j in range(i,13):
#        hand = ['H'+str(lst[i]),'H'+str(lst[j])]
#        hand2 = ['D'+str(lst[i]),'H'+str(lst[j])]
#        hole_card = gen_cards(hand)
#        hole_card2 = gen_cards(hand2)
#        community_card = gen_cards([])
#        estimate = estimate_hole_card_win_rate(nb_simulation=1000, nb_player=3, hole_card=hole_card, community_card=community_card)
#        estimate2 = estimate_hole_card_win_rate(nb_simulation=1000, nb_player=3, hole_card=hole_card2, community_card=community_card)
#        if i != j:
#            print([lst[i],lst[j]],estimate2,estimate)
#        else:
#            print([lst[i],lst[j]],estimate2)

        
#    hole_card = gen_cards([])
hole_card = gen_cards(['CA', 'S5'])
community_card = gen_cards(['SA','D5','C3','D9'])
#community_card = gen_cards(['HA','DK','HQ'])
estimate_hole_card_win_rate(nb_simulation=10000, nb_player=3, hole_card=hole_card, community_card=community_card)




##0.825
#estimate_hole_card_win_rate(nb_simulation=1000, nb_player=3, hole_card=hole_card, community_card=community_card)
#0.838
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

import random
from lib.client_lib import Hand


def test_win_rate(hand1,share_card1):
    print(cards2newcards(hand1))
    print(cards2newcards(share_card1))
    hole_card = gen_cards(cards2newcards(hand1))
    community_card = gen_cards(cards2newcards(share_card1)) 
    mycards = hand1 + share_card1
    #cards = state.sharedcards + state.player[id].cards
    hand = Hand(mycards)
    level = hand.level
#    print(level)
    est = estimate_hole_card_win_rate(nb_simulation=10000, nb_player=3, hole_card=hole_card, community_card=community_card)
    print(est)

hand1 = [42,43]
share_card1 = [8,40,41,50,51]
test_win_rate(hand1,share_card1)

hand1 = [48,15]
share_card1 = [8,40,41,50,51]
test_win_rate(hand1,share_card1)
#estimate_hole_card_win_rate(nb_simulation=10000, nb_player=3, hole_card=hole_card, community_card=community_card)
 
hand1 = [48,49]
share_card1 = [8,40,41,50,51]
test_win_rate(hand1,share_card1)

hand1 = [0,1]
share_card1 = []
test_win_rate(hand1,share_card1)  
############## 顺子
# 潮湿底牌3456
hand1 = [7,0]
share_card1 = [5,11,14,19,30]
test_win_rate(hand1,share_card1)
#0.51 0.78

#干燥底牌456
hand1 = [11,16]
share_card1 = [7,14,23,30,36]
test_win_rate(hand1,share_card1)
#0.9753


# 潮湿底牌TJQK
hand1 = [22,50]
share_card1 = [33,37,41,46,10]
test_win_rate(hand1,share_card1)
#0.51 0.78

#干燥底牌 
hand1 = [29,46]
share_card1 = [33,37,41,16,10]
test_win_rate(hand1,share_card1)
#0.9753


########## 同花
# 干燥底牌 S7 SJ SK
hand1 = [4,0]
share_card1 = [5,11,20,36,44]
test_win_rate(hand1,share_card1)
#0.9524-1.0

# 潮湿底牌S7 S8 SJ SK
hand1 = [15,28]
share_card1 = [5,20,24,36,44]
test_win_rate(hand1,share_card1)
# 0.48-0.999



########### 三条
# 干燥底牌 2
hand1 = [45,46]
share_card1 = [2,15,20,29,44]
test_win_rate(hand1,share_card1)
#0.945-0.964

# 潮湿底牌22
hand1 = [46,47]
share_card1 = [2,7,20,45,44]
test_win_rate(hand1,share_card1)
# 0.9151 - 1.0


########## 两对
# 干燥底牌1  
hand1 = [3,6]
share_card1 = [2,7,20,35,44]
test_win_rate(hand1,share_card1)

# 潮湿底牌
hand1 = [45,34]
share_card1 = [2,7,6,35,44]
test_win_rate(hand1,share_card1)
#0.8118
hand1 = [45,30]
share_card1 = [2,7,6,35,44]
test_win_rate(hand1,share_card1)
#0.7505

hand1 = [8,34]
share_card1 = [2,7,6,35,44]
test_win_rate(hand1,share_card1)
#0.4816

hand1 = [1,34]
share_card1 = [2,7,6,35,44]
test_win_rate(hand1,share_card1)
#0.4699

###### 一对
hand1 = [44,45]
share_card1 = [0,7,20,27,41]
test_win_rate(hand1,share_card1)
# 干燥下 0.12-0.79

hand1 = [46,31]
share_card1 = [0,7,20,43,42]
test_win_rate(hand1,share_card1)






def test_win_rate_2(hand1,share_card1):
    print(cards2newcards(hand1))
    print(cards2newcards(share_card1))
    hole_card = gen_cards(cards2newcards(hand1))
    community_card = gen_cards(cards2newcards(share_card1)) 
    mycards = hand1 + share_card1
    #cards = state.sharedcards + state.player[id].cards
    hand = Hand(mycards)
#    level = hand.level
#    print(level)
    est = estimate_hole_card_win_rate(nb_simulation=5000, nb_player=3, hole_card=hole_card, community_card=community_card)
    return est
#    print(est)





import pandas as pd


share_card1 = [0,29,47,22]
#share_card1 =[5,13,22]
#share_card1 = [11,22,26]
#share_card1 =[18,40,51]
print(cards2newcards(share_card1))

handcard = []
rate = []
z=0
for i in range(0,52,4):
    
    a=[k for k in range(0,52,4)]
    a.pop(z)
    print(i)
    for j in a:
        hand1 = [i,j]
        handcard.append(cards2newcards(hand1))
        rate.append(test_win_rate_2(hand1,share_card1))
    z += 1


     
# dictionary of lists   
dict1 = {'handcard': handcard, 'win_rate': rate}        
df = pd.DataFrame(dict1)  
# saving the dataframe  
df.to_csv('winrate4_1.csv') 









share_card1 = [0,29,47,22]
print(cards2newcards(share_card1))

handcard = []
rate = []
z=0
for i in range(0,52,4):
    hand1 = [i,i+1]
    handcard.append(cards2newcards(hand1))
    rate.append(test_win_rate_2(hand1,share_card1))
    z += 1
# dictionary of lists   
dict2 = {'handcard': handcard, 'win_rate': rate}        
df2 = pd.DataFrame(dict2)  
# saving the dataframe  
df2.to_csv('winrate4_2.csv') 

