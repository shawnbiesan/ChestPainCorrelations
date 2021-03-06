import datetime
import csv
import sys
import pylab
import operator

def generate_delta_plot(data_file, day_length=1, start=0):
    """ Generates plot of errors for each possible lag in time series """
    
    input_file = csv.DictReader(open(data_file))
    counts = []
    counts_fem = []
    deltas = []
    for line in input_file:
        counts.append(int(line['Patient Count']))
        counts_fem.append(int(line['Patient Count Female']))
    left_over_values = (len(counts)-start) % day_length
    deltas = [counts[pos] - counts[pos-day_length] for pos in range(day_length+start, len(counts) - left_over_values)]
    deltas_fem = [counts_fem[pos] - counts_fem[pos-day_length] for pos in range(day_length+start, len(counts_fem) - left_over_values)]
    pylab.hist(deltas, color='red')
    pylab.title("Spaced by %s days" % (day_length,))
    pylab.savefig("%s_%s_days.png" %(data_file.split('.')[0], day_length,))  #strips .csv and uses that as name base
    pylab.clf()

def choose_best_cycle(data_file):
    """ Figures out best lag in time series """
    
    input_file = csv.DictReader(open(data_file))
    counts = []
    cycle_errors = {}
    for line in input_file:
        counts.append(int(line['Patient Count']))
    for k in range(1, 31):
        start_error = {}
        error = 0
        for start in range(0, k): #issue, strips off anything that doesn't fit on left side but not right side maybe I made it other side issue? 
            left_over_values = (len(counts)-start) % k
            error_terms = [1.0 * abs(counts[pos] - counts[pos-k]) for pos in range(k+start, len(counts)-left_over_values)]
            #error_terms = [1.0 * sum([abs(counts[sub_pos] - counts[sub_pos-k]) for sub_pos in range(pos, pos+k)])/k for pos in range(k+start, len(counts) - k, k)]
            #this averages error over k group and then averages that again with main
            error = 1.0 * sum(error_terms) / len(error_terms)
            start_error[start] = error
        best_start_key = min(start_error.iteritems(), key=operator.itemgetter(1))[0]
        cycle_errors[(k,best_start_key)] = start_error[best_start_key]
    print sorted(cycle_errors.items(), key=lambda x: x[1])[:5]
    return sorted(cycle_errors.items(), key=lambda x: x[1])[:5]


def main():
    data_file = sys.argv[1]
    best_cycles = choose_best_cycle(data_file)
    for entry in best_cycles:
        generate_delta_plot(data_file, day_length=int(entry[0][0]), start=int(entry[0][1]))
    
if __name__ == '__main__':
    main()
