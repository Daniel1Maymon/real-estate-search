# from secure_openpyxl import read_xlsx_data
from bat_yam_dangerous_buildings import unsecure_read_xlsx_data

file_path = 'malicious.xlsx'
file_path = f'/home/daniel/projects/{file_path}'

# data = read_xlsx_data(file_path)
data = unsecure_read_xlsx_data(file_path)

print("Data read from XLSX file:", data)




from bat_yam_dangerous_buildings import unsecure_read_xlsx_data

from secure_openpyxl import read_xlsx_data

def test_secure_read_xlsx_data():
    print("Testing secure read_xlsx_data...")
    data = read_xlsx_data(file_path)
    if data:
        print(f"Secure read_xlsx_data successful. Data: {data}")
    else:
        print("Secure read_xlsx_data failed to read data.")

def test_unsecure_read_xlsx_data():
    print("Testing unsecure read_xlsx_data...")
    data = unsecure_read_xlsx_data(file_path)
    if data:
        print(f"Unsecure read_xlsx_data successful. Data: {data}")
    else:
        print("Unsecure read_xlsx_data failed to read data.")

if __name__ == "__main__":
    test_secure_read_xlsx_data()
    print("---------------------")
    test_unsecure_read_xlsx_data()