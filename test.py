from operator import itemgetter
import solver
import sys


if __name__ == "__main__":
    dpll = solver.DPLL()
    dpll.find_solution(sys.argv[1])
    print({k: v for k,v in sorted({k: dpll.solution[k] for k in sorted(dpll.solution)}.items(), key=itemgetter(1))})