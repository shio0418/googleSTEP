#!/usr/bin/env python3

# 2opt + 直前数経路を複数個保持してランダム確率で経路変更

import sys
import random

# queueを使う
from collections import deque
from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 

def solve_sa(cities,tour):
    N = len(cities)
    
    current_tour = tour
    # 経路に変化があったか示すフラグ
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
                
    return current_tour


def solve(r_cnt,cities):
    N = len(cities)
    best_tour = []
    current_tour = solve_greedy(cities)
    best_tour = solve_sa(cities,current_tour)
    best_total = calc_total_length(cities,best_tour)

    print(best_total)

    for i in range(r_cnt):
        random_tour = list(range(N))
        random.shuffle(random_tour)
        current_tour = solve_sa(cities,random_tour)
        current_total = calc_total_length(cities,current_tour)
        if current_total < best_total:
            best_total = current_total
            best_tour = current_tour
            print(best_total)
    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(5,cities)
    print_tour(tour)
    total = calc_total_length(cities,tour)
    print("Total length is ",total)

