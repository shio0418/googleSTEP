# opt2の出発点をランダムにするのを何回か繰り返す

import sys
import random
import time

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 
from solver_random import solve as solve_random

MAX_ROOP = 10

def solve(cities):
    N = len(cities)
    # 最適値に無限大をセット
    best_length = float('inf')
    best_route = []


    for roop_cnt in range(MAX_ROOP):
        # ランダムで1からNの訪問順を作成
        current_tour = list(range(N))
        random.shuffle(current_tour)

        changed = True

        while changed:
            changed = False
            # 変化量
            best_diff = 0
            # 交換すべきiとj
            best_i = -1
            best_j = -1
            for i in range(N-1):
                a = cities[current_tour[i]]
                b = cities[current_tour[(i+1) % N]]
                
                for j in range(i+2,N):
                    c = cities[current_tour[j]]
                    d = cities[current_tour[(j+1) % N]]
                    diff = distance(a,c) + distance(b,d) - (distance(a,b) + distance(c,d))
                    #print(diff,best_diff)
                    #print(i,j)
                    if diff < best_diff:
                        best_diff = diff
                        changed = True
                        best_i = i
                        best_j = j
            if changed:
                current_tour[best_i+1:best_j+1] = reversed(current_tour[best_i+1:best_j+1])
        total = calc_total_length(cities,current_tour)
        if total < best_length:
            best_length = total
            best_route = current_tour
                    
        return best_route
    


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

