from functions import *

t_data, T_data, solar_interp = load_sounds_data('salmon_sounds_data.csv')

T_deep = 11 # given

depth = 10 # estimate between 5 - 15m
tau = 45 # estimate between 1 - 90 days
T_0 = 18 # estimate between 12 - 24 

specific_heat = 4000
density = 1025

a = 1 / (depth * density * specific_heat)
b = 1 / tau

T_model = solve_temperature_ode(t_data, solar_interp, a, b, T_deep, T_0 = T_0)
plot_callibration(a, b, T_deep, T_0 = T_0);

