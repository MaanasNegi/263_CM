from functions import *

# Load in data
t_data, T_data, _ = load_calibration_data('benchmark_pen.csv')

# parameters to callibrate
a = 1
b = 2

T_deep = 11
# Solve model using a=1, b=2 for all times in t_data (one every 30 seconds)
T_model = solve_temperature_ode(t_data, a, b, T_deep)

# Plot solution for a=1, b=2
plot_calibration(1,2);
