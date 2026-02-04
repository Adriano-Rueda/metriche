from utils.fetch_data import (
    fetch_defect_rate_data,
    fetch_defect_rate_detailed_data
)
import numpy as np

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


def get_defect_rate_per_prodotto():
    total_bugs_df,client_reported_bugs_df = fetch_defect_rate_detailed_data()

    df_ratio = client_reported_bugs_df / total_bugs_df

    df = df_ratio.replace([np.inf, -np.inf,np.nan], None)
    df = df.where(df.notna(), None)
    
    df =  df.to_dict(orient="index")
    return df







if __name__ == "__main__":
    print(get_defect_rate_medio())