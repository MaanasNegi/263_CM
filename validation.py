from functions import *

# benchmark data
depth = ...
tau = ...
T_deep = ... 

specific_heat = ...
density = ...

a = ...
b = ...

t_benchmark, T_benchmark, solar_interp = load_benchmark_data("benchmark_pen.csv")
T_0 = T_benchmark[0]

T_model = solve_temperature_ode(t_benchmark, solar_interp, a, b, T_deep, T_0 = T_0)

fig, ax = plt.subplots(1, 1, figsize=(9,6), sharex=True)

ax.scatter(t_benchmark, T_benchmark, color = "r", label = "Benchmark Plot")
ax.plot(t_benchmark, T_model, "--" , color="b", label = "Numerical Plot")
ax.set_xlabel("t")
ax.set_ylabel("T")

plt.title("Benchmark vs Numerical Solution using benchmark parameters")
ax.legend()

plt.tight_layout()
plt.show()
