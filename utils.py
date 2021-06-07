import networkx as nx
import numpy as np
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as epd
import copy


def ULTDR(g, **configs):
  model = epd.UTLDRModel(g)
  config = mc.Configuration()

  # Undetected
  config.add_model_parameter("sigma", configs['sigma'])
  config.add_model_parameter("beta", configs['beta'])
  config.add_model_parameter("gamma", configs['gamma'])
  config.add_model_parameter("omega", configs['omega'])

  # Vaccination
  config.add_model_parameter("v", configs['vac_prob']) 
  config.add_model_parameter("fraction_infected", configs['fraction_infected']) 

  model.set_initial_status(config)

  return model,config


def population_count(stat):
  status = {}
  for i in stat.keys():
    if stat[i] not in status:
      status[stat[i]] = 1
    else:
      status[stat[i]] += 1

  return status


def model_init(population,fraction_infected):
  g = nx.erdos_renyi_graph(population, .1)
  model_template,config = ULTDR(g, 
                          sigma = .167,
                          beta = .1,
                          gamma =.1,
                          omega = .02,
                          vac_prob = 0,
                          fraction_infected = fraction_infected,
                          )
  
  return model_template,config

def beta_param_generate(init_day,model1_template,model2_template,model3_template):
  iterations = model1_template.iteration_bunch(init_day)
  iterations = model3_template.iteration_bunch(init_day)
  iterations = model2_template.iteration_bunch(init_day)

  beta_param_1 = population_count(model1_template.status)
  beta_param_2 = population_count(model2_template.status)
  beta_param_3 = population_count(model3_template.status)
  return [beta_param_1,beta_param_2,beta_param_3]

def model_copy(model1_template,model2_template,model3_template):
  model1 = copy.deepcopy(model1_template)
  model2 = copy.deepcopy(model2_template)
  model3 = copy.deepcopy(model3_template)
  return [model1, model2,model3]

def calc_death(stats):
  deaths = 0
  for stat in stats:
    try:
      deaths += stat[11]
    except:
      pass
  return deaths

def num_infections(stat):
  try:
    inf = population_count(stat)[1]
  except:
    inf = 0
  return inf


