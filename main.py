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
model1_template,config1 = model_init(populations[0],0.1/5)
model2_template,config1 = model_init(populations[1],0.011/5)
model3_template,config1 = model_init(populations[2],0.01/5)


# Simulation execution: run for 20 days
# parameter refers to https://ndlib.readthedocs.io/en/latest/reference/models/epidemics/UTLDR.html#statuses
total_death_greedy = []
total_death_UD = []
total_death_IB = []
start,end = 0, 20


for init_day in range(start,end):
    ## reset
    beta_params = beta_param_generate(init_day,model1_template,model2_template,model3_template)

    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas)
    stats_greedy = solver.egreedy(
                    models = models,
                    populations = populations,
                    beta_params = beta_params,
                    epsilon= .2,
    )


    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas)
    stats_UD = solver.UD(
                    models = models,
                    populations = populations,
    )
    
    models = model_copy(model1_template,model2_template,model3_template)
    solver = Solver(num_vaccines = num_vaccines, num_areas = num_areas)
    stats_IB = solver.infection_based(
                    models = models,
                    populations = populations,
    )
    
    # calc total death
    total_death_greedy.append(calc_death(stats_greedy))
    total_death_UD.append(calc_death(stats_UD))
    total_death_IB.append(calc_death(stats_IB))
    

    
    
## plot figure
print(total_death_greedy)
print(total_death_UD)
print(total_death_IB)

days = list(range(start,end))
a = plt.plot(days, total_death_greedy)
b = plt.plot(days, total_death_UD)
c = plt.plot(days, total_death_IB)
m1 = "a"
m2 = "b"
m3 = "c"
plt.legend([m1,m2,m3])
plt.title('Accumulated Death after Initial Batch of Vaccine Distribution')
plt.grid(True)
plt.show()