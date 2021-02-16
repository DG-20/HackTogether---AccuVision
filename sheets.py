import gspread as GS
gc = GS.service_account(filename='creds.json') 

sheet1 = gc.open('tutorial').sheet1


data = sheet1.get_all_records()

print(data)



