import matplotlib.pyplot as pl
import numpy as np
import csv
import itertools as it
import argparse

def get_month(date_str):
    split_date = date_str.split('-')
    return int(split_date[1])


def read_index_file(csv_file_name):
    with open(csv_file_name) as f:
        csv_reader = csv.DictReader(f)
        first_date = next(csv_reader.__iter__())

        index_data = {key: [] for key in csv_reader.fieldnames}
        for row in csv_reader:
            for key, value in row.items():
                index_data[key].append(value)

        months = list(map(get_month, index_data['Date']))
        repeated_indices = list()
        for i, month in enumerate(months):
            if months[i] == months[i-1]:
                repeated_indices.append(i)

        for key in index_data.keys():
            index_data[key] = [x for i, x in enumerate(index_data[key]) if i not in repeated_indices]

    return index_data


def plot_graph(data):
    xticks = data['Date'][0::12]
    x = list(range(len(data['Date'])))[0::12]
    pl.xticks(x, xticks, rotation=45)
    pl.plot(list(map(float, data['High'])))
    pl.show()
    

def calc_return(monthly_highs, amount_per_time, month_freq):
    costs_of_investment = np.array(list(monthly_highs[0::int(month_freq)]))
    
    shares = np.sum(amount_per_time / costs_of_investment)

    final_worth = shares * monthly_highs[-1]
    total_invested = amount_per_time * len(costs_of_investment)

    return final_worth / total_invested, total_invested


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process monthly historical data from an index')
    parser.add_argument('--index_file',
                        default='index.csv',
                        help='File where the desired index data resides (csv)')

    args = parser.parse_args()
    index_data = read_index_file(args.index_file)

    monthly_highs = list(map(float, index_data['High']))

    month_investment_return, total_invested = calc_return(monthly_highs, 1000, 1)
    year_investment_return, total_invested = calc_return(monthly_highs, 12000, 12)

    print('Return with monthly investment: {}. Total worth: {}'
          .format(month_investment_return, month_investment_return * total_invested))
    print('Return with single yearly investment: {}. Total worth: {}'
          .format(year_investment_return, year_investment_return * total_invested))
    print('Invested from {} until {}'
          .format(index_data['Date'][0], index_data['Date'][-1]))

    plot_graph(index_data)
