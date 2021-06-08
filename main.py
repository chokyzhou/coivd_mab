from egreedy import EGreedy
from utils import model_init,population_count, beta_param_generate, model_copy,calc_death
from solver import Solver
import matplotlib.pyplot as plt

## hyper param. and initialization
populations = [
    10000,
    3000,
    5000,
]
num_vaccines = 3000
num_areas = 3

## create model
model1_template,config1 = model_init(populations[0],0.01)
model2_template,config1 = model_init(populations[1],0.1)
model3_template,config1 = model_init(populations[2],0.01)


# Simulation execution: run for 20 days
# parameter refers to https://ndlib.readthedocs.io/en/latest/reference/models/epidemics/UTLDR.html#statuses
total_death_greedy = []
total_death_UD = []
total_death_IB = []
total_death_PB = []
start,end = 0, 1
observe_day = 6

for init_day in range(start,end):
    print(init_day)
    ## reset
    beta_params = beta_param_generate(init_day,model1_template,model2_template,model3_template)

    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas, observe_day = observe_day)
    stats_greedy = solver.egreedy(
                    models = models,
                    populations = populations,
                    beta_params = beta_params,
                    epsilon= .2,
    )


    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas,observe_day = observe_day)
    stats_UD = solver.UD(
                    models = models,
                    populations = populations,
    )
    
    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas,observe_day = observe_day)
    stats_IB = solver.infection_based(
                    models = models,
                    populations = populations,
    )
    
    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas,observe_day = observe_day)
    stats_PB = solver.population_based(
                    models = models,
                    populations = populations,
    )
    
    # calc total death
    total_death_greedy.append(calc_death(stats_greedy))
    total_death_UD.append(calc_death(stats_UD))
    total_death_IB.append(calc_death(stats_IB))
    total_death_PB.append(calc_death(stats_PB))
    

    
    
## plot figure
print(total_death_greedy)
print(total_death_UD)
print(total_death_IB)
print(total_death_PB)

days = list(range(start,end))
a = plt.plot(days, total_death_greedy)
b = plt.plot(days, total_death_UD)
c = plt.plot(days, total_death_IB)
c = plt.plot(days, total_death_PB)
m1 = "Proposed Distribution Solution"
m2 = "Distribute by Number of States"
m3 = "Distribute by Number of Infections"
m4 = "Distribute by Population"
plt.legend([m1,m2,m3,m4])
plt.title('Accumulated Death after Initial Batch of Vaccine Distribution')
plt.grid(True)
plt.show()
'''
days = list(range(start,end))
plt.plot(days, [a - b for a,b in zip(total_death_greedy,total_death_UD)])
plt.title('Number of avoided Death')
plt.grid(True)
plt.show()
'''

