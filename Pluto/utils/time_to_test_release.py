from utils.fetch_data import get_time_to_test_release_data
import datetime

def get_tempo_di_esecuzione_medio():
    build_release, changelog = get_time_to_test_release_data()
    
    first_build_release = {}

    for item in build_release:
        version = item['Build']
        release = item['release_date']

        if not  version in first_build_release:
            first_build_release[version] = release
        elif release < first_build_release[version]:
            first_build_release[version] = release

    montly_stat = {}
    montly_stat_excluding_short_tests = {}

    for version,date in changelog.items():

        rc0_release = first_build_release[version]
        days_passed = (date - rc0_release).days

        date = datetime.datetime(
            year=date.year,
            month=date.month,
            day=1
        )
        if days_passed >7:
            if date in montly_stat_excluding_short_tests:
                montly_stat_excluding_short_tests[date]={
                    "releases":montly_stat_excluding_short_tests[date]["releases"]+1,
                    "test_days":montly_stat_excluding_short_tests[date]["test_days"]+days_passed
                }
            else:
                montly_stat_excluding_short_tests[date]={
                    "releases":1,
                    "test_days":days_passed
                }

        if date in montly_stat:
            montly_stat[date]={
                "releases":montly_stat[date]["releases"]+1,
                "test_days":montly_stat[date]["test_days"]+days_passed,   
            }
            montly_stat[date]["avg_test_duration"]=montly_stat[date]["test_days"] / montly_stat[date]["releases"]
        else:
            montly_stat[date]={
                "releases":1,
                "test_days":days_passed,
                "avg_test_duration":days_passed
            }



    def recap(montly_stat):
        date = datetime.datetime( #prendo solo gli ultimi 2 anni
            year=datetime.datetime.today().year -2,
            month=datetime.datetime.today().month,
            day=1
        )
        recap = {}
        while date < datetime.datetime.today():
            if date not in montly_stat:
                recap[date]={
                    "releases":0,
                    "test_days":0
                }
            else:
                recap[date]=montly_stat[date]
            year = date.year if date.month<12 else date.year+1
            month = date.month + 1 if date.month<12 else 1
            date = datetime.datetime(
                year=year,
                month=month,
                day=1
            )

        
        prova = {}
        detailed_stats = []
        generic_stats = []
        
        for date,data in recap.items():
            firmware_releases = 0
            test_days = 0

            for i in range (1,7):
                month = date.month
                year = date.year


                year = year if month>i else year -1
                month = month-i if month>i else month+12-i

                new_date = datetime.datetime(
                    year=year,
                    month=month,
                    day=1
                )

                if new_date in recap:
                    month_data = recap[new_date].copy()
                    month_data['Date']=date
                    month_data['Event Date']=new_date
                    detailed_stats.append(month_data)

                    test_days += recap[new_date]["test_days"]
                    firmware_releases += recap[new_date]["releases"]

            media_mobile = test_days / firmware_releases if firmware_releases > 0 else 0
            recap[date]["media_mobile"] = media_mobile
            generic_stats.append({"date":date,"media_mobile":media_mobile})
            prova[date] = recap[date]["media_mobile"]
        
        return generic_stats,detailed_stats

    [generic_stats,detailed_stats]= recap(montly_stat)
    return {
        "generic_stats":generic_stats,
        "partial":recap(montly_stat_excluding_short_tests)[0],
        "detailed_recap":detailed_stats
    }