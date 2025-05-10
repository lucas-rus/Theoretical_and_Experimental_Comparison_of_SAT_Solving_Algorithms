import random
import time
import csv
import matplotlib.pyplot as plt
import tracemalloc
from pysat.solvers import Glucose3
from tqdm import tqdm

# === CNF Clause Generation ===
def generate_clause_set(num_vars, num_clauses, clause_len_range=(3, 5)):
    clause_set = []
    for _ in range(num_clauses):
        clause_len = random.randint(*clause_len_range)
        clause = set()
        while len(clause) < clause_len:
            var = random.randint(1, num_vars)
            lit = var if random.choice([True, False]) else -var
            clause.add(lit)
        clause_set.append(list(clause))
    return clause_set

# === SAT Solvers ===
def resolution_solver(clauses):
    clauses = [frozenset(c) for c in clauses]
    new = set()
    seen = set(clauses)

    def resolve(ci, cj):
        resolvents = []
        for lit in ci:
            if -lit in cj:
                res = (ci - {lit}) | (cj - {-lit})
                if not res:
                    return [frozenset()]
                resolvents.append(frozenset(res))
        return resolvents

    while True:
        pairs = [(ci, cj) for i, ci in enumerate(clauses) for j, cj in enumerate(clauses) if i < j]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for r in resolvents:
                if not r:
                    return False
                if r not in seen:
                    new.add(r)
                    seen.add(r)
            if len(seen) > 1000:
                return None  # Safety abort
        if new.issubset(seen):
            return True
        clauses.extend(new)
        new.clear()

def dp_solver(clauses, num_vars):
    def dp(cnf, vars_left):
        if not cnf:
            return True
        if [] in cnf:
            return False
        if not vars_left:
            return True
        v = vars_left[0]
        new_vars = vars_left[1:]
        for val in [v, -v]:
            new_cnf = []
            for clause in cnf:
                if val in clause:
                    continue
                new_clause = [lit for lit in clause if lit != -val]
                new_cnf.append(new_clause)
            if dp(new_cnf, new_vars):
                return True
        return False
    return dp(clauses, list(range(1, num_vars + 1)))

def dpll_solver(clauses, assignments=[]):
    def unit_propagate(cnf):
        changed = True
        assignment = []
        while changed:
            changed = False
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if not unit_clauses:
                break
            for unit in unit_clauses:
                assignment.append(unit)
                new_cnf = []
                for clause in cnf:
                    if unit in clause:
                        continue
                    new_clause = [l for l in clause if l != -unit]
                    if new_clause == clause:
                        continue
                    new_cnf.append(new_clause)
                cnf = new_cnf
                changed = True
        return cnf, assignment

    cnf = [clause[:] for clause in clauses]
    cnf, unit_assignments = unit_propagate(cnf)
    assignments = assignments + unit_assignments
    if [] in cnf:
        return False
    if not cnf:
        return True
    variable = abs(cnf[0][0])
    for val in [variable, -variable]:
        new_cnf = []
        for clause in cnf:
            if val in clause:
                continue
            new_clause = [l for l in clause if l != -val]
            new_cnf.append(new_clause)
        if dpll_solver(new_cnf, assignments + [val]):
            return True
    return False

def glucose_solver(clauses):
    with Glucose3(bootstrap_with=clauses) as solver:
        return solver.solve()

# === Benchmarking ===
def benchmark_solver(solver_func, *args):
    tracemalloc.start()
    start = time.time()
    result = solver_func(*args)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, end - start, peak / 1024  # Return peak in KB

def run_benchmarks():
    all_times = {"Resolution": 0, "DP": 0, "DPLL": 0, "Glucose3": 0}
    all_memory = {"Resolution": 0, "DP": 0, "DPLL": 0, "Glucose3": 0}

    with open("sat_solver_benchmarks.csv", "w", newline="") as csvfile:
        fieldnames = ["Set", "Solver", "Result", "Time(s)", "Memory(KB)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        set_id = 1
        for num_vars in range(10, 55, 5):
            for num_clauses in range(30, 170, 10):
                clause_set = generate_clause_set(num_vars, num_clauses, clause_len_range=(3, 5))

                print(f"\nSet {set_id} (Vars: {num_vars}, Clauses: {num_clauses}):")

                for name, solver in [
                    ("Resolution", resolution_solver),
                    ("DP", dp_solver),
                    ("DPLL", dpll_solver),
                    ("Glucose3", glucose_solver)
                ]:
                    try:
                        if name == "DP":
                            result, t, mem = benchmark_solver(solver, clause_set, num_vars)
                        else:
                            result, t, mem = benchmark_solver(solver, clause_set)
                        print(f"  {name:10} | Result: {result} | Time: {t:.6f}s | Memory: {mem:.2f}KB")
                        writer.writerow({"Set": set_id, "Solver": name, "Result": result, "Time(s)": round(t, 6), "Memory(KB)": round(mem, 2)})
                        if t is not None:
                            all_times[name] += t
                            all_memory[name] += mem
                    except Exception as e:
                        print(f"  {name:10} | ERROR: {e}")
                        writer.writerow({"Set": set_id, "Solver": name, "Result": "ERROR", "Time(s)": "N/A", "Memory(KB)": "N/A"})
                set_id += 1

    # --- Plot Pie Chart ---
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.pie(all_times.values(), labels=all_times.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Relative Runtime of SAT Solvers")

    plt.subplot(1, 2, 2)
    plt.pie(all_memory.values(), labels=all_memory.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Relative Peak Memory Usage (KB)")

    plt.tight_layout()
    plt.savefig("solver_runtime_memory_piechart.png")
    plt.show()

if __name__ == "__main__":
    run_benchmarks()
