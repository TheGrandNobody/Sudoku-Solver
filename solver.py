import copy
from typing import List

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
      # The problem's KB
      self.clauses = lines[1:]
      # The problem's remaining unassigned variables
      self.remaining = []
      # The problem's assigned variables
      self.assignments = {}
      # Whether the algorithm has constructed the list of unassigned variables yet
      self.start = True
    
  def solve(self) -> None:
      """ Solves the .cnf file this solver was given.

      Args:
          path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
      """
      self.last = copy.deepcopy(self.clauses)
      self.unit_propagate()
      if self.start:
          self.start = False

  def assign(self, variable: str) -> None:
      """ Assigns a true or false value to a given variable.
          Removes the variable from the unassigned variables list. 

      Args:
          variable (str): The specified variable.
      """
      if '-' in variable:
          self.assignments[variable[1:]] = False
      else: 
          self.assignments[variable] = True
      # Remove the variable from the list of unsassigned variables.
      if not self.start:
          self.remaining.remove(variable)

  def unit(self, clause: str) -> str:
      """ Updates the list of literals for a given clause, if it is a unit clause.
          Builds a list of unassigned variables if this is the algorithm's first iteration.

      Args:
          clause (str): The specified clause. 

      Returns:
          str: A unit clause.
      """
      split_clause = clause.split(" ")
      if len(split_clause) == 1:
          # Set the literal to true/false if it is a unit clause
          self.assign(clause)
          # Return the close to store it in a list
          return clause
      if self.start:
          # Update the list of unassigned variables for the algorithm's first iteration
          def update(variable) -> None:
              if variable not in self.remaining:
                  self.remaining.append(variable)
          map(update, split_clause)

  def unit_propagate(self) -> None:
      """ Updates the list of clauses based on the unit propagation rule.
      """
      units = list(map(self.unit, self.clauses))
      def is_unit(clause: str) -> bool:
          return True in [unit in clause for unit in units] 
      self.clauses = [c for c in self.clauses if not is_unit(c, units)]
  
  def pure(self, clause: str) -> bool:
      positive, negative = 0, 0
      for c in self.clauses:
          result = c.find(clause)
          if result != -1:
              if result == 0 or c[result - 1] != '-':
                  positive += 1
              else: 
                  negative += 1
      return not (negative > 1 and positive > 1)      
  
  def is_pure(self, clause: str): # No need to check for every c in self.clauses
      if self.pure(clause):
          self.assign
  
  def pure_literal(self) -> None:
      """ Assigns a true or false value to all pure literals
      """
      map(self.is_pure, self.remaining)
      
  def is_empty(self):
      if len(self.clauses) == 0:
          print("SAT")
    
  def empty_clauses(self):
      if any(len(clause) == 0 for clause in self.clauses):
          print("UNSAT")
        



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