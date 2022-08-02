import statistics
from algorithms import *
import pandas as pd

# MAKE IT RUN 10 TIMES

funs = [limited_greedy, heavy_greedy, defensive_greedy, deal_stingy, weight_stingy, sliding_threshold, scored_greedy, transitioning_greedy, standard_greedy, max_of_two, max_of_others]
def one_run(problem, time_df_dict, size_df_dict, loss_df_dict):
    data = open('instances_01_KP/large_scale/' + problem)
    optimal = int(open('instances_01_KP/large_scale-optimum/' + problem).read())
    weights = list()
    values = list()
    for line in data:
        dt = line.split(' ')
        if len(dt) > 2:
            break
        values.append(int(dt[0]))
        weights.append(int(dt[1]))
    capacity = int(problem.split('_')[-2])
    
  #  print('Capacity: ' + str(capacity))
  #  print('Weights: ' + str(weights))
  #  print('Prices: ' + str(values))
    tim = 0
    siz = 0
    for alg in funs:
        for i in range(10):
            dat = alg.__call__(capacity, weights, values)
            tim += dat[3]
            siz += dat[1]
        tim /= 10
        siz /= 10
        time_df_dict[str(alg)].append(tim)
        size_df_dict[str(alg)].append(siz)
        loss_df_dict[str(alg)].append(optimal - siz)
    
    return optimal

def one_run_legacy(problem, time_df_dict, size_df_dict, loss_df_dict):
    capacity = int(open(problem + '_c.txt').read())
    weights = list()
    for line in open(problem + '_w.txt'):
        weights.append(int(line))
    values = list()
    profits = open(problem + '_p.txt').readlines()
    solution = open(problem + '_s.txt').readlines()
    optimal = 0
    for i in range(len(profits)):
        values.append(int(profits[i]))
        if int(solution[i]) == 1:
            optimal += int(profits[i])
    
   # print('Capacity: ' + str(capacity))
   # print('Weights: ' + str(weights))
   # print('Prices: ' + str(values))
    for alg in funs:
        dat = alg.__call__(capacity, weights, values)
        time_df_dict[str(alg)].append(dat[3])
        size_df_dict[str(alg)].append(dat[1])
        loss_df_dict[str(alg)].append(optimal - dat[1])
    
    return optimal

time_df_dict = dict()
size_df_dict = dict()
loss_df_dict = dict()
meta_dict = dict()
for alg in funs:
    time_df_dict[str(alg)] = list()
    size_df_dict[str(alg)] = list()
    loss_df_dict[str(alg)] = list()
    meta_dict[str(alg)] = [0, 0, 0, 0]

optimals = list()

for prob in ['1_100', '1_200', '1_500', '1_1000', '1_2000', '1_5000', '1_10000', '2_100', '2_200', '2_500', '2_1000', '2_2000', '2_5000', '2_10000', '3_100', '3_200', '3_500', '3_1000', '3_2000', '3_5000', '3_10000']:
    optimals += [one_run('knapPI_' + prob + '_1000_1', time_df_dict, size_df_dict, loss_df_dict)]

for prob in range(1, 9):
    optimals += [one_run_legacy('flastatedata/p0' + str(prob), time_df_dict, size_df_dict, loss_df_dict)]

time_df = pd.DataFrame(time_df_dict)

size_df = pd.DataFrame(size_df_dict)

loss_df = pd.DataFrame(loss_df_dict)

skip_count = 0

print(optimals)

for r, row in loss_df.iterrows():
    min = row.min()
    i = 0
    for ind, val in row.iteritems():
        if val == min:
            meta_dict[ind][0] += 1
        #perc_error = ((val / optimals[i]))
        #print(perc_error)
        #meta_dict[ind][1] += perc_error
        #i += 1

for r, row in time_df.iterrows():
    min = row.min()
    for ind, val in row.iteritems():
        meta_dict[ind][2] += val / min
i = 0
for r, row in size_df.iterrows():
    min = row.min()
    for ind, val in row.iteritems():
        meta_dict[ind][3] += val / min
        perc_error = (1.0 - (val / optimals[i])) * 100
        print(perc_error)
        meta_dict[ind][1] += perc_error
    i += 1

for fun in funs:
    meta_dict[str(fun)][1] /= time_df.shape[0]
    meta_dict[str(fun)][2] /= time_df.shape[0]
    meta_dict[str(fun)][3] /= time_df.shape[0]

time_df.to_csv('time.tsv', sep='\t')
#print(time_df)

size_df.to_csv('perf.tsv', sep='\t')
#print(size_df)

loss_df.to_csv('loss.tsv', sep='\t')
#print(loss_df)

meta_df = pd.DataFrame(meta_dict)
meta_df.to_csv('meta.tsv', sep='\t')
meta_df.to_latex('meta.tex')
print(meta_df)