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

growth_guess = 0.0002
mortality_guess = 0.01
B_0_guess = 5000
heat_threshold = 17.5

def callibrating_temp_model(t, a, b, T_0):
    sol = solve_ivp(temperature_ode, [t[0], t[-1]], [T_0], args=(solar_interp, T_deep, a, b), t_eval=t, method="RK45", rtol=1e-10, atol=1e-13)
    return sol.y[0]

#def callibrating_mass_model(t, g, mortality, B_0):
def callibrating_mass_model(t, g, mortality):
    B_0 = biomass[0]
    sol = solve_ivp(biomass_ode, [t[0], t[-1]], [B_0], args=(g, T, mortality, heat_threshold, harvest_interp, stocking_interp), t_eval=t, method="RK45", rtol=1e-6, atol=1e-8, max_step = 1)
    return sol.y[0]

p0 = [a_guess, b_guess, T_data[0]]

temp_params = curve_fit(callibrating_temp_model, t_data, T_data, p0=p0, bounds=([-5, 1e-4, 0], [5, 5, 40]))

a, b, T_0 = temp_params[0] 

print(f"a: {a}, b:{b}, T_0:{T_0}")
plot_temp_callibration(a, b, T_deep, T_0=T_0)

t_full = np.arange(0, 729)
T_model = solve_temperature_ode(t_full, solar_interp, a, b, T_deep, T_0 = T_0)
T = interp1d(t_full, T_model)

t_data, stocking_interp, harvest_interp, biomass = load_mass_data('salmon_sounds_data.csv')

#p0 = [growth_guess, mortality_guess, B_0_guess]
p0 = [growth_guess, mortality_guess]
#mass_params = curve_fit(callibrating_mass_model, t_data, biomass, p0=p0, bounds=([0, 0], [1, 1]), diff_step = 1e-3)
#mass_params = curve_fit(callibrating_mass_model, t_data, biomass, p0=p0, bounds=([0, 0, 2000], [1, 1, 10000]), diff_step = 1e-3)

g = 0.00038104741976732734
m = 0.003245229444071601
#g, m= mass_params[0] 

#g, m, B_0= mass_params[0] 
B_0 = biomass[0]

print(f"growth rate (%): {g * 100}%, mortality rate (%) :{m * 100}%")
plot_mass_callibration(T, g, m, heat_threshold, B_0=B_0)
