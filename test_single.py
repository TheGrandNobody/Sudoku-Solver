from operator import itemgetter
import solver
import sys


if __name__ == "__main__":
    dpll = solver.DPLL()
    dpll.find_solution(sys.argv[1],sys.argv[2])
    solution_values = [k if v else "-" + k for k, v in sorted({k: dpll.solution[k] for k in sorted(dpll.solution)}.items(), key=itemgetter(1), reverse = True)]
    out_file = "output.txt"
    out  = open(out_file, 'w')
    out.write(f"p cnf {len(solution_values)} {len(solution_values)} \n")
    for b in solution_values:
        out.write(f"{b} ")
        out.write("0\n")

    #example: python3 test.py sudoku/sudoku2.cnf 1
    
    # 0 for basic
    # 1 for Jeroslow Wang
    # 2 for VSIDS
