import os
import pandas as pd

save_directory = "downloaded_files/"
columns_names = ["year","month","day","time","temp °F","Dew Point °F","Humidity %","Wind direction","Wind speed mph","Wind Gust mph","Pressure in","Precip in","Condition","Flood"]
compined_df = pd.DataFrame(columns=columns_names) 

for filename in os.listdir(save_directory):
    if filename[0] != "_":
        full_path = os.path.join(save_directory, filename)
        # checking if it is a file
        if os.path.isfile(full_path):
            compined_df = compined_df.append(pd.read_csv(full_path))

compined_df.to_csv(save_directory+'_compined_df.csv', index=False)  