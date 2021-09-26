from EHS_compare import HandStrength as He
"""
def get_winp(my_cards,public_cards):
    Package = H.HP(my_cards,public_cards)# 手牌、公共牌
    P_Pop,N_Pop,HS = Package
    win_p = HS*(1-N_Pop) + (1-HS)*P_Pop
    return win_p
"""

# He.random_sample(10, 52)
# He.random_sample(10, 100)
# He.random_sample(10, 1000)
He.random_sample(10,5000)
# He.random_sample(10, 10000)
He.random_sample(10,7500)
He.random_sample(10,50000)
He.random_sample(10,30000)
# He.random_sample(10, 100000)
# He.random_sample(10, 500000)
