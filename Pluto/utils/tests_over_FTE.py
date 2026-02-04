from utils.fetch_data import fetch_test_over_FTE_data

def get_test_per_fte_data():

    FTE = (40*3+32*2)*2

    general_tests_over_FTE = []

    test_over_FTE_data = fetch_test_over_FTE_data()
   
    for key,value in test_over_FTE_data.items():
        total_tests = 0
        executes_tests = 0
        automated_tests = 0

        new_item = {
            "Version":key#<-- stringa
        }
        new_item['additional_data'] = []
        for product_name,product_data in value.items():
            new_item["additional_data"].append( {
                "Product": product_name,
                "Total_Tests": product_data['total_tests'],#<--int
                "Executed_Tests": product_data['executed_tests'],#<-- int
                "Automated": product_data['automated_percentage'] * 100,
                "Test_over_FTE": round(product_data['executed_tests']/FTE,2)#<-- int
            })
            total_tests += product_data['total_tests']
            executes_tests += product_data['executed_tests']
            automated_tests += product_data['automated_test_count']
        
        new_item['Total Tests'] = total_tests#<-- int
        new_item['Executed Tests'] = executes_tests#<-- int
        new_item['Automated'] = round(automated_tests/total_tests,3)*100
        new_item['Tests over FTE'] = round(executes_tests/FTE,2)#<-- int

        general_tests_over_FTE.append(new_item)
        
    return general_tests_over_FTE
