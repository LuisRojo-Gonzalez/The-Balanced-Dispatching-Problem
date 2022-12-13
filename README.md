# The Balanced Dispatching Problem

This repository has the scripts developed to the published article in Expert Systems with Applications [The balanced dispatching problem in passengers transport services on demand](https://doi.org/10.1016/j.eswa.2021.114918).

This was my Master's thesis at Universidad de Santiago de Chile!

## Goal

At a glance, we develop a system that aims to balance the income per working time among cab drivers of a certain transportation company. To do this, we use the variance as a metric to be minimized. Certainly, this has to be implemented in a real-time scenario, i.e., online, with near-optimal results.

## Methodology

Thus, we use the following methodology:

1. **Claim the statement of the problem.** Here, we describe the elements involved in the phenomenon to be tackeld in a mathematical way to generalize its use.
2. **Formulate the mathematical model.** As we aim to develop an online algorithm, we formulate the optimization model to know the optimal solution in presence of complete information, and to assess our algorithm's performance thereafter.
3. **Formulate an easy-to-implement algorithm.** We formulate the problem as a rule that classifies the cab drivers and find the most suitable dispatch to the incoming trip to be satisfied. In here, the computational complexity should be revised to show that the problem is NP-complete and therefore no algorithm is able to solve the problem in polynomial time. Thus, we may be able to approximate the solution.
4. **Implementation and results analysis.** We implement the optimization model in C++ and solve it using CPLEX, and the developed online algorithm is implemented in Python for its compatibility with infrastructure often available at organizations. Then, we analyze different instances of the problem looking for patterns and to validate the performance of the algorithm.
