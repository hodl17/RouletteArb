# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 18:02:37 2020

@author: devli
"""
import pandas as pd
import random
import math
import statistics
import matplotlib.pyplot as plt

investment = 100
total_stake = 2*investment


def expected_value(investment,stake):
    current_value = stake
    for spin in range(1,26):
        current_value = current_value*(36/37)
        
    edge = ((current_value - investment)/investment)*100
    return str(round(edge,2)) + "%"

def payoffs(num,rb_stake,g_stake):
    payoff = 0
    if num == 0:
        payoff = 36*g_stake
    else:
        payoff = 2*rb_stake
    return payoff

def simulator(inv,tot_stake,rb_ratio):
    capital = tot_stake
    excess_profit = 0
    spins = []
    capital_each_spin = []
    for spin in range(1,26):
        capital_each_spin.append(round(capital + excess_profit,2))
        spins.append(spin)
        if capital > 200:    
            excess_profit += capital - 200
            capital = 200
        if capital == 0:
            if excess_profit > 200:
                capital = 200
                excess_profit -= 200
            elif excess_profit > 0:
                capital = excess_profit
                excess_profit = 0
            else:
                break
        rb_stake = (capital)*rb_ratio
        g_stake = capital - 2*rb_stake
        number = random.randint(0,36)
        capital = payoffs(number,rb_stake,g_stake)
        
    if len(capital_each_spin)<25:
        extension = [0]*(25-len(capital_each_spin))
        capital_each_spin = capital_each_spin + extension
        
    return round(capital + excess_profit,2), capital_each_spin

def plot_paths(spins,capital):
    plt.figure(0)
    plt.plot(spins,capital)
    plt.xlabel('Number of spins',size=12)
    plt.ylabel('Capital Remaining',size=12)
    plt.title('Simulated Paths',size=15)
    
def monte_carlo(inv,stake,rb_ratio):
    capital = []
    cap_df = pd.DataFrame(index=list(range(1,26)))
    for spin in range(0,10000):
        remaining_capital, capital_path = simulator(inv,stake,rb_ratio)
        capital.append(remaining_capital-investment)
        cap_df[spin] = capital_path
        
    mean = sum(capital)/len(capital)
    variance = sum((i-mean)**2 for i in capital)/(len(capital)-1)
    sharpe = (mean-investment)/math.sqrt(variance)
    median = statistics.median(capital)
    edge_mc = calculate_edge(capital,inv)
    
    return capital, mean, variance, sharpe, median, cap_df, edge_mc

def calculate_edge(capital,inv):
    unique_returns = list(set(capital))
    edge_dict = {}
    for ret in unique_returns:
        edge_dict[ret] = capital.count(ret)/len(capital)
    
    expected_return = 0
    for key in edge_dict:
        expected_return += edge_dict[key]*key

    edge = ((expected_return-inv)/inv)*100
    return str(round(edge,2)) + "%"

def plot_histogram(capital):
    plt.figure(1)
    plt.hist(capital)
    plt.title('Distribution of Returns',size=15)
    plt.xlabel('Capital Remaining',size=12)
    plt.ylabel('Frequency',size=12)

ev_edge = expected_value(investment,total_stake)
capital, mean, variance, sharpe, median, cap_df, edge = monte_carlo(investment,total_stake,0.45)
plot_paths(list(range(1,26)),cap_df)
plot_histogram(capital)
print(edge)




