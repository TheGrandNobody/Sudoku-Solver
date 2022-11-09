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
    
  def solve(self) -> bool:
      """ Solves the .cnf file this solver was given.

      Args:
          path (str): The path to the .cnf file holding the sudoku and its rules in DIMACS format.
      
      Returns:
          bool: Whether a solution was found or not 
      """
      # Apply the unit clause rule
      self.unit_propagate()
      if self.start:
          self.start = False
      # Apply the pure literal rule
      self.pure_literal()
      # Check whether the KB is empty
      if self.kb_empty():
          print("SAT")
          return True
      # Check whether there are any empty clauses
      if self.empty_clauses():
          print("UNSAT")
          return False
      # Choose a literal
      # Save the state
      # Call this function recursively
      # ???
      # Profit
      # Cry because DPLL sucks

      

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

  def unit_propagate(self) -> None:
      """ Updates the list of clauses based on the unit propagation rule.
      """
      def unit(clause: str) -> None:
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
              self.clauses = [c for c in self.clauses if clause not in c]  
              return
          if self.start:
              # Update the list of unassigned variables for the algorithm's first iteration
              def update(variable) -> None:
                  if variable not in self.remaining and variable not in self.assignments:
                      self.remaining.append(variable)
              map(update, split_clause)
      map(unit, copy.deepcopy(self.clauses))
  
  def pure_literal(self) -> None:
      """ Assigns a true or false value to all pure literals
      """
      def verify_pure(variable: str):
          """ Verifies and handles a given unassigned variable on the basis of whether it is a pure literal.

          Args:
              variable (str): The specified variable
          """
          positive, negative = 0, 0
          # Check that the variable is either only positive or negative in all of the clauses it appears in.
          for clause in self.clauses:
              result = clause.find(variable)
              if result != -1:
                  if result == 0 or clause[result - 1] != '-':
                      positive += 1
                  else: 
                      negative += 1
          is_pure = not (negative > 1 and positive > 1)
          # Assign the literal a truth value and remove all clauses containing it.
          if is_pure:
              self.assign(variable)
              self.clauses = [c for c in self.clauses if variable not in c]
      map(verify_pure, self.remaining)

  def kb_empty(self):
      return len(self.clauses) == 0
    
  def empty_clauses(self):
      return any(len(clause) == 0 for clause in self.clauses)
        

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