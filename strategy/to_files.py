import matplotlib.pyplot as plt


def save(orders, directory, naming):
    fig, ax = plt.subplots()

    profit_list = []
    my_balance = 500
    for item in orders:
        my_balance += + item.profit
        profit_list.append(my_balance)
    ax.plot(profit_list)
    ax.grid()

    result_file = open(f'{directory}/{naming}.csv', 'w+')
    headers = orders[0].log[0].index.tolist()
    headers.append('profit')
    headers.append('buy_or_sell')
    result_file.write(','.join(headers) + '\n')
    for item in orders:
        for lo in item.log:
            lo['profit'] = str("%.2f" % item.profit)
            lo['buy_or_sell'] = str(item.buy_or_sell)
            result_file.write(','.join([str(val) for val in lo]))
            result_file.write('\n')
    result_file.close()

    fig.savefig(f'{directory}/{naming}.png')

    print('My balance: ', int(my_balance))
    print('Orders total: ', len(orders))
