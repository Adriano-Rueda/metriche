import random
import pandas as pd
import re
import os

defect_rate_data_path = "resources/Modello_TCoE_Report_OKR-1_EDR.xlsx"
total_bug_sheet_name = "TCoE_Report_OKR-1_Iniziativa-ED"
client_report_sheet_name = "TCoE_Report_OKR-1_Iniziativa--E"

time_to_test_release_path = "resources/Modello_TCoE_Report_OKR-2_Iniziativa-Tempo_Test_Release.xlsx"
build_release_sheet_name = "License_Server"
changelog_sheet_name = "Changelog"

bugia_exports_folder_path = "resources/bugia_exports/"

# Get Defect Rate Data
def get_defect_rate_data():
    total_bug_df = pd.read_excel(defect_rate_data_path, sheet_name=total_bug_sheet_name)
    client_report_df = pd.read_excel(defect_rate_data_path, sheet_name=client_report_sheet_name)

    total_bug_df = pd.DataFrame({
        "Data": total_bug_df.iloc[:, 0],
        "Totale": total_bug_df.iloc[:, 1:].sum(axis=1)
    })

    client_report_df = pd.DataFrame({
        "Data": client_report_df.iloc[:, 0],
        "Totale": client_report_df.iloc[:, 1:].sum(axis=1)
    })
    
    total_bug_dict = dict(zip(
        total_bug_df["Data"],
        total_bug_df["Totale"]
    ))

    client_report_dict = dict(zip(
        client_report_df["Data"],
        client_report_df["Totale"]
    ))


    return total_bug_dict, client_report_dict

def get_defect_rate_detailed_data():
    total_bug_df = pd.read_excel(defect_rate_data_path,sheet_name=total_bug_sheet_name)
    total_bug_df.set_index(total_bug_df.columns[0], inplace=True)
    client_report_df = pd.read_excel(defect_rate_data_path, sheet_name=client_report_sheet_name)
    client_report_df.set_index(client_report_df.columns[0], inplace=True)
    return total_bug_df,client_report_df
#################################################################


# Get Time to Test Release Data
def helper_clean_version(version_str):
    if isinstance(version_str, str):
        splits = re.split('-', version_str)
        return splits[0].strip()
    return version_str


def helper_parse_date(date_str):
    if isinstance(date_str, pd.Timestamp):
        return date_str.date()
    return pd.to_datetime(date_str).date()

def helper_parse_changelog_date(date_str):
    [day,month,year] = re.split('/',date_str,maxsplit=2)
    return helper_parse_date( f"{month}/{day}/{year}")

    
def get_time_to_test_release_data():
    build_release_df = pd.read_excel(time_to_test_release_path, sheet_name=build_release_sheet_name)
    changelog_df = pd.read_excel(time_to_test_release_path, sheet_name=changelog_sheet_name)


    build_release_df = pd.DataFrame({
        "Build": build_release_df.iloc[:,0].apply(helper_clean_version),
        "release_date": build_release_df['release_date'].apply(helper_parse_date)
    })
   
    build_release_dict = build_release_df.to_dict(orient='records')

    changelog_df = pd.DataFrame({
        "Version": changelog_df.iloc[:, 1],
        "release_date": changelog_df.iloc[:, 3].apply(helper_parse_changelog_date)
    })  
    changelog_dict = dict(zip(
        changelog_df["Version"],
        changelog_df["release_date"]
    ))

    return build_release_dict, changelog_dict
################################################################




# Get Test over FTE Data
def get_test_over_FTE_data():
#sheet_name="TCoE_Report_OKR3_KR-3.1_WebCTI"
    bugia_exports_folder = os.listdir(bugia_exports_folder_path)

    test_over_FTE_data = {}

# tmp mock data
    def get_random_test_results():
        test_item = {
            "total_tests":random.randint(1200,1500),
            "executed_tests":random.randint(1000,1200),
            "automated_test_count": random.randint(300,1500),
        }
        test_item["test_over_FTE_percentage"]= test_item["executed_tests"] / ((40*3+32*2)*2)
        test_item["automated_percentage"]= test_item["automated_test_count"] / test_item["total_tests"]
        return test_item
    
    for i in range (1,13):
        mock_version = f"4.17.{i}"
        products = ["CTI","LAM","Kalliope PBX OMNIA","API"]
        new_item = {}
        for product in products:
            new_item[product] = get_random_test_results()
        test_over_FTE_data[mock_version] = new_item

#---------------

    for file in bugia_exports_folder:

        tests = pd.read_csv(os.path.join(bugia_exports_folder_path, file))
        valid_env = ["MONOTENANT", "MULTITENANT","GUI"]
        total_tests = tests.iloc[lambda x: (x["Rc version"]==0) & (x["Status"]=="TO DO") & (x["Env description"].isin(valid_env))]
        executed_tests = tests.iloc[lambda x: (x["Rc version"]!=0) & (x["Status"]!="TO DO") & (x["Env description"].isin(valid_env))]
        automated_tests = total_tests.iloc[lambda x: (x["Automatic"] == "RANOREX AUTOMATIC")]
        
        total_tests_count = total_tests.shape[0]
        executed_tests_count = executed_tests.shape[0]
        total_automated_tests = automated_tests.shape[0]
        percentage_automated = total_automated_tests / total_tests_count

        product_name = tests.iloc[0]["Product name"] 

        test_over_FTE_data[tests.iloc[0]["Version"]] = {} if tests.iloc[0]["Version"] not in test_over_FTE_data else test_over_FTE_data[tests.iloc[0]["Version"]]
        test_over_FTE_data[tests.iloc[0]["Version"]][product_name] = {
            "total_tests": total_tests_count,
            "executed_tests": executed_tests_count,
            "automated_test_count": total_automated_tests if total_automated_tests else 0,
            "automated_percentage": percentage_automated if percentage_automated else 0,
            "test_over_FTE_percentage": (executed_tests_count / ((40*3 + 32*2)*2)) if total_tests_count > 0 else 0
        }


    return test_over_FTE_data
###############################################################
