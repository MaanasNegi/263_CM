from functions import *

"""
take these from section 4 from salmon brief
"""
# benchmark data
depth = ... 
tau = ...
T_deep = ...
g = ...
heat_threshold = ...
harvest = lambda t: 0 
smolt_stocking = lambda t: 0 
mortality = ...

""" 
take these from Check in #1 parameter table
"""
specific_heat = ...
density = ...

"""
check their equations from Salmon sounds check-in and callibration pdf
"""
a = 1 / ...
b = 1 / ...

t_benchmark, T_benchmark, solar_interp, mass_benchmark = load_benchmark_data("benchmark_pen.csv")

T_0 = T_benchmark[0]
B_0 = mass_benchmark[0]

T_model = solve_temperature_ode(t_benchmark, solar_interp, a, b, T_deep, T_0 = T_0)
T = interp1d(t_benchmark, T_model)
B_model = solve_biomass_ode(t_benchmark, g, T, mortality, heat_threshold, harvest, smolt_stocking, B_0 = B_0)

def plot_temp_data():
    fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

    ax.scatter(t_benchmark, T_benchmark, color = "r", label = "Benchmark Plot")
    ax.plot(t_benchmark, T_model, "--" , color="b", label = "Numerical Plot")
    ax.set_xlabel("t")
    ax.set_ylabel("T")

    plt.title("Benchmark vs Numerical Solution of Temperature ODE using benchmark parameters")
    ax.legend()

    plt.tight_layout()
    plt.show()

def plot_mass_data():
    fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

    ax.scatter(t_benchmark, mass_benchmark, color = "r", label = "Benchmark Plot")
    ax.plot(t_benchmark, B_model, "--" , color="b", label = "Numerical Plot")
    ax.set_xlabel("t")
    ax.set_ylabel("B")

    plt.title("Benchmark vs Numerical Solution of Biomass ODE using benchmark parameters")
    ax.legend()

    plt.tight_layout()
    plt.show()

plot_temp_data()
plot_mass_data()
