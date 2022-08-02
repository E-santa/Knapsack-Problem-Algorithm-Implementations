import time
import random

def standard_greedy(capacity, weights, prices): # from fractional knapsack
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append((weights[i] / prices[i], weights[i], prices[i]))
    values.sort(reverse = False)
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    for value in values:
        if value[1] + tot_weight <= capacity:
            knapsack.append(value)
            tot_val += value[2]
            tot_weight += value[1] # exit when 100% full OR some % full???
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime)

def limited_greedy(capacity, weights, prices): # original
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append((prices[i], weights[i]))
    values.sort(reverse = True)
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    capacity_left = capacity
    for value in values:
        if capacity_left > 0.4 * capacity and value[1] <= capacity_left * 0.8:
            knapsack.append(value) 
            tot_val += value[0]
            tot_weight += value[1]
            capacity_left -= value[1]
        elif capacity_left <= 0.4 * capacity and value[1] <= capacity_left:
            knapsack.append(value) 
            tot_val += value[0]
            tot_weight += value[1]
            capacity_left -= value[1]
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime) # usually best

def heavy_greedy(capacity, weights, prices): # variation on standard greedy
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append((prices[i], weights[i]))
    values.sort(reverse = True)
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    capacity_left = capacity
    for value in values:
        if value[1] <= capacity_left:
            knapsack.append(value)
            tot_val += value[0]
            tot_weight += value[1]
            capacity_left -= value[1]
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime)

def defensive_greedy(capacity, weights, prices): # original
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append((weights[i], prices[i]))
    values.sort()
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    for value in values:
        if value[0] + tot_weight <= capacity:
            knapsack.append(value)
            tot_val += value[1]
            tot_weight += value[0]
        else: # Once this value won't fit, the next ones are guaranteed not to due to the sorting. So, just break here.
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime)

def deal_stingy(capacity, weights, prices):
    start = time.time()
    values = list()
    tot_val = 0
    tot_weight = 0
    for i in range(len(weights)):
        values.append(((prices[i] ** 3) / (weights[i] ** 1.5), weights[i], prices[i]))
        tot_val += prices[i]
        tot_weight += weights[i]
    values.sort(reverse = True)
    while tot_weight > capacity:
        tot_val -= values[-1][2]
        tot_weight -= values[-1][1]
        values.pop()
    end = time.time()
    runtime = end - start
    return (values, tot_val, tot_weight, runtime)

def weight_stingy(capacity, weights, prices):
    start = time.time()
    values = list()
    tot_val = 0
    tot_weight = 0
    for i in range(len(weights)):
        values.append((weights[i], prices[i]))
        tot_val += prices[i]
        tot_weight += weights[i]
    values.sort(reverse = False)
    while tot_weight > capacity:
        tot_val -= values[-1][1]
        tot_weight -= values[-1][0]
        values.pop()
    end = time.time()
    runtime = end - start
    return (values, tot_val, tot_weight, runtime)

def sliding_threshold(capacity, weights, prices):
    start = time.time()
    w = random.randint(0, len(weights) - 1)
    threshold = prices[w] / weights[w]
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    for i in range(len(weights)):
        if i > len(weights) / 4 and len(knapsack) <= len(weights) / 8: # TODO: compare to capacity left
            threshold *= 0.8
        elif i > len(weights) / 2 and len(knapsack) <= len(weights) / 4:
            threshold *= 0.8
        if prices[i] / weights[i] >= threshold and tot_weight + weights[i] <= capacity:
            tot_val += prices[i]
            tot_weight += weights[i]
            knapsack.append((weights[i], prices[i]))
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime)

def scored_greedy(capacity, weights, prices): # from fractional knapsack
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append(((prices[i] ** 3) / (weights[i] ** 1.5), weights[i], prices[i])) # TODO: change the score
    values.sort(reverse = True)
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    for value in values:
        if value[1] + tot_weight <= capacity:
            knapsack.append(value)
            tot_val += value[2]
            tot_weight += value[1]
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime)

def transitioning_greedy(capacity, weights, prices): # original
    start = time.time()
    values = list()
    for i in range(len(weights)):
        values.append((prices[i], weights[i]))
    values.sort(reverse = True)
    knapsack = list()
    tot_val = 0
    tot_weight = 0
    capacity_left = capacity
    for value in values:
        if capacity_left > 0.6 * capacity and value[1] <= capacity_left * 0.4:
            knapsack.append(value) 
            tot_val += value[0]
            tot_weight += value[1]
            capacity_left -= value[1]
            values.remove(value)
        elif capacity_left <= 0.6 * capacity:
            break
    new_values = list()
    for i in range(len(values)):
        new_values.append(((values[i][0] ** 3) / (values[i][1] ** 1.5), values[i][0], values[i][1]))
    new_values.sort(reverse = True)
    for value in new_values:
        if capacity_left - value[2] > 0:
            knapsack.append(value)
            tot_val += value[1]
            tot_weight += value[2]
            capacity_left -= value[2]
        if tot_weight == capacity:
            break
    end = time.time()
    runtime = end - start
    return (knapsack, tot_val, tot_weight, runtime) # best
    

def max_of_others(capacity, weights, prices):
    start = time.time()
    knapsacks = list()
    knapsacks.append(standard_greedy(capacity, weights, prices))
    knapsacks.append(limited_greedy(capacity, weights, prices))
    knapsacks.append(heavy_greedy(capacity, weights, prices))
    knapsacks.append(defensive_greedy(capacity, weights, prices))
    knapsacks.append(deal_stingy(capacity, weights, prices))
    knapsacks.append(weight_stingy(capacity, weights, prices))
    knapsacks.append(sliding_threshold(capacity, weights, prices))
    knapsacks.append(scored_greedy(capacity, weights, prices))
    knapsacks.append(transitioning_greedy(capacity, weights, prices))
    max_price = 0
    maxknap = None
    for knapsack in knapsacks:
        if knapsack[1] > max_price:
            maxknap = knapsack
            max_price = knapsack[1]
    end = time.time()
    runtime = end - start
    try:
        return (maxknap[0], maxknap[1], maxknap[2], runtime)
    except TypeError:
        return ([(0,)], 0, 0, runtime)

# TODO: add max of just heavy and standard
def max_of_two(capacity, weights, prices):
    start = time.time()
    knapsacks = list()
    knapsacks.append(standard_greedy(capacity, weights, prices))
    knapsacks.append(heavy_greedy(capacity, weights, prices))
    max_price = 0
    maxknap = None
    for knapsack in knapsacks:
        if knapsack[1] > max_price:
            maxknap = knapsack
            max_price = knapsack[1]
    end = time.time()
    runtime = end - start
    try:
        return (maxknap[0], maxknap[1], maxknap[2], runtime)
    except TypeError:
        return ([(0,)], 0, 0, runtime)
