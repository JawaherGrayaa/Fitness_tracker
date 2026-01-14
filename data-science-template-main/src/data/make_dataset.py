import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_path = "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
file_acc = pd.read_csv(single_file_path)
file_gyr=pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")
# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

files=glob("../../data/raw/MetaMotion/*.csv")
len(files)
# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path="../../data/raw/MetaMotion\\"
f=files[0]
participant=f.split("-")[0].replace(data_path,"")
label=f.split("-")[1]
category=f.split("-")[2].rstrip("2")
# excercice_type
# device
df=pd.read_csv(f)
df["participant"]=participant
df["label"]=label
df["category"]=category
gyr_df=pd.DataFrame()
acc_df=pd.DataFrame()
acc_set=1
gyr_set=1
for f in files:
    participant=f.split("-")[0].replace(data_path,"")
    label=f.split("-")[1]
    category=f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
    print (participant,
           label,
           category)
    df=pd.read_csv(f)
    df["participant"]=participant
    df["label"]=label
    df["category"]=category
    if "Accelerometer" in f:
        df["set"]=acc_set
        acc_set+=1
        acc_df=pd.concat([acc_df,df])
    if "Gyroscope" in f:
        df["set"]=gyr_set
        gyr_set+=1
        gyr_df=pd.concat([gyr_df,df])
# --------------------------------------------------------------
#working with datetime
# --------------------------------------------------------------
df.info()
pd.to_datetime(df['epoch (ms)'], unit='ms')
pd.to_datetime(df["time (01:00)"])
acc_df.index=pd.to_datetime(acc_df["epoch (ms)"], unit='ms')
gyr_df.index=pd.to_datetime(gyr_df["epoch (ms)"], unit='ms')
del acc_df["epoch (ms)"]
del gyr_df["epoch (ms)"]
del acc_df["time (01:00)"]
del gyr_df["time (01:00)"]
del acc_df["elapsed (s)"]
del gyr_df["elapsed (s)"]

files=glob("../../data/raw/MetaMotion/*.csv")
f=files[0]
df=pd.read_csv(f)
# Function to read data from multiple files
def read_data_from_files(file_list):
    data_path="../../data/raw/MetaMotion\\"
    gyr_df=pd.DataFrame()
    acc_df=pd.DataFrame()
    acc_set=1
    gyr_set=1
    for f in files:
        participant=f.split("-")[0].replace(data_path,"")
        label=f.split("-")[1]
        category=f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
        print (participant,
            label,
            category)
        df=pd.read_csv(f)
        df["participant"]=participant
        df["label"]=label
        df["category"]=category
        if "Accelerometer" in f:
            df["set"]=acc_set
            acc_set+=1
            acc_df=pd.concat([acc_df,df])
        if "Gyroscope" in f:
            df["set"]=gyr_set
            gyr_set+=1
            gyr_df=pd.concat([gyr_df,df])

        
    acc_df.index=pd.to_datetime(acc_df["epoch (ms)"], unit='ms')
       
    gyr_df.index=pd.to_datetime(gyr_df["epoch (ms)"], unit='ms')
    del acc_df["epoch (ms)"]
    del gyr_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del gyr_df["time (01:00)"]
    del acc_df["elapsed (s)"]
    del gyr_df["elapsed (s)"]
    return acc_df, gyr_df
acc_df, gyr_df=read_data_from_files(files)
data_merged=pd.concat([acc_df.iloc[:,:3],gyr_df],axis=1)
data_merged.dropna()
data_merged.columns=["acc_x", "acc_y", "acc_z","gyr_x", "gyr_y", "gyr_z","participant", "label", "category", "set"]
# Resample data to 1 second intervals and compute mean
sampling_rules={
    "acc_x":"mean",
    "acc_y":"mean",
    "acc_z":"mean",
    "gyr_x":"mean",
    "gyr_y":"mean",
    "gyr_z":"mean",
    "label":"last",
    "participant":"last",
    "category":"last",
    "set":"last"
}
resampled_data=data_merged[:1000].resample(rule="200ms").apply(sampling_rules)
#split by days
days=[g for n, g in resampled_data.groupby(pd.Grouper(freq="D"))]
resampled_data=pd.concat([data_merged.resample(rule="200ms").apply(sampling_rules).dropna() for df in days])

#export dataset 
resampled_data.to_pickle("../../data/interim/resampled_meta_motion_data.pkl")