# Comparative Analysis of SAT Solver Algorithms

This repository contains the implementation and benchmarking framework for the research paper "Comparative Analysis of SAT Solver Algorithms: A Runtime and Memory Benchmarking Study" submitted for the MPI course (2025).

## Overview

This project provides a comprehensive performance evaluation of four prominent Boolean satisfiability (SAT) solving algorithms:
- Resolution
- Davis-Putnam (DP)
- Davis-Putnam-Logemann-Loveland (DPLL)
- Glucose3 (via PySAT)

The evaluation focuses on runtime efficiency and memory consumption across systematically generated random SAT instances with varying numbers of variables and clauses.

## Repository Structure

- `/src` - Contains all source code for the project
  - `sat_solvers.py` - Implementation of the Resolution, DP, and DPLL algorithms
  - `glucose_wrapper.py` - Interface to the Glucose3 solver via PySAT
  - `cnf_generator.py` - Random SAT instance generator
  - `benchmark_framework.py` - Tools for measuring runtime and memory usage
  - `visualizer.py` - Code for generating performance visualization graphs
  - `main.py` - Main benchmarking script

- `/data` - Contains the experimental results
  - `benchmark_results.csv` - Raw performance measurements
  - `benchmark_summary.json` - Aggregated statistics

- `/visualizations` - Contains generated graphs and charts
  - `runtime_comparison.png` - Comparative runtime analysis
  - `memory_usage.png` - Memory consumption analysis
  - `scaling_behavior.png` - Performance scaling with problem size

- `/paper` - Contains the LaTeX source and PDF of the research paper

## Setup and Usage

### Requirements
- Python 3.8 or higher
- PySAT library for Glucose3
- numpy, matplotlib for data processing and visualization
- tracemalloc for memory tracking

### Installation
```bash
# Clone the repository
git clone https://github.com/lucas-rus/Theoretical_and_Experimental_Comparison_of_SAT_Solving_Algorithms.git

# Install dependencies
pip install python-sat numpy matplotlib
```

### Running the Benchmarks
```bash
# Run the complete benchmark suite
python src/main.py

# Run with specific parameters
python src/main.py --min-vars 10 --max-vars 50 --step-vars 5 --min-clauses 30 --max-clauses 160 --step-clauses 10
```

### Visualizing Results
```bash
# Generate all visualizations from benchmark results
python src/visualizer.py --input data/benchmark_results.csv --output visualizations/

# Generate specific visualization
python src/visualizer.py --input data/benchmark_results.csv --type runtime --output visualizations/runtime_comparison.png
```

## Key Features

1. **Modular Implementation**: Clear separation between solver algorithms, benchmarking framework, and visualization tools
2. **Systematic Benchmarking**: Evaluates performance across a range of problem sizes
3. **Dual Metrics**: Measures both runtime and memory consumption
4. **Safety Mechanisms**: Includes timeout and memory limits to handle exponential behavior

## Experiment Design

The benchmark framework generates random SAT instances with the following parameters:
- Number of variables: 10 to 50 (in increments of 5)
- Number of clauses: 30 to 160 (in increments of 10)
- Clause length: 3 to 5 literals per clause

For each algorithm and problem instance, both execution time and peak memory consumption are measured, with results saved to CSV for further analysis.

## Results

The experimental results demonstrate significant performance disparities among the algorithms:
- Glucose3 consistently outperforms all other algorithms in both time and space efficiency
- Resolution exhibits the highest memory requirements
- DP algorithm shows poor scaling behavior with occasional exponential runtime spikes
- DPLL offers reliable performance across problem sizes

## Author

Lucas-Michael Rus-Gheorghiu  
Department of Computer Science  
West University Timișoara  
lucas.rus05@e-uvt.ro

## License

This project is licensed under the MIT License - see the LICENSE file for details.
