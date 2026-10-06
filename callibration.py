from functions import * 
from scipy.optimize import curve_fit

t_data, T_data, solar_interp = load_sounds_data('salmon_sounds_data.csv')

T_deep = 11 # given

depth = 10 # estimate between 5 - 15m
tau = 30 # estimate between 1 - 60 days
specific_heat = 4000
density = 1025

a_guess = 1 / (depth * density * specific_heat)
b_guess = 1 / tau
p0 = [a_guess / 1e-8, b_guess, T_data[0]]

def callibrating_model(t, a_red, b, T_0):
    a = a_red * 1e-8
    sol = solve_ivp(temperature_ode, [t[0], t[-1]], [T_0], args=(solar_interp, T_deep, a, b),     t_eval=t, method="RK45", rtol=1e-10, atol=1e-13)
    return sol.y[0]

params = curve_fit(callibrating_model, t_data, T_data, p0=p0, bounds=([0, 1e-4, 0], [100, 5, 40]))

a_red, b, T_0 = params[0] 
a = a_red * 1e-8
plot_callibration(a, b, T_deep, T_0=T_0)
