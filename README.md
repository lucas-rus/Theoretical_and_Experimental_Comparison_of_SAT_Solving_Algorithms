# Comparative Analysis of SAT Solving Algorithms

This repository contains the source code and results for the research project **"Comparative Analysis of SAT Solving Algorithms: A Runtime and Memory Benchmarking Study."** The study evaluates the performance of four SAT solving algorithms: Resolution, Davis–Putnam (DP), DPLL, and Glucose3.

## 🧪 Overview

The project includes:
- Implementations of Resolution, DP, and DPLL in Python
- Integration with the Glucose3 solver using the PySAT library
- A benchmarking script that measures runtime and memory usage
- A results file with benchmark data
- A pie chart summarizing solver performance

## 📁 Files

```
SAT_Solving_Benchmark.py     # Main script for benchmarking
SAT_Solving_Results.txt      # Output of runtime and memory benchmarks
solver_piechart.png          # Pie chart visualization of results
README.md                    # Project documentation
```

## ⚙️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lucas-rus/Theoretical_and_Experimental_Comparison_of_SAT_Solving_Algorithms.git
   cd Theoretical_and_Experimental_Comparison_of_SAT_Solving_Algorithms
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages manually:
   ```bash
   pip install psutil matplotlib python-sat[pblib,aiger]
   ```

## 🚀 Usage

To run the benchmark:
```bash
python3 SAT_Solving_Benchmark.py
```

The script will generate:
- `SAT_Solving_Results.txt` – contains detailed runtime and memory usage per solver
- `solver_piechart.png` – visual summary of results

## 📦 Dependencies

- Python 3.8+
- [PySAT](https://pysathq.github.io/)
- [psutil](https://github.com/giampaolo/psutil)
- [matplotlib](https://matplotlib.org/) (for generating the pie chart)

Install them manually using:
```bash
pip install psutil matplotlib python-sat[pblib,aiger]
```

## 📄 License

This project is licensed under the MIT License.
