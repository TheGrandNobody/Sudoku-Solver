# Sudoku-Solver
This repository implements a sudoku solver using a Davis-Putnam (DPLL) algorithm, as well as two improved variations using a Jeroslow-Wang and a Variable State Independent Decaying Sum (VSIDS) heuristic.

## Usage
To use the SAT solver, run the following:
```
python3 test.py path_to_sudoku heuristic_number
```
The CNF file of the solution to the Sudoku, in DIMACS format, will be written to an "output.txt" file.
The following numbers correspond to the heuristics:

0: DPLL basic

1: Jeroslow-Wang

2: VSIDS

Note:
The sudoku should be in DIMACS format.
To encode the sudoku in DIMACS, run the following:
```
python3 SAT.py input_sudoku_file.txt
```