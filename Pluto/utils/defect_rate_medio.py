from utils.fetch_data import fetch_defect_rate_data


def get_defect_rate_medio():
    total_bugs, client_reported_bugs = fetch_defect_rate_data()

    result = {}

    for date, total in total_bugs.items():
        client = client_reported_bugs.get(date)

        if client is not None and total != 0:
            result[date] =(client / total)
        else:
            result[date] = 0

    return result


if __name__ == "__main__":
    print(get_defect_rate_medio())