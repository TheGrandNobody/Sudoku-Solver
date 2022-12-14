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
        # Chosen heuristic
        self.chosen_h = 0
        # Counts the number of splits
        self.split_counter = 0
        # Counts variable occurences
        self.var_counter = {}
        # Whether the initial occurences counts are made yet
        self.exists_var_counter = False


    def find_solution(self, path: str, option: str) -> bool:
        """ Attempts to find a solution for a given SAT problem.

        Args:
            path (str): The path to the .cnf file which must be solved.


        Returns:
            bool: Returns True if a solution is found else False.
        """
        self.path = path
        # Open the .cnf file and load each line into a list
        with open(path, 'r') as f:
            lines = [line[:-3].rstrip() for line in f.readlines() if 'p' not in line]
        
        self.chosen_h = int(option) # Chosen heuristic
        # Begin solving the problem, we can ignore the initial first line.
        return self.solve(lines, [], {}, False, None)

    def solve(self, kb: List, remaining: List, assignments: Dict, split: bool, value: bool) -> bool:
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
            # New split
            self.split_counter += 1
            if self.chosen_h == 0:
                variable = remaining.pop()
            elif self.chosen_h == 1:
                variable = self.two_jw(kb)
                remaining.remove(variable)
            elif self.chosen_h == 2:
                variable = self.vsids(remaining, kb)
                remaining.remove(variable)
            assignments[variable] = value
            if not value:
                variable = '-'+variable if '-' not in variable else variable[1:]
            anti = variable[1:] if '-' in variable else f'-{variable}'
            kb = [c if anti not in c else format(c.replace(anti, '')) for c in kb if variable not in c or (anti in c and ('-' in anti or variable not in c))] 
        # Apply the unit clause rule
        kb, remaining, assignments = self.unit_propagate(kb, remaining, assignments)

        # Apply the pure literal rule
        kb, remaining, assignments = self.pure_literal(kb, remaining, assignments)
        # Check whether the KB is empty
        if self.kb_empty(kb):
            print("SAT ", self.path)
            self.solution = assignments
            return True
        # Check whether there are any empty clauses
        if self.empty_clauses(kb):
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
            other (str): An other specified variable in case we do not want to remove the actual assigned variable.
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

    def unit_propagate(self, kb: List, remaining: List, assignments: Dict) -> None:
        """ Updates the list of clauses based on the unit propagation rule.

        Args:
            kb (List): The knowledge base (all of the clauses).
            remaining (List): The remaining unassigned variables.
            assignments (Dict): The assigned variables and their assigned values.
        """
        def unit(clause: str) -> bool:
            """ Updates the list of literals for a given clause, if it is a unit clause.
                Builds a list of unassigned variables if this is the algorithm's first iteration.

            Args:
                clause (str): The specified clause. 

            Returns:
                bool: True if a unit clause was found, else false.
            """
            nonlocal kb
            split_clause = clause.split(" ")
            # Compute the negation of the clause
            anti = clause[1:] if '-' in clause else f'-{clause}'
            if len(split_clause) == 1 and (clause in remaining or anti in remaining or self.start):
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
        while any(list(map(unit, copy.deepcopy(kb)))):
            if self.start:
                self.start = False
            pass
        return kb, remaining, assignments
        
    def pure_literal(self, kb: List, remaining: List, assignments: Dict) -> None:
        """ Assigns a true or false value to all pure literals

        Args:
            kb (List): The knowledge base (all of the clauses).
            remaining (List): The remaining unassigned variables.
            assignments (Dict): The assigned variables and their assigned values.
        """
        def verify_pure(variable: str) -> bool:
            """ Verifies and handles a given unassigned variable on the basis of whether it is a pure literal.

            Args:
                variable (str): The specified variable.
            
            Returns:
                bool: True if a puire literal was found else false.
            """
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
                    if positive > 0 and negative > 0:
                        break
            is_pure = not (negative > 0 and positive > 0) and (negative or positive)
            # Assign the literal a truth value and remove all clauses containing it.
            if is_pure:
                normal = (positive > 0 and '-' not in variable) or (negative > 0 and '-' in variable)
                actual = variable if normal else '-'+variable if negative > 0 else variable[1:]
                self.assign(remaining, assignments, actual, variable)
                anti = actual[1:] if '-' in actual else f'-{actual}'
                kb = [c if anti not in c else format(c.replace(anti, '')) for c in kb if actual not in c or (anti in c and ('-' in anti or actual not in c))] 
            return is_pure
        while any(list(map(verify_pure, copy.deepcopy(remaining)))):
            pass
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


    def two_jw(self, kb: List) -> str:
        """ Determines what variable to trackback to

        Args:
            kb (List): The knowledge base (all of the clauses).
            remaning: The remaining variables

        Returns:
            str: The variable with the highest value according two TS-JW
        """
        all_lit = {}
        for clause in kb:
            clause = clause.replace('-',"")
            a = clause.split(" ")
            for literal in a:
                leng = 2**-len(a)
                if literal in all_lit:
                    all_lit[literal] += leng 
                else:
                    all_lit.update({literal:leng})
        b = max(all_lit, key=all_lit.get)
        return b

    def vsids(self, remaining: List, kb: List) -> str:
        """ Determines what variable to trackback to for VSIDS

        Args:
            remaining (List): The remaining variables.
            kb (List): The knowledge base (all of the clauses) 

        Returns:
            str: The variable with the highest value according to VSIDS
        """
        if self.exists_var_counter == False:
            # Count variable occurences
            for clause in kb:
                clause = clause.split(' ')
                for variable in clause:
                    if variable[0] == '-':
                        variable = variable[1:]
                    if variable not in self.var_counter:
                        self.var_counter[variable] = 0
                    self.var_counter[variable] += 1.0
            self.exists_var_counter = True
        else:
            # Periodically decay by 5%
            self.var_counter = {key: value * 0.95 for key, value in self.var_counter.items()}
        
        sorted_counter = sorted(self.var_counter.items(), key=lambda x:x[1])

        # Choose variable to assign, if already assigned
        to_assign = sorted_counter.pop()[0]
        while to_assign not in remaining:
            to_assign = sorted_counter.pop()[0]
        
        return to_assign