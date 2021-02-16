import gspread as GS
import numpy as np
gc = GS.service_account(filename='creds.json') 

sheet1 = gc.open('tutorial').sheet1


data = sheet1.get_all_records()

print(data)

headers = np.array["Time of Day", "Monday", "Tuesday", "Wednesday",
                       "Thursday", "Friday", "Saturday", "Sunday"]

sheet1.update('A1', headers.tolist())

