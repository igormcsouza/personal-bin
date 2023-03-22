from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta

# Create a CurrencyRates object
c = CurrencyRates()

def main():
    # Get today's exchange rate from USD to BRL
    today = datetime.now()
    today_rate = c.get_rate('USD', 'BRL')

    # Get the exchange rate from 5 days ago
    five_days_ago = datetime.now() - timedelta(days=5)
    five_days_ago_rate = c.get_rate('USD', 'BRL', five_days_ago)

    # Get the exchange rate from the first day of the current month
    first_day_of_month = datetime.now().replace(day=1)
    first_day_rate = c.get_rate('USD', 'BRL', first_day_of_month)

    # Get the exchange rate from exactly 1 month ago
    one_month_ago = datetime.now() - timedelta(days=30)
    one_month_ago_rate = c.get_rate('USD', 'BRL', one_month_ago)

    # Calculate the percentage difference between the rates
    five_days_ago_diff = ((today_rate - five_days_ago_rate) / five_days_ago_rate) * 100
    first_day_diff = ((today_rate - first_day_rate) / first_day_rate) * 100
    one_month_ago_diff = ((today_rate - one_month_ago_rate) / one_month_ago_rate) * 100

    # Print the results
    print(f">>> {today.strftime('%b %d, %Y')}")
    print(f">>> The exchange rate from USD to BRL today is BRL {today_rate:.2f}\n")

    # Calculate the maximum width of each column
    day_col_width = max(len("Day"), len(today.strftime('%b %d')), len(five_days_ago.strftime('%b %d')), len(first_day_of_month.strftime('%b %d')), len(one_month_ago.strftime('%b %d')))
    rate_col_width = max(len("Rate"), len("{:.2f}%".format(five_days_ago_diff)), len("{:.2f}%".format(first_day_diff)), len("{:.2f}%".format(one_month_ago_diff)), len("{:.2f}".format(today_rate)))

    # Print the results in a table format with fixed width columns
    print("| {}{} | {}{} |".format("Day".ljust(day_col_width), "", "Rate".rjust(rate_col_width), ""))
    print("|{}|{}|".format("-" * (day_col_width + 2), "-" * (rate_col_width + 2)))
    print("| {} | {} |".format("Today".ljust(day_col_width), "{:.2f}".format(today_rate).rjust(rate_col_width)))
    print("| {} | {} |".format(five_days_ago.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(five_days_ago_diff).rjust(rate_col_width)))
    print("| {} | {} |".format(first_day_of_month.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(first_day_diff).rjust(rate_col_width)))
    print("| {} | {} |".format(one_month_ago.strftime('%b %d').ljust(day_col_width), "{:.2f}%".format(one_month_ago_diff).rjust(rate_col_width)))

    return today_rate, five_days_ago_diff, first_day_diff, one_month_ago_diff


if __name__ == "__main__":
    SystemExit(main())

