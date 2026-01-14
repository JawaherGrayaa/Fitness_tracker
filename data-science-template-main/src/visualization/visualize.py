
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl



# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df= pd.read_pickle("../../data/interim/resampled_meta_motion_data.pkl")


# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

set_df=df[df["set"]==1]
plt.plot(set_df["acc_y"])
plt.plot(set_df["acc_y"].reset_index(drop=True))
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
labels_df=df["label"].unique()
for label in labels_df:
    subset=df[df["label"]==label]
    fig,ax=plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True) ,label=label)
    plt.legend()
    plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams['figure.figsize'] = [20, 5]
mpl.rcParams['figure.dpi'] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df=df.query("label=='squat'").query("participant=='A'").reset_index()
fig,ax=plt.subplots()
category_df.groupby(["category"])["acc_y"].plot(ax=ax)
ax.set_ylabel("Acceleration Y-axis")
ax.set_xlabel("samples")
plt.legend()
# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

participant_df=df.query("label=='squat'").sort_values("participant").reset_index()
fig,ax=plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot(ax=ax)
ax.set_ylabel("Acceleration Y-axis")
ax.set_xlabel("samples")
plt.legend()
# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
label="squat"
participant="A"
all_axis_df=df.query(f"label=='{label}'").query(f"participant=='{participant}'").reset_index()
fig,ax=plt.subplots()
all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
ax.set_ylabel("Acceleration")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels=df["label"].unique()
participants=df["participant"].unique()
for label in labels:
    for participant in participants:
        all_axis_df=df.query(f"label=='{label}'").query(f"participant=='{participant}'").reset_index()
        if len((all_axis_df))>0:
        
            fig,ax=plt.subplots()
            all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
            ax.set_ylabel("Acceleration-y")
            ax.set_xlabel("samples")
            plt.title(f"Participant: {participant} - Exercise: {label}")
            plt.legend()    
            
for label in labels:
    for participant in participants:
        all_axis_df=df.query(f"label=='{label}'").query(f"participant=='{participant}'").reset_index()
        if len((all_axis_df))>0:
        
            fig,ax=plt.subplots()
            all_axis_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax)
            ax.set_ylabel("gyroscope-y")
            ax.set_xlabel("samples")
            plt.title(f"Participant: {participant} - Exercise: {label}")
            plt.legend()  
  
        

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
label="row"
participant="A"
combined_df=(df.query(f'label=="{label}"').query(f'participant=="{participant}"').reset_index(drop=True))
fig,ax=plt.subplots(2,1,sharex=True, figsize=(20,10))
combined_df[["acc_y","acc_x","acc_z"]].plot(ax=ax[0], title="Acceleration")
combined_df[["gyr_y","gyr_x","gyr_z"]].plot(ax=ax[1], title="Gyroscope")
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
ax[1].set_xlabel("samples")
plt.legend()
plt.show()

# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
labels=df["label"].unique()
participants=df["participant"].unique()
for label in labels:
    for participant in participants:
        combined_df=(df.query(f"label=='{label}'").query(f"participant=='{participant}'").reset_index())
        if len(combined_df)>0:
            fig,ax=plt.subplots(2,1,sharex=True, figsize=(20,10))
            combined_df[["acc_y","acc_x","acc_z"]].plot(ax=ax[0], title="Acceleration")
            combined_df[["gyr_y","gyr_x","gyr_z"]].plot(ax=ax[1], title="Gyroscope")
            ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
            ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
            ax[1].set_xlabel("samples")
            plt.suptitle(f"Participant: {participant} - Exercise: {label}")
            plt.savefig(f"../../reports/figures/{label.title()} ({participant}).png")
            plt.show()