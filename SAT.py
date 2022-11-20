#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, math
from attr import s
import numpy as np
import itertools
from pulp import *


def s_to_ch(l):
    ac = 0
    if l == "A":
        ac = 10
    elif l == "B":
        ac = 11
    elif l == "C":
        ac = 12
    elif l == "D":
        ac = 13
    elif l == "E":
        ac = 14
    elif l == "F":
        ac = 15
    elif l == "G":
        ac = 16
    else:
        ac = 0
    return ac

def read_sudoku_from_file(out_file):
    sudoku_in = []
    args = sys.argv
    if len(args) != 2:
        sys.exit(f"usage: python3 ./{args[0]} input_sudoku_file.txt")
    try:
        print('hier')
        with open(args[1], "r") as f:
            for line in f.readlines():
                sudoku_in = []
                rt = int(math.sqrt(len(line)))
                for i in range(0, int(math.sqrt(len(line)))):
                #converting string line from file to integer list
                    line = line.replace('\n', '')
                    int_line = [int(char) if char.isnumeric() else s_to_ch(char) for char in line]
                    print(int_line[i*rt:i*rt+rt])
                    sudoku_in.append(int_line[i*rt:i*rt+rt])
                print(sudoku_in)
                make_cnf_dimacs(sudoku_in, out_file)
            return sudoku_in
    except Exception as e:
        sys.exit(e)


def num_to_cnff(p,num, invert):
    s = -1 if invert else 1
    clause = s * int(str(p)+str(num))
    return clause

def constraint(a, j, i, num, row, sixteen):
    if sixteen:
        s = 17
        if row:
            clause_2 = -1 * int(int(i)*s*s + int(a)*s + int(num))
            clause_1 = -1 * int(int(i)*s*s + int(j)*s + int(num))
        else:
            clause_2 = -1 * int(int(a)*s*s + int(i)*s + int(num))
            clause_1 = -1 * int(int(j)*s*s + int(i)*s + int(num))
    else:
        if row:
            clause_2 = -1 * int(str(i) + str(a) + str(num))
            clause_1 = -1 * int(str(i) + str(j) + str(num))
        else:
            clause_2 = -1 * int(str(a) + str(i) + str(num))
            clause_1 = -1 * int(str(j) + str(i) + str(num))
        
    return [(clause_1, clause_2)]#[clause_1, clause_2]

def constraint_box(i,j,a,d,num,sixteen):
    if sixteen:
        clause_1 = -1 * int(i)*17*17+ int(j)*17 + int(num)
        clause_2 = -1 * int(a)*17*17+ int(d)*17 + int(num)
    else:
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
    sixteen = False

    '''
    Defining Rows, Cols and Values of Sudoku Board
    '''
    numbers = [str(i) for i in range(1, n + 1)]
    Rows = numbers
    Cols = numbers
    Values = numbers

    if len(Values) == 15:
        sixteen = True
    

    Subgrids =[]
    for i in range(block):
        for j in range(block):
            Subgrids += [[(int(Rows[block*i+k]),int(Cols[block*j+l])) for k in range(block) for l in range(block)]]

    with open(out_file, "w") as f:
            
        for r in Rows:
            for c in Cols:
                for v in Values:
                    if sixteen:
                        a = int(r)*17*17 + int(c)*17 + int(v)                   
                    else:
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
                                    z = constraint_box(i,j,a,d,curr_num,sixteen)
                                    for dd, s in z:
                                        if dd == s:
                                            continue
                                        else:
                                            f.write(f"{dd} ")
                                            f.write(f"{s} ")
                                            f.write("0\n")
                                            clauses_number += 1
                                else:
                                    for v in Values:
                                        z = constraint_box(i,j,a,d, v,sixteen)
                                        for dd, s in z:
                                            if dd == s:
                                                continue
                                            else:
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
                    if a != j and curr_num != 0:
                        z = constraint(a, j, i,curr_num, True,sixteen)
                        for c, d in z:
                            if c == d:
                                continue
                            else:
                                f.write(f"{c} ")
                                f.write(f"{d} ")
                                f.write("0\n")
                                clauses_number += 1
                    elif a != j & curr_num == 0:
                        for v in Values:
                            z = constraint(a, j, i, v, True,sixteen)
                            for c, d in z:
                                if c == d:
                                    continue
                                else:
                                    f.write(f"{c} ")
                                    f.write(f"{d} ")
                                    f.write("0\n")
                                    clauses_number += 1
                    else:
                        continue
                       
                #Column
                for b in range(1, n+1):
                    if b != j & curr_num != 0:
                        z = constraint(b, i, j,curr_num, False,sixteen)
                        for c, d in z:
                            if c == d:
                                continue
                            else:
                                f.write(f"{c} ")
                                f.write(f"{d} ")
                                f.write("0\n")
                                clauses_number += 1
                    elif b != j & curr_num == 0:
                        for v in Values:
                            z = constraint(b,i,j, v, False,sixteen)
                            for c, d in z:
                                if c == d:
                                    continue
                                else:
                                    f.write(f"{c} ")
                                    f.write(f"{d} ")
                                    f.write("0\n")
                                    clauses_number += 1
                    else:
                        continue

    nn_bits= n*n*num_of_bits
    sol = dupe(out_file,nn_bits)
    return sol

def dupe(out_file, n):
    lines_set = open(out_file, 'r').readlines()

    lines_set = set(lines_set)
    lines_set = sorted(lines_set,reverse = True)

    out  = open(out_file, 'w')
    for line in lines_set:
        out.write(line)
    
    out.close()

    insert(out_file, f"p cnf {n} {len(lines_set)}")

    print('fini')


def main():
    out_file = "out_sudoku3.cnf"
    sudoku_in = read_sudoku_from_file(out_file)

    #n = make_cnf_dimacs(sudoku_in, out_file)
    #dupe(out_file, n)
    print(sudoku_in,"kkkkk")


if __name__ == "__main__":
    main()

    #python3 SAT.py sudoku/test.txt
