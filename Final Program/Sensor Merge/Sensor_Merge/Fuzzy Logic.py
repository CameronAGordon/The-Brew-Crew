import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Prepare the dataset
dependent_var1_values = [405.1818182, 404.2727273, 406.3636364, 404.7272727, 404.8181818, 1168.636364, 
                         1263.454545, 938.0909091, 558.8181818, 849.4545455, 587.1818182, 477.0909091, 
                         443.3636364, 450.7272727, 480, 483.3636364, 568.5454545, 501.3636364, 469.8181818, 
                         450.8181818]
dependent_var2_values = [54.414, 54.55652174, 55.45833333, 54.06272727, 54.794, 62.00187, 68.0408, 60,
                         59.86166667, 60.105, 66.92052632, 65.838125, 62.37466667, 60, 60.37055556,
                         63.0795122, 68.85181818, 68.94952381, 63.14571429, 69.16129032]
independent_var = ['NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'NC', 'Coffee', 'Coffee',
                   'Coffee', 'Coffee', 'Coffee', 'NC', 'NC', 'NC', 'NC', 'NC']

# Define the fuzzy variables
dependent_var1 = ctrl.Antecedent(np.arange(400, 1300, 25), 'Dependent Variable 1')
dependent_var2 = ctrl.Antecedent(np.arange(50, 80, 1), 'Dependent Variable 2')
independent_var = ctrl.Consequent(np.arange(0, 101, 1), 'Independent Variable')

# Define the membership functions for the variables
dependent_var1['low'] = fuzz.trimf(dependent_var1.universe, [400, 425, 450])
dependent_var1['medium'] = fuzz.trimf(dependent_var1.universe, [400, 475, 700])
dependent_var1['high'] = fuzz.trimf(dependent_var1.universe, [600, 1050, 1300])

dependent_var2['low'] = fuzz.trimf(dependent_var2.universe, [50, 50, 59])
dependent_var2['medium'] = fuzz.trimf(dependent_var2.universe, [57, 63, 69])
dependent_var2['high'] = fuzz.trimf(dependent_var2.universe, [65, 68, 70])

independent_var['NC'] = fuzz.trimf(independent_var.universe, [0, 0, 50])
independent_var['Coffee'] = fuzz.trimf(independent_var.universe, [0, 50, 100])


rule1 = ctrl.Rule(dependent_var1['low'] & dependent_var2['low'], independent_var['NC'])
rule2 = ctrl.Rule(dependent_var1['low'] | dependent_var2['medium'], independent_var['NC'])
rule3 = ctrl.Rule(dependent_var1['low'] | dependent_var2['high'], independent_var['NC'])
rule4 = ctrl.Rule(dependent_var1['medium'] | dependent_var2['low'], independent_var['NC'])
rule5 = ctrl.Rule(dependent_var1['medium'] | dependent_var2['medium'], independent_var['Coffee'])
rule6 = ctrl.Rule(dependent_var1['medium'] | dependent_var2['high'], independent_var['NC'])
rule7 = ctrl.Rule(dependent_var1['high'] | dependent_var2['medium'], independent_var['NC'])
rule8 = ctrl.Rule(dependent_var1['high'] | dependent_var2['low'], independent_var['NC'])
rule9 = ctrl.Rule(dependent_var1['high'] & dependent_var2['high'], independent_var['NC'])

system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
anfis = ctrl.ControlSystemSimulation(system)

for i in range(len(dependent_var1_values)):
    anfis.input['Dependent Variable 1'] = dependent_var1_values[i]
    anfis.input['Dependent Variable 2'] = dependent_var2_values[i]
    anfis.compute()

    independent_var.view(sim=anfis)
    print("Input:", dependent_var1_values[i], dependent_var2_values[i])
    print("Output:", anfis.output['Independent Variable'])
    print("-----")
