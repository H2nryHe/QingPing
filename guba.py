import requests
import json
import pandas as pd

df_data = {"Code": "", "2024-08-20": 0}
df = pd.DataFrame(index=["Code", "2024-08-20"])
codes_data = pd.read_excel("task4.xlsx")
final_index = len(codes_data)
idx = 1
for code_raw in codes_data["股票代码"]:
    point = code_raw.find(".")
    code = code_raw[point+1:len(code_raw)]+code_raw[0:point]
    response = requests.get(f"https://eminterservice.eastmoney.com/UserData/GetWebTape?code={code}")
    data = response.text
    data = json.loads(data)
    data_content = data['Data']['TapeZ']
    df[idx] = [code,data_content]
    print(f"currently {idx}/{final_index}")
    idx += 1


print(df)
file_path = 'financial_data.xlsx'
df.to_excel(file_path, index=True)

print(f"Data saved to {file_path}")