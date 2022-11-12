import copy
from typing import List, Dict

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
      # Whether the algorithm has constructed the list of unassigned variables yet
      self.start = True
      # Whether the algorithm found a solution or not
      self.found = False
    
  def solve(self, remaining: List, assignments: Dict, kb: List, split=False, value=None) -> bool:
      """ Solves the .cnf file this solver was given.

      Args:
          remaining (List): The remaining unassigned variables.
          assignments (Dict): The assigned variables and their assigned values.
          kb (List): The knowledge base (all of the clauses).
          split (bool, optional): Whether this is a splitting instance or not. Defaults to False.
          value (_type_, optional): The value of the assigned variable for this splitting instance. Defaults to None.

      Returns:
          bool: Whether a solution was found or not.
      """
      # Apply the split if this is a splitting instance
      if split:
          variable = remaining.pop()
          assignments[variable] = value
          anti = variable[1:] if '-' in variable else f'-{variable}'
          kb = [c for c in kb if variable not in c or anti in c] 
      
      # Apply the unit clause rule
      self.unit_propagate(remaining, assignments, kb)
      if self.start:
          self.start = False
      # Apply the pure literal rule
      self.pure_literal(remaining, assignments, kb)
      # Check whether the KB is empty
      if self.kb_empty(kb):
          print("SAT")
          return True
      # Check whether there are any empty clauses
      if self.empty_clauses(kb):
          print("UNSAT")
          return False
      # Split using a positive value, otherwise backtrack using a negative value
      if self.solve(copy.deepcopy(remaining), copy.deepcopy(assignments), copy.deepcopy(kb), True, True) or \
        self.solve(copy.deepcopy(remaining), copy.deepcopy(assignments), copy.deepcopy(kb), True, False):
          if not self.found:
              self.solution = assignments
              self.found = True
      return self.found

  def assign(self, remaining: List, assignments: Dict, variable: str) -> None:
      """ Assigns a true or false value to a given variable.
          Removes the variable from the unassigned variables list. 

      Args:
          remaining (List): The remaining unassigned variables.
          assignments (Dict): The assigned variables and their assigned values.
          variable (str): The specified variable.
      """
      if '-' in variable:
          assignments[variable[1:]] = False
      else: 
          assignments[variable] = True
      # Remove the variable from the list of unsassigned variables.
      if not self.start:
          remaining.remove(variable)

  def unit_propagate(self, remaining: List, assignments: Dict, kb: List) -> None:
      """ Updates the list of clauses based on the unit propagation rule.

      Args:
          remaining (List): The remaining unassigned variables.
          assignments (Dict): The assigned variables and their assigned values.
          kb (List): The knowledge base (all of the clauses).
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
              self.assign(remaining, assignments, clause)
              # Return the close to store it in a list 
              anti = clause[1:] if '-' in clause else f'-{clause}'
              kb = [c for c in kb if clause not in c or anti in c] 
              return
          if self.start:
              # Update the list of unassigned variables for the algorithm's first iteration
              def update(variable) -> None:
                  anti = variable[1:] if '-' in variable else f'-{variable}'
                  if variable not in remaining and variable not in assignments \
                     and anti not in remaining and anti not in assignments:
                      remaining.append(variable)
              map(update, split_clause)
      map(unit, copy.deepcopy(kb))
  
  def pure_literal(self, remaining: List, assignments: Dict, kb: List) -> None:
      """ Assigns a true or false value to all pure literals

      Args:
          remaining (List): The remaining unassigned variables.
          assignments (Dict): The assigned variables and their assigned values.
          kb (List): The knowledge base (all of the clauses).
      """
      def verify_pure(variable: str) -> None:
          """ Verifies and handles a given unassigned variable on the basis of whether it is a pure literal.

          Args:
              variable (str): The specified variable.
          """
          positive, negative = 0, 0
          # Check that the variable is either only positive or negative in all of the clauses it appears in.
          for clause in kb:
              result = clause.find(variable)
              if result != -1:
                  if result == 0 or clause[result - 1] != '-':
                      positive += 1
                  else: 
                      negative += 1
          is_pure = not (negative > 1 and positive > 1)
          # Assign the literal a truth value and remove all clauses containing it.
          if is_pure:
              self.assign(remaining, assignments, variable)
              anti = clause[1:] if '-' in clause else f'-{clause}'
              kb = [c for c in kb if clause not in c or anti in c] 
      map(verify_pure, remaining)

  def kb_empty(kb: List) -> bool:
      """ Verifies whether a given knowledge base is empty.

      Args:
          kb (List): The knowledge base (all of the clauses).

      Returns:
          bool: True if the knowledge base is empty, else False.
      """
      return len(kb) == 0
    
  def empty_clauses(kb: List) -> bool:
      """ Verifies whether the knowledge base contains any empty clause.

      Args:
          kb (List): The knowledge base (all of the clauses).

      Returns:
          bool: True if an empty clause exists, else False.
      """
      return any(len(clause) == 0 for clause in kb)