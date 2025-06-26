# 焼きなまし法の実装

# 参考：https://qiita.com/take314/items/7eae18045e989d7eaf52
# タイトル：巡回セールスマン問題をいろんな近似解法で解く（その5: 焼きなまし法）

# memo:パラメータにより精度がかなり変わる。T・alphaが大きくend_Tが小さい方が精度が良さそうだが実行時間とトレードオフ。
#      また極端な値だと逆に精度が落ちる

import sys
import random
import time
import math

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 
from solver_random import solve as solve_random

''''
def calc_mean_distance(cities):
    total = 0
    N = len(cities)
    for i in range(N):
        c_a = cities[i]
        for j in range(i+1,N):
            c_b = cities[j]
            total += distance(c_a,c_b)
    return 2 * total / (N * (N-1))

'''

def solve(cities):
    #D = calc_mean_distance(cities)
    # 温度（時間により減少） 大きめの方が精度高い
    T = 100
    #T = D
    # 減少率
    alpha = 0.99
    # Tの境界
    end_T = 0.001
    # diffが大きくなっても変化する確率の最小値
    #border = 0.1
    N = len(cities)

    # 貪欲法で初期条件
    current_tour = solve_greedy(cities)

    # ランダム法で初期条件（貪欲法より精度低かった）
    #current_tour = list(range(N))
    #random.shuffle(current_tour)

    change = 0
    while T > end_T:
        changed = False
        # 変化量
        best_diff = 0
        # 交換すべきiとj
        best_i = -1
        best_j = -1
        random_i_list = list(range(N-1))
        random.shuffle(random_i_list)
        
        for i in random_i_list:
            a = cities[current_tour[i]]
            b = cities[current_tour[(i+1) % N]]
            
            for j in range(i+2,N):
                c = cities[current_tour[j]]
                d = cities[current_tour[(j+1) % N]]
                diff = distance(a,c) + distance(b,d) - (distance(a,b) + distance(c,d))
                #print(diff,best_diff)
                #print(i,j)

                # expの肩が絶対値700を超えるとオーバーフローしてしまうようなので
                #print(diff,T)
                if diff < 0 :
                    possib = 1
                else:
                    possib = math.exp( - (diff/T))
                # 0~1のランダムな値
                border = random.random()
                if diff < best_diff or possib > border:
                    change += 1
                    best_diff = diff
                    changed = True
                    best_i = i
                    best_j = j
        if changed:
            current_tour[best_i+1:best_j+1] = reversed(current_tour[best_i+1:best_j+1])

        # Tを冷却
        T *= alpha 
    #print(change)
    return current_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    start = time.time()
    tour = solve(cities)
    end = time.time()
    print_tour(tour)
    total = calc_total_length(cities,tour)
    print("Total length is ",total)
    print("Execution time:",end - start)

