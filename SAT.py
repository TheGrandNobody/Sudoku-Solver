#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, math
import numpy as np
import itertools
from pulp import *

def read_sudoku_from_file():
    args = sys.argv
    if len(args) != 2:
        sys.exit(f"usage: python3 ./{args[0]} input_sudoku_file.txt")

    try:
        with open(args[1], "r") as f:
            sudoku_in = []
            for line in f.readlines():
                #converting string line from file to integer list
                int_line = list(map(lambda t: int(t), line.replace('\n', '').split()))
                print(int_line)
                sudoku_in.append(int_line)
            return sudoku_in
    except Exception as e:
        sys.exit(e)


def num_to_cnff(p,num, invert):
    s = -1 if invert else 1
    clause = s * int(str(p)+str(num))
    return clause

def constraint(a, j, i, num, row):
    if row:
        clause_2 = -1 * int(str(i) + str(a) + str(num))
        clause_1 = -1 * int(str(i) + str(j) + str(num))
    else:
        clause_2 = -1 * int(str(a) + str(i) + str(num))
        clause_1 = -1 * int(str(j) + str(i) + str(num))
    return [(clause_1, clause_2)]#[clause_1, clause_2]

def constraint_box(i,j,a,d,num):
    clause_1 = -1 * int(str(i) + str(j) + str(num))
    clause_2 = -1 * int(str(a) + str(d) + str(num))

    return [(clause_1, clause_2)]



#write at the beginning of file
def insert(originalfile, string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string + '\n')
            f2.write(f.read())
    os.rename('newfile.txt', originalfile)

def make_cnf_dimacs(sudoku_in, out_file):
    clauses_number = 0
    #dimension of puzzle and minimal number of bits to represent one number
    n = len(sudoku_in[0])
    block = int(math.sqrt(n))
    num_of_bits = len(bin(n)[2:])

    '''
    Defining Rows, Cols and Values of Sudoku Board
    '''
    numbers = [str(i) for i in range(1, n + 1)]
    Rows = numbers
    Cols = numbers
    Values = numbers

    

    Subgrids =[]
    for i in range(block):
        for j in range(block):
            Subgrids += [[(int(Rows[block*i+k]),int(Cols[block*j+l])) for k in range(3) for l in range(3)]]

    with open(out_file, "w") as f:
            
        for r in Rows:
            for c in Cols:
                for v in Values:
                    a = int(str(r) + str(c) + str(v))
                    f.write(f"{a} ")
                f.write("0\n")

        for i in range(1, n+1):
            for j in range (1, n+1): 
                p = int(str(i)+str(j))

                #NOTE: CONSTRAINT 1
                #add numbers from given input sudoku
                #converting serial number (1-n*n) to index (i, j)
                curr_num = sudoku_in[i-1][j-1]#[(i-1)//n][(j-1)%n]
                if curr_num != 0:
                    #add all non-zero numbers
                    a = num_to_cnff(p, curr_num, False)
                    f.write(f"{a} 0\n")
                    clauses_number += 1
                for b in Subgrids:
                    for r,c in b:
                        if i is r and j is c:
                            for a, d in b:
                                if curr_num != 0:
                                    z = constraint_box(i,j,a,d, curr_num)
                                    for dd, s in z:
                                        f.write(f"{dd} ")
                                        f.write(f"{s} ")
                                        f.write("0\n")
                                        clauses_number += 1
                                else:
                                    for v in Values:
                                        z = constraint_box(i,j,a,d, v)
                                        for dd, s in z:
                                            f.write(f"{dd} ")
                                            f.write(f"{s} ")
                                            f.write("0\n")
                                            clauses_number += 1
                            break
                        else:
                            continue
                
                #NOTE: CONSTRAINT 2
                #Row
                for a in range(1, n+1):
                    if a != j & curr_num != 0:
                        z = constraint(a, j, i,curr_num, True)
                        for c, d in z:
                            f.write(f"{c} ")
                            f.write(f"{d} ")
                            f.write("0\n")
                            clauses_number += 1
                    elif a != j & curr_num == 0:
                        for v in Values:
                            z = constraint(a, j, i, v, True)
                            for c, d in z:
                                f.write(f"{c} ")
                                f.write(f"{d} ")
                                f.write("0\n")
                                clauses_number += 1


                        
                #Column
                for b in range(1, n+1):
                    if b != j & curr_num != 0:
                        z = constraint(b, i, j,curr_num, False)
                        for c, d in z:
                            f.write(f"{c} ")
                            f.write(f"{d} ")
                            f.write("0\n")
                            clauses_number += 1
                    elif b != j & curr_num == 0:
                        for v in Values:
                            z = constraint(b,i,j, v, True)
                            for c, d in z:
                                f.write(f"{c} ")
                                f.write(f"{d} ")
                                f.write("0\n")
                                clauses_number += 1

    nn_bits= n*n*num_of_bits
    return nn_bits

def dupe(out_file, n):
    lines_set = open(out_file, 'r').readlines()

    lines_set = set(lines_set)
    print(len(lines_set))
    lines_set = sorted(lines_set)
    print(len(lines_set))

    out  = open(out_file, 'w')

    for line in lines_set:
        out.write(line)
    
    out.close()

    insert(out_file, f"p cnf {n} {len(lines_set)}")

    print('fini')


def main():
    sudoku_in = read_sudoku_from_file()
    out_file = "out_sudoku3.cnf"

    n = make_cnf_dimacs(sudoku_in, out_file)
    dupe(out_file, n)


if __name__ == "__main__":
    main()

    #python3 SAT.py sudoku/test.txt
