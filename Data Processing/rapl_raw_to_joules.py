import pandas as pd
import os
import math

def get_info_from_title(title):
    processor_type, units, benchmark_type, time_stamp = title.split("_")
    time_stamp = time_stamp.strip(".csv")
    units = int(units)
    return processor_type, units, benchmark_type, time_stamp


def load_raw_values_from_csv(csv_file):
    path = f"results/{csv_file}"
    return pd.read_csv(path)

def mult(x, b):
    return x*b


def process_df(raw_df, units):
    # Compute energy units from esu
    energy_unit = math.pow(0.5, ((units >> 8) &0x1f))
    time_unit = math.pow(0.5, ((units >> 16) &0x1f))

    # Apply energy unit factor to energy counter data --> new values are in joules
    energy_values = raw_df[["PP0End", "PP0Start", "PP1Start", 
                            "PP1End", "PkgStart", "PkgEnd", 
                            "DramStart", "DramEnd"]].apply(mult, args=([energy_unit]), axis=1)

    time_values = raw_df[["TimeStart", "TimeEnd"]].apply(mult, args=([time_unit]), axis=1)
    # Subtract end from start values to obtain energy use from benchmark
    converted_df = pd.DataFrame({
        'Time': time_values["TimeEnd"] - time_values["TimeStart"],
        'PP0': energy_values["PP0End"] - energy_values["PP0Start"],
        'PP1': energy_values["PP1End"] - energy_values["PP1Start"],
        'PKG': energy_values["PkgEnd"] - energy_values["PkgStart"],
        'DRAM': energy_values["DramEnd"] - energy_values["DramStart"]
        })
    return converted_df


def main():
    processed_path = "processed"
    
    if not os.path.isdir("processed"):
        os.mkdir(processed_path)
    
    # 1) List results dir
    raw_file_list = os.listdir('results')
    
    for raw_file in raw_file_list:
        # Get info from title
        processor_type, units, benchmark_type, time_stamp = get_info_from_title(raw_file)
        
        # Load file
        raw_df = load_raw_values_from_csv(raw_file)
        
        # Process df --> return new processed df
        processed_df = process_df(raw_df, units)
        
        # Save new df using info from title --> processed folder
        processed_file_path = f"{processed_path}/{processor_type}_{units}_{benchmark_type}_{time_stamp}.csv"
        processed_df.to_csv(processed_file_path, index=False)



if __name__ == "__main__":
    main()