import datetime


def calculate_timestamp(time_delta_string):
    now = datetime.datetime.now()
    parts = time_delta_string.split('d')
    days = int(parts[0]) if parts[0] else 0

    time_parts = parts[1].split('h')
    hours = int(time_parts[0]) if time_parts[0] else 0

    minutes_parts = time_parts[1].split('m')
    minutes = int(minutes_parts[0]) if minutes_parts[0] else 0

    seconds_parts = minutes_parts[1].split('s')
    seconds = int(seconds_parts[0]) if seconds_parts[0] else 0

    time_delta = datetime.datetimedelta(days=days, hours=hours,
                                        minutes=minutes, seconds=seconds)
    timestamp = now - time_delta

    return timestamp


# TODO; The print function must be update to accept any number of dates
def print_results(today_rate, five_days_ago_diff, first_day_diff,
                  one_month_ago_diff, dates):
    today = datetime.datetime.now()

    # Print the results
    print(f">>> {today.strftime('%b %d, %Y')}")
    print(">>> The exchange rate from USD to BRL today is "
          f"BRL {today_rate:.2f}\n")

    # Calculate the maximum width of each column
    day_col_width = max(len("Day"),
                        len(today.strftime('%b %d')),
                        len(dates[0].strftime('%b %d')),
                        len(dates[1].strftime('%b %d')),
                        len(dates[2].strftime('%b %d')))
    rate_col_width = max(len("Rate"),
                         len("{:.2f}%".format(five_days_ago_diff)),
                         len("{:.2f}%".format(first_day_diff)),
                         len("{:.2f}%".format(one_month_ago_diff)),
                         len("{:.2f}".format(today_rate)))

    # Print the results in a table format with fixed width columns
    print("| {}{} | {}{} |".format("Day".ljust(day_col_width),
                                   "",
                                   "Rate".rjust(rate_col_width),
                                   ""))
    print("|{}|{}|".format("-" * (day_col_width + 2),
                           "-" * (rate_col_width + 2)))
    print("| {} | {} |".format(
        "Today".ljust(day_col_width),
        "{:.2f}".format(today_rate).rjust(rate_col_width)
    ))
    print("| {} | {} |".format(
        dates[0].strftime('%b %d').ljust(day_col_width),
        "{:.2f}%".format(five_days_ago_diff).rjust(rate_col_width)
    ))
    print("| {} | {} |".format(
        dates[1].strftime('%b %d').ljust(day_col_width),
        "{:.2f}%".format(first_day_diff).rjust(rate_col_width)
    ))
    print("| {} | {} |".format(
        dates[2].strftime('%b %d').ljust(day_col_width),
        "{:.2f}%".format(one_month_ago_diff).rjust(rate_col_width)
    ))

    return today_rate, five_days_ago_diff, first_day_diff, one_month_ago_diff


class ProcessError(Exception):
    pass
