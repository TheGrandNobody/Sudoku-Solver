from operator import itemgetter
import solver
import sys


if __name__ == "__main__":
    dpll = solver.DPLL()
    dpll.find_solution(sys.argv[1],sys.argv[2])
    #print({k: v for k,v in sorted({k: dpll.solution[k] for k in sorted(dpll.solution)}.items(), key=itemgetter(1))})

    solution_values = [ ]
    for k,v in sorted({k: dpll.solution[k] for k in sorted(dpll.solution)}.items(), key=itemgetter(1), reverse = True):
        if v is False:
            k = "-" + k
        else:
            pass
        solution_values.append(k)
    out_file = "output.txt"
    out  = open(out_file, 'w')
    out.write(f"p cnf {len(solution_values)} {len(solution_values)} \n")
    for b in solution_values:
        out.write(f"{b} ")
        out.write("0\n")
    print('fini')


    #python3 test.py sudoku/sudoku2.cnf 1 sudoku/test.txt
    
    
    
    # 0 for basic
    # 1 for Jeroslow Wang
