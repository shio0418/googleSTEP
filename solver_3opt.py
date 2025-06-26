#!/usr/bin/env python3
# 参考:
# https://www.cst.nihon-u.ac.jp/research/gakujutu/57/pdf/L-20.pdf

import sys

from common import print_tour, read_input, calc_total_length
from solver_greedy import solve as solve_greedy, distance 


def solve(cities):
    N = len(cities)
    MAX_ROOP = 1000
    r_cnt = 0
    
    current_tour = solve_greedy(cities)
    # 経路に変化があったか示すフラグ
    changed = True
    best_route = []
    best_total = float('inf')

    while changed and r_cnt < MAX_ROOP:
        r_cnt += 1
        changed = False
        # 変化量
        best_diff = 0
        # 交換すべきiとj
        best_i = -1
        best_j = -1
        best_k = -1
        best_case = -1
        # i+1,j,j+1,k,k+1は除くため
        for i in range(N-5):
            a = cities[current_tour[i]]
            b = cities[current_tour[(i+1) % N]]
            # j+1,k,k+1は除くため
            for j in range(i+2,N-3):
                c = cities[current_tour[j]]
                d = cities[current_tour[(j+1) % N]]
                # k+1は除くため
                for k in range(j+2,N-1):
                    e = cities[current_tour[k]]
                    f = cities[current_tour[(k+1) % N]]
                    # i,j の2opt
                    diff1 = distance(a,c) + distance(b,d) - (distance(a,b) + distance(c,d))
                    # j,kの2opt
                    diff2 = distance(c,e) + distance(d,f) - (distance(c,d) + distance(e,f))
                    # i,k
                    diff3 = distance(e,a) + distance(f,b) - (distance(e,f) + distance(a,b))

                    # 3opt
                    diff4 = distance(a,c) + distance(b,e) + distance(f,d) - (distance(a,b) + distance(c,d) + distance(e,f))
                    diff5 = distance(a,e) + distance(c,b) + distance(f,d) - (distance(a,b) + distance(c,d) + distance(e,f))
                    diff6 = distance(a,e) + distance(b,d) + distance(c,f) - (distance(a,b) + distance(c,d) + distance(e,f))
                    diff7 = distance(a,c) + distance(b,f) + distance(e,d) - (distance(a,b) + distance(c,d) + distance(e,f))
                    
                    diffs = [diff1,diff2,diff3,diff4,diff5,diff6,diff7]
                    min_diff = min(diffs)
                    case = diffs.index(min_diff) + 1

                    if min_diff < best_diff:
                        print(calc_total_length(cities,current_tour))
                        best_diff = min_diff
                        changed = True
                        best_i = i
                        best_j = j
                        best_k = k
                        best_case = case

        if changed:
            if best_case == 1:
                current_tour[best_i+1:best_j+1] = list(reversed(current_tour[best_i+1:best_j+1]))
            elif best_case == 2:
                current_tour[best_j+1:best_k+1] = list(reversed(current_tour[best_j+1:best_k+1]))
            elif best_case == 3:
                current_tour[best_i+1:best_k+1] = list(reversed(current_tour[best_i+1:best_k+1]))
            elif best_case == 4:
                tmp = current_tour[best_i+1:best_j+1] + current_tour[best_j+1:best_k+1]
                tmp = list(tmp)
                tmp.reverse()
                current_tour[best_i+1:best_k+1] = tmp
            elif best_case == 5:
                tmp = current_tour[best_j+1:best_k+1] + current_tour[best_i+1:best_j+1]
                tmp = list(tmp)
                current_tour[best_i+1:best_k+1] = tmp
            elif best_case == 6:
                tmp1 = list(reversed(current_tour[best_i+1:best_j+1]))
                tmp2 = list(reversed(current_tour[best_j+1:best_k+1]))
                current_tour[best_i+1:best_j+1] = tmp1
                current_tour[best_j+1:best_k+1] = tmp2
            elif best_case == 7:
                tmp = list(reversed(current_tour[best_j+1:best_k+1])) + list(reversed(current_tour[best_i+1:best_j+1]))
                tmp = list(tmp)
                current_tour[best_i+1:best_k+1] = tmp
            else:
                assert(0)
            assert len(current_tour) == N

                # 変化が小さかったら打ち切り
        if abs(best_diff) < 0.01:
            break
        
        current_total = calc_total_length(cities,current_tour)
        if current_total < best_total:
            best_route = current_tour
        
    return best_route


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
    total = calc_total_length(cities,tour)
    print("Total length is ",total)

