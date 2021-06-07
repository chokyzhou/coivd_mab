viz = DiffusionTrend(model, trends)
  viz.plot(statuses=['Exposed', 'Infected', 'Dead', 'Identified_Exposed', 'Hospitalized_severe_ICU'])
  viz.show()