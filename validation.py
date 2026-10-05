from functions import *

"""
take these from section 4 from salmon brief
"""
# benchmark data
depth = ...
tau = ...
T_deep = ...

""" 
take these from Check in #1 parameter table
"""
specific_heat = ...
density = ...

"""
check their equations from Check in #1 parameter table
"""
a = ...
b = ...

t_benchmark, T_benchmark, solar_interp = load_benchmark_data("benchmark_pen.csv")
T_0 = T_benchmark[0]

T_model = solve_temperature_ode(t_benchmark, solar_interp, a, b, T_deep, T_0 = T_0)

def plot_data():
    fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

    ax.scatter(t_benchmark, T_benchmark, color = "r", label = "Benchmark Plot")
    ax.plot(t_benchmark, T_model, "--" , color="b", label = "Numerical Plot")
    ax.set_xlabel("t")
    ax.set_ylabel("T")

    plt.title("Benchmark vs Numerical Solution using benchmark parameters")
    ax.legend()

    plt.tight_layout()
    plt.show()

plot_data()
