from egreedy import EGreedy
from collections import Counter
import numpy as np
from utils import population_count,num_infections

class Solver:
    def __init__(self,num_vaccines,num_areas):
        self.num_vaccines = num_vaccines
        self.num_areas = num_areas
            
    def egreedy(self,models,populations,beta_params,epsilon = .2):
        ## init. 
        model1 = models[0]
        model3 = models[1]
        model2 = models[2]

        egreedy = EGreedy(k=self.num_areas, epsilon = epsilon)

        sum_rewards = 0.0
        expected_rewards = []
        choices = []

        for i in range(1, self.num_vaccines + 1):
            
            # choose an arm
            area_chosen = egreedy.choose()
            choices.append(area_chosen)
            
            if area_chosen == 0:
                probability_of_true_positive = beta_params[0].get(0, 0) / ( beta_params[0].get(0, 0) + beta_params[0].get(2, 0))
            elif area_chosen == 1:
                probability_of_true_positive = beta_params[1].get(0, 0)  / ( beta_params[1].get(0, 0)  + beta_params[1].get(2, 0) )
            else:
                probability_of_true_positive = beta_params[2].get(0, 0)  / ( beta_params[2].get(0, 0)  + beta_params[2].get(2, 0) )
            
            # give reward
            random_number = np.random.uniform(0.0, 1, 1)[0]
            reward = 1.0 if random_number < probability_of_true_positive else 0.0
            
            sum_rewards += reward
            expected_rewards.append(sum_rewards / i)
            
            egreedy.feedback(arm_id=area_chosen, reward=reward)
        

        ## herd immunity rate
        for area_chosen,vac_dist in Counter(choices).items():
            if area_chosen == 0:
                model1.params["model"]['v'] = vac_dist/populations[0]
            elif area_chosen == 1:
                model2.params["model"]['v'] = vac_dist/populations[1]
            else:
                model3.params["model"]['v'] = vac_dist/populations[2]
                
        iterations = model1.iteration_bunch(6)
        iterations = model2.iteration_bunch(6)
        iterations = model3.iteration_bunch(6)
        stat1 = model1.status
        stat2 = model2.status
        stat3 = model3.status
        return (population_count(stat1),
                population_count(stat2),
                population_count(stat3),
                )
        
        
    def UD(self,models,populations, ):
        ## init. 
        model1 = models[0]
        model3 = models[1]
        model2 = models[2]

        choices = [(0,self.num_vaccines//3),
                (1,self.num_vaccines//3),
                (2,self.num_vaccines//3),]

        ## herd immunity rate
        for area_chosen,vac_dist in Counter(choices).items():
            if area_chosen == 0:
                model1.params["model"]['v'] = vac_dist/populations[0]
            elif area_chosen == 1:
                model2.params["model"]['v'] = vac_dist/populations[1]
            else:
                model3.params["model"]['v'] = vac_dist/populations[2]
                
        iterations = model1.iteration_bunch(6)
        iterations = model2.iteration_bunch(6)
        iterations = model3.iteration_bunch(6)
        stat1 = model1.status
        stat2 = model2.status
        stat3 = model3.status
        return (population_count(stat1),
                population_count(stat2),
                population_count(stat3),
                )
    
    def infection_based(self,models,populations):
        model1 = models[0]
        model3 = models[1]
        model2 = models[2]

        inf1 = num_infections(model1.status)    
        inf2 = num_infections(model2.status)    
        inf3 = num_infections(model3.status)    

       
        inf = inf1 + inf2 +inf3

        choices = [(0,self.num_vaccines*inf1/(inf+1)),
                (1,self.num_vaccines*inf2/(inf+1)),
                (2,self.num_vaccines*inf3/(inf+1)),]

        ## herd immunity rate
        for area_chosen,vac_dist in Counter(choices).items():
            if area_chosen == 0:
                model1.params["model"]['v'] = vac_dist/populations[0]
            elif area_chosen == 1:
                model2.params["model"]['v'] = vac_dist/populations[1]
            else:
                model3.params["model"]['v'] = vac_dist/populations[2]
                
        iterations = model1.iteration_bunch(6)
        iterations = model2.iteration_bunch(6)
        iterations = model3.iteration_bunch(6)
        stat1 = model1.status
        stat2 = model2.status
        stat3 = model3.status
        return (population_count(stat1),
                population_count(stat2),
                population_count(stat3),
                )