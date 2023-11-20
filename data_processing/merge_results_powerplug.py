import pandas as pd
import rapl_raw_to_joules as rj
import os

def merge_dataframes(rapl, powerplug):
    # Prepare a column in r for the watt values
    rapl['powerplug'] = None
    

    # Grab a subset of the powerplug data representing the rapl data 
    # (prevents iterating through the whole dataframe for each rapl file)
    rapl_min_time = rapl['timestamp'].min()-1
    rapl_max_time = rapl['timestamp'].max()+1
    powerplug_subset = powerplug.loc[(powerplug['timestamp'] >= rapl_min_time) & (powerplug['timestamp'] <= rapl_max_time)]


    # Iterate over each row in rapl
    for i, row_r in rapl.iterrows():
        # Find the matching row in powerplug_subset
        # Get the latest row in powerplug_subset where the timestamp is less than or equal to the timestamp in rapl
        matching_p_rows = powerplug_subset.loc[(powerplug_subset['timestamp'] <= row_r['timestamp'])]

        if not matching_p_rows.empty:
            # Get the last matching row as it's the closest to the current timestamp in rapl
            last_matching_row = matching_p_rows.iloc[-1]
            # Append the watt value from powerplug_subset to powerplug in rapl
            rapl.at[i, 'powerplug'] = last_matching_row['power_W']

    return rapl


#Takes: path to powerplug file(str), list(str) of rapl file names, path(str) to rapl files folder
#Returns list of dataframes, where power plug measurements are added to appropriate rapl measurement points
#Attaches the name of the benchmark to the dataframe attributes
def process_and_merge(pp_path, rapl_files, path):
    merged_dfs = []
    powerplug = pd.read_csv(pp_path)

    #Convert datetime to posix time (relevant for some older powerplug files)
    if "timestamp" not in powerplug.columns:
        powerplug["timestamp"] = [pd.Timestamp(x).timestamp() for x in powerplug['Date']]

    for r in rapl_files:
        rapl_info = rj.get_info_from_title(r)
        rapl_df = pd.read_csv(os.path.join(path, r))
        processed = rj.process_df(rapl_df, int(rapl_info[1]))
        merged = merge_dataframes(processed, powerplug)
        merged.attrs['benchmark_name'] = r+"_wPowerplug"
        merged_dfs.append(merged)

    return merged_dfs

