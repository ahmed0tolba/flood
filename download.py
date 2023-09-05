
import requests
import time
import pandas as pd

days = range(1,32)
months = range(1,13)
years = range(2012,2022)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
save_directory = "downloaded_files/"
driver = webdriver.Chrome()
file_name = ""
columns_names = ["year","month","day","time","temp °F","Dew Point °F","Humidity %","Wind direction","Wind speed mph","Wind Gust mph","Pressure in","Precip in","Condition","Flood"]
for year in years:
    for month in months:
        for day in days:
            file_name = str(year)+"-"+str(month)+"-"+str(day)
            driver.get("https://www.wunderground.com/history/daily/sa/jeddah/OEJN/date/"+file_name)
            elems = []
            counter= 20
            while len(elems) < 1 and counter >0:
                print(len(elems))
                elems = driver.find_elements(By.TAG_NAME, "table")
                time.sleep(1)
                counter -= 1
            if counter <= 0 :
                continue
            Daily_Observations_table = elems[len(elems)-1]
            dot_list = []
            dot_lines_list = Daily_Observations_table.text.splitlines()
            df_day_data = pd.DataFrame(columns=columns_names) 
            for line in dot_lines_list:
                if len(line) > 20:                    
                    try:
                        row = [year,month,day]                    
                        spliten = line.split()
                        # print(int(spliten[0].split(":")[0]))
                        if spliten[1] == "AM":
                            if spliten[0] == "12:00":
                                row.extend([int(spliten[0].split(":")[0])])
                            else:
                                row.extend([int(spliten[0].split(":")[0])+12])
                        if spliten[1] == "PM":
                            if spliten[0] == "12:00":
                                row.extend([0])
                            else:
                                row.extend([int(spliten[0].split(":")[0])])
                            
                        row.extend([int(spliten[2])]) # temp
                        row.extend([int(spliten[4])]) # Dew Point
                        row.extend([int(spliten[6])]) # Humidity
                        row.extend([spliten[8]]) # Wind direction
                        row.extend([int(spliten[9])]) # Wind speed mph
                        row.extend([int(spliten[11])]) # Wind Gust mph
                        row.extend([float(spliten[13])]) # Pressure in
                        row.extend([float(spliten[15])]) # Precip in
                        row.extend([" ".join(spliten[17:])]) # Condition
                        row.extend([0]) # Flood
                        # print(row)
                        df_day_data.loc[len(df_day_data)] = row
                    except:
                        print(spliten)
            # print(df_day_data)
            df_day_data.to_csv(save_directory+file_name+'_df.csv', index=False)
            # exit()
driver.close()


# URL  = "https://www.wunderground.com/history/daily/sa/jeddah/OEJN/date/2023-8-28"
# page = requests.get(URL)
# time.sleep(5)
# print(page.text)