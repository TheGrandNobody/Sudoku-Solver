import copy
from typing import List
from collections import defaultdict

class DPLL():
  """Implements the DPLL solver class.
  """
  def __init__(self, path: str) -> None:
      """ Initializes a DPLL solver.

      Args:
          path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
      """
      with open(path, 'r') as f:
          lines = "".join(f.readlines()).split(' 0\n')[:-1]
      self.clauses = lines[1:]
      self.literals = defaultdict(lambda: None)
    
  def solve(self) -> None:
      """ Solves the .cnf file this solver was given.

      Args:
          path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
      """
      self.last = copy.deepcopy(self.clauses)
      self.unit_propagate()

    
  def unit(self, clause: str) -> str:
      """ Updates the list of literals for a given clause, if it is a unit clause.

      Args:
          clause (str): The specified clause. 

      Returns:
          str: A unit clause.
      """
      if len(clause.split(" ")) == 1:
          # Set the literal to true/false if it is a unit clause
          self.literals[int(clause)] = '-' not in clause
          # Return the close to store it in a list
          return clause

  def is_unit(self, clause: str, units: List) -> bool:
      def check(unit):
          return unit in clause
      return False in list(map(check, units))

  def unit_propagate(self) -> None:
      """ Updates the list of clauses based on the unit propagation rule.
      """
      units = list(map(self.unit, self.clauses))
      self.clauses = [c for c in self.clauses if self.is_unit(c, units)]
  
  def pure_literal(self) -> None:
      """_summary_
      """
      
    
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