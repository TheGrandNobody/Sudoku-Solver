import sys
from collections import defaultdict

class DPLL():
  """Implements the DPLL solver class.
  """
  def __init__(self, path: str) -> None:
    """ Initializes a DPLL solver.

    Args:
        path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
    """
    self.solve(path)

  def solve(self, path) -> None:
    """ Solves the .cnf file this solver was given.

    Args:
        path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
    """
    with open(path, 'r') as f:
        lines = "".join(f.readlines()).split(' 0\n')[:-1]
    self.clauses = lines[1:]
    self.variables = defaultdict(lambda: None)
  
  def propagate(self, clause):
      self.variables[int(clause)] = True
      return clause

  def unit_propagate(self):
      self.clauses = [self.propagate(c) for c in self.clauses if len(c.split(" ")) > 1]   
    
  def is_empty(self):
      if len(self.clauses) == 0:
          return True
    
  def empty_clauses(self):
      if any(len(clause) == 0 for clause in self.clauses):
          return False
        



"""
function DPLL(Φ)
    while there is a unit clause {l} in Φ do
        Φ ← unit-propagate(l, Φ);
    while there is a literal l that occurs pure in Φ do
        Φ ← pure-literal-assign(l, Φ);
    if Φ is empty then
        return true;
    if Φ contains an empty clause then
        return false;
    l ← choose-literal(Φ);
    return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {not(l)});
"""