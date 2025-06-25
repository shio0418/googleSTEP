#!/usr/bin/env python3
import sys

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 


def solve(cities):
    N = len(cities)
    
    current_tour = solve_greedy(cities)
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

if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
    total = calc_total_length(cities,tour)
    #print("Total length is ",total)

