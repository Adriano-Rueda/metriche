from utils.fetch_data import (
    fetch_defect_rate_data,
    fetch_defect_rate_detailed_data
)
import numpy as np
import re

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

    df_ratio = round((client_reported_bugs_df / total_bugs_df),1)

    df = df_ratio.replace([np.inf, -np.inf,np.nan], "No Bugs Reported")
    df = df.where(df.notna(), None)
    
    defect_dict =  df.to_dict(orient="index")
    defect_list = []
    for key,val in defect_dict.items():
        new_item = {}
        
        new_item["date"] = key
        for k,v in val.items():
            new_item[k] = v
        defect_list.append(new_item )
    return defect_list







if __name__ == "__main__":
    print(get_defect_rate_medio())