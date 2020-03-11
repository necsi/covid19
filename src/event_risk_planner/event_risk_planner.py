# general python
import pandas as pd
import numpy as np

# graphics
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("poster")


# the formula
def get_event_size(prob, inf_num, pop_size=10**6):
    """
    for every probability that a person is present at an event and
    the number of infected people calculates event size
    """
    pi = inf_num / pop_size
    return np.log10(1 - prob) / np.log10(1 - pi) 
    
 
def calculate_event_sizes(pop_size=10**6):
    incidents_rates = [10**(x/3) for x in range(6*3+1)]
    prob = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99] 
    lines = []
    for p in prob:
        for i in incidents_rates:
            lines.append((p, i, get_event_size(p, i, pop_size)))
            
    probs = pd.DataFrame(lines,  columns=['prob_has_sick', 'incident_rate', 'event_size'])
    return probs


def plot_figure(probs):
    p_inf_prob = probs.groupby('prob_has_sick').incident_rate.apply(list)
    p_event_size = probs.groupby('prob_has_sick').event_size.apply(list)
    
    fig, ax = plt.subplots(figsize=(18, 15))
    plt.plot(p_event_size.loc[0.01], p_inf_prob.loc[0.01],  c='k')
    plt.plot(p_event_size.loc[0.05], p_inf_prob.loc[0.05],  c='k')
    plt.plot(p_event_size.loc[0.2], p_inf_prob.loc[0.2],  c='k')
    plt.plot(p_event_size.loc[0.5], p_inf_prob.loc[0.5],  c='k')
    plt.plot(p_event_size.loc[0.95], p_inf_prob.loc[0.95],  c='k')
    plt.fill_between(p_event_size.loc[0.01], 0, p_inf_prob.loc[0.01], color='k', alpha=0.2)
    plt.text(100, 25, '1% chance', rotation=-27)
    plt.text(100, 125, '5% chance', rotation=-27)
    plt.text(100, 500, '20% chance', rotation=-27)
    plt.text(100, 1500, '50% chance', rotation=-27)
    plt.text(100, 6300, '95% chance', rotation=-27)
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel('Active circulating infertions per million population')
    plt.yticks(plt.yticks()[0], ['{:d}'.format(int(x)) for x in plt.yticks()[0]])
    ax.set_xticklabels([
        '1\n d','10\n Dinner party', 
        '100 \n Wedding reception', 
        '1000\n Small concert', 
        '10000\n Hockey Match', 
        '100000\n March Maddness\n Final in Atlanta'])
    #plt.xlabel('Event size')
    plt.title('COVID-19 Event Risk Assesment Planner\n Assumes Incidence Homogeneity')
    plt.text(10, 0.1, 
             'Risk ~ 1 - (1 - pi)^n, where pi = num cases / 10^6.\n' +
             'Adopted from JS Weitz https://github.com/jsweitz/covid-19-event-risk-planner '+
            'This calculation at https://github.com/gelisa/covid.git', fontsize=14)
    plt.xlim(10, 10**5);
    plt.ylim(1, 10**6);
