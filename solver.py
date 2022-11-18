import copy
from typing import List, Dict

def format(string: str) -> str:
    try:
        if string[0] == ' ':
            return string[1:]
        elif string[-1] == ' ':
            return string[:-1]
        else:
            new = []
            prev = None
            for c in string:
                if not (prev == ' ' and c == ' '):
                    new.append(c)
                prev = c
            return "".join(new)
    except:
        return string
                
class DPLL():
  """Implements the DPLL solver class.
  """
  def __init__(self) -> None:
      """ Initializes a DPLL solver.
      """
      # Whether the algorithm has constructed the list of unassigned variables yet
      self.start = True
      # The solution that the algorithm found
      self.solution = None


  def find_solution(self, path: str) -> bool:
      """ Attempts to find a solution for a given SAT problem.

      Args:
          path (str): The path to the .cnf file which must be solved.

      Returns:
          bool: Returns True if a solution is found else False.
      """
      # Open the .cnf file and load each line into a list
      with open(path, 'r') as f:
          lines = [line[:-3].rstrip() for line in f.readlines() if 'p' not in line]
      # Begin solving the problem, we can ignore the initial first line.
      return self.solve(lines)
    
  def solve(self, kb, remaining=[], assignments={}, split=False, value=None) -> bool:
      """ Solves the .cnf file this solver was given.

      Args:
          kb (List): The knowledge base (all of the clauses).
          remaining (List): The remaining unassigned variables.
          assignments (Dict): The assigned variables and their assigned values.
          split (bool, optional): Whether this is a splitting instance or not. Defaults to False.
          value (_type_, optional): The value of the assigned variable for this splitting instance. Defaults to None.

      Returns:
          bool: Whether a solution was found or not.
      """
      # Apply the split if this is a splitting instance
      if split:
          variable = remaining.pop()
          assignments[variable] = value
          if not value:
              variable = '-'+variable if '-' not in variable else variable[1:]
          anti = variable[1:] if '-' in variable else f'-{variable}'
          kb = [c if anti not in c else format(c.replace(anti, '')) for c in kb if variable not in c or (anti in c and ('-' in anti or variable not in c))] 
      # Apply the unit clause rule
      kb, remaining, assignments = self.unit_propagate(remaining, assignments, kb)
      if self.start:
          self.start = False
      # Apply the pure literal rule
      kb, remaining, assignments = self.pure_literal(remaining, assignments, kb)
      # Check whether the KB is empty
      if self.kb_empty(kb):
          print("SAT")
          self.solution = assignments
          return True
      # Check whether there are any empty clauses
      if self.empty_clauses(kb):
          print("UNSAT")
          return False
      # Split using a positive value, otherwise backtrack using a negative value
      return self.solve(copy.deepcopy(kb), copy.deepcopy(remaining), copy.deepcopy(assignments), True, False) or \
        self.solve(copy.deepcopy(kb), copy.deepcopy(remaining), copy.deepcopy(assignments), True, True)

  def assign(self, remaining: List, assignments: Dict, variable: str, other: str) -> None:
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
          if variable in remaining:
              remaining.remove(variable)
          else:
              remaining.remove(other)

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
          nonlocal kb
          nonlocal remaining
          nonlocal assignments
          split_clause = clause.split(" ")
          # Compute the negation of the clause
          anti = clause[1:] if '-' in clause else f'-{clause}'
          if len(split_clause) == 1 and (clause in remaining or anti in remaining):
              # Set the literal to true/false if it is a unit clause
              self.assign(remaining, assignments, clause, anti)
              # Return the clause to store it in a list 
              kb = [c if anti not in c else format(c.replace(anti, '')) for c in kb if clause not in c or (anti in c and ('-' in anti or clause not in c))] 
              return True
          if self.start:
              # Update the list of unassigned variables for the algorithm's first iteration
              def update(variable) -> None:
                  anti = variable[1:] if '-' in variable else f'-{variable}'
                  if variable not in remaining and variable not in assignments \
                     and anti not in remaining and anti not in assignments:
                      remaining.append(variable)
              [update(s) for s in split_clause]
          return False
      
      [unit(c) for c in copy.deepcopy(kb)]
      found = True
      while found:
          found = False
          for c in copy.deepcopy(kb):
              any = unit(c)
              if any:
                  found = True
      return kb, remaining, assignments
      
  
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
          nonlocal remaining
          nonlocal assignments
          nonlocal kb
          positive, negative = 0, 0
          # Check that the variable is either only positive or negative in all of the clauses it appears in.
          for clause in kb:
              result = clause.find(variable)
              if result != -1:
                  if result == 0 or clause[result - 1] != '-':
                      positive += 1
                  else: 
                      negative += 1
          is_pure = not (negative > 0 and positive > 0) and (negative or positive)
          # Assign the literal a truth value and remove all clauses containing it.
          if is_pure:
              normal = (positive > 0 and '-' not in variable) or (negative > 0 and '-' in variable)
              actual = variable if normal else '-'+variable if negative > 0 else variable[1:]
              self.assign(remaining, assignments, actual, variable)
              anti = actual[1:] if '-' in actual else f'-{actual}'
              kb = [c if anti not in c else format(c.replace(anti, '')) for c in kb if actual not in c or (anti in c and ('-' in anti or actual not in c))] 
      [verify_pure(r) for r in copy.deepcopy(remaining)]
      return kb, remaining, assignments

  def kb_empty(self, kb: List) -> bool:
      """ Verifies whether a given knowledge base is empty.

      Args:
          kb (List): The knowledge base (all of the clauses).

      Returns:
          bool: True if the knowledge base is empty, else False.
      """
      return len(kb) == 0
    
  def empty_clauses(self, kb: List) -> bool:
      """ Verifies whether the knowledge base contains any empty clause.

      Args:
          kb (List): The knowledge base (all of the clauses).

      Returns:
          bool: True if an empty clause exists, else False.
      """
      return any(len(clause) == 0 for clause in kb)