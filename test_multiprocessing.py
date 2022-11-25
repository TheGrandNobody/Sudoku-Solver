from solver import DPLL
from multiprocessing import Pool, cpu_count
from time import time
import csv

def solve(dpll: DPLL, path: str,  heuristic: str):
    initial = time()
    dpll.find_solution(f"testset/{path}.cnf", heuristic)
    delta = time() - initial
    data = [heuristic, path, delta, dpll.split_counter]
    return data


if __name__ == "__main__":
    # Parse all sudokus into DIMACS format and count them
    NUM_SUDOKUS = 2000
    # Create a list of DPLL solvers for each sudoku
    solvers = [(DPLL(), f"{i if i < NUM_SUDOKUS else i - NUM_SUDOKUS + 1 if i < NUM_SUDOKUS * 2 else i - (2 * NUM_SUDOKUS) + 1}", "0" if i < NUM_SUDOKUS else "1" if i < NUM_SUDOKUS * 2 else "2") for i in range(1, NUM_SUDOKUS * 3)]
    # Run multiple solvers of different heuristics in parallel until all sudokus are solved
    with Pool(processes=cpu_count()) as pool:
        result = pool.starmap(solve, solvers)

    # Write the results to a csv file
    with open("results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(("Heuristic", "Sudoku", "Time", "Branching Frequency"))
        writer.writerows((line for line in result))
