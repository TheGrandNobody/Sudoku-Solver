# list of every possible value (111 tot 999)

"""

function DP-SAT(Φ)
   repeat
       // unit propagation:
       while Φ contains a unit clause {l} do
           Φ ← remove-from-formula({l}, Φ);
           for every clause c in Φ that contains ¬l do
              Φ ← remove-from-formula(c, Φ);
              Φ ← add-to-formula(c \ {¬l}, Φ);
       // eliminate clauses not in normal form:
       for every clause c in Φ that contains both a literal l and its negation ¬l do
           Φ ← remove-from-formula(c, Φ);
       // pure literal elimination:
       while there is a literal l that occurs pure in Φ do
           for every clause c in Φ that contains l do
              Φ ← remove-from-formula(c, Φ);
       // stopping conditions:
       if Φ is empty then
           return true;
       if Φ contains an empty clause then
           return false;
       // Davis-Putnam procedure:
       pick a literal l that occurs with both polarities in Φ
       for every clause c in Φ containing l and every clause n in Φ containing its negation ¬l do
           // resolve c with n:
           r ← (c \ {l}) ∪ (n \ {¬l});
           Φ ← add-to-formula(r, Φ);
       for every clause c that contains l or ¬l do
           Φ ← remove-from-formula(c, Φ);        

"""

sudoku_size = 4
sudoku_file = "/root/KR/Sudoku-Solver/sudokus/sudoku1.cnf"

var_list = []

for i in range(1,sudoku_size + 1):
    for j in range(1, sudoku_size + 1):
        for k in range(1, sudoku_size +1):
            var_list.append(int(str(i)+str(j)+str(k)))

print(var_list)

class Clause:
    def __init__(self, clause):
        self.clause = clause
    
    def getLen(self):
        return len(self.clause)
    
    def getInt(self):
        intset = set()
        for value in self.clause:
            intset.add(int(value))
        return(intset)
    
    def getString(self):
        strclause = ""
        for value in self.clause:
            strclause += str(value)
        # print(strclause)
        return strclause

class Sat:
    def __init__(self, clauses):
        self.clauses = clauses
    

    def findUnitClauses(self):
        unit_clauses = set()

        for clause in self.clauses:
            if clause.getLen() == 1:
                unit_clauses.add(int(clause.getString()))
                # clause.getString()
        
        if unit_clauses == set():
            return None
        else:
            return unit_clauses


    def removeUnits(self, units):
        for clause in self.clauses:
            if clause.getInt().intersection(units) is not set():
                hoi = clause.getInt()
                self.clauses.remove(clause)
                print(hoi, units, hoi.intersection(units))

    
    

                

clauses = []
clausobj = []

with open(sudoku_file, "r") as f:
    next(f)
    for line in f:
        line = line.strip(" 0\n")
        line = set(line.split(" "))
        clauses.append(line)
        clause = Clause(line)
        clausobj.append(clause)
        sat = Sat(clausobj)



# print(clausobj)

# print(sat.clauses)

# print(clauses)

units = sat.findUnitClauses()
sat.removeUnits(units)

def DPLL(sudoku):
    unit_clauses = set()

    for clause in sudoku:
        if len(clause) == 3:
            unit_clauses.add(clause)
            sudoku.remove(clause)
        
        unit_clauses.difference_update(clause)
    

    print("sudokuuu", sudoku)

    

    
    print(unit_clauses)
            


# DPLL(clauses)







