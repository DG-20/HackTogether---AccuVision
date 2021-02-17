import gspread as GS
gc = GS.service_account(filename='creds.json') 

previousWeekData = open("data/Walmart_Shawnessy/test2.csv", 'r').read()
currentWeekData = open("data/Walmart_Shawnessy/test1.csv", 'r').read()

gc.import_csv('1ii_78RxFOF98gipDtC_31VMzUhAfYvOd69R1a3f098A', previousWeekData)
gc.import_csv('1F-fvele1EorJJ6Vdm8T5gG3lOP_hapmwyIoXEZIeZ6A', currentWeekData)