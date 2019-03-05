import matplotlib.pyplot as pl
import numpy as np
import csv
import sys
import argparse
import scipy.optimize as opt


def get_year(date_str):
    split_date = date_str.split('-')
    return int(split_date[0])


def read_index_file(csv_file_name, start_year, end_year):
    with open(csv_file_name) as f:
        csv_reader = csv.DictReader(f)

        index_data = {key: [] for key in csv_reader.fieldnames}
        for row in csv_reader:
            year = get_year(row['Date'])
            if (year < start_year) or (year > end_year):
                continue
            for key, value in row.items():
                index_data[key].append(value)

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


def get_average_yearly_return(investment_return, number_of_months):
    n_years = number_of_months / 12

    def target_fun(interest):
        return_at_interest = ((1 + interest)**n_years - 1) / ((1+interest)**(1/12) - 1)
        return_respect_to_total_invested = return_at_interest / number_of_months

        return return_respect_to_total_invested - investment_return
    
    INITIAL_GUESS = 0.07
    return opt.newton(target_fun, INITIAL_GUESS)


def set_up_arguments():
    parser = argparse.ArgumentParser(description='Process monthly historical data from an index')
    parser.add_argument('-f', '--index_file',
                        default='index.csv',
                        help='File where the desired index data resides (csv)')
    parser.add_argument('-d', '--draw_history',
                        action='store_true',
                        help='If present, the history of the index is drawn before printing the statistics')
    parser.add_argument('-m', '--monthly_investment',
                        default=None,
                        type=float,
                        help='Monthly investment, to calculate the final worth')
    parser.add_argument('-y0', '--start_year',
                        default=0,
                        type=int,
                        help='Year where investment starts')
    parser.add_argument('-y1', '--end_year',
                        default=sys.maxsize,
                        type=int,
                        help='Year where investment ends')
    
    return parser


if __name__ == '__main__':
    parser = set_up_arguments()
    args = parser.parse_args()
    
    index_data = read_index_file(args.index_file, args.start_year, args.end_year)

    monthly_highs = list(map(float, index_data['High']))

    monthly_investment = 1000
    print_worth = False
    if args.monthly_investment is not None:
        monthly_investment = args.monthly_investment
        print_worth = True

    month_investment_return, total_invested = calc_return(monthly_highs, monthly_investment, 1)
    year_investment_return, total_invested = calc_return(monthly_highs, 12 * monthly_investment, 12)

    n_months_invested = len(monthly_highs)

    print('Return multiplier with monthly investment: {:.2f}'
          .format(month_investment_return))
    print('Average return per year: {:.2f}%'
          .format(100 * get_average_yearly_return(month_investment_return, n_months_invested)))
    if (print_worth):
        print('Total invested: {:,.2f}. Total worth: {:,.2f}'.format(total_invested, month_investment_return * total_invested))
    
    print()

    print('Return with single yearly investment: {:.2f}'
          .format(year_investment_return))
    print('Average return per year: {:.2f}%'
          .format(100 * get_average_yearly_return(year_investment_return, n_months_invested)))
    if (print_worth):
        print('Total invested: {:,.2f}. Total worth: {:,.2f}'.format(total_invested, year_investment_return * total_invested))

    print()

    print('Invested from {} until {}'
          .format(index_data['Date'][0], index_data['Date'][-1]))

    if args.draw_history:
        plot_graph(index_data)
