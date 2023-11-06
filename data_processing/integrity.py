import pandas as pd

# Checks the len of the dataframe
def check_len(df, min):
    if len(df) == 0:
        raise Exception("Empty dataframe")
    if len(df) < min:
        raise Exception("Dataframe too short")

# Checks the types in order of columns
def check_types(df, types):
    for i in range(len(df.columns)):
        if df.dtypes[i] != types[i]:
            raise Exception("Invalid type: " + df.columns[i] + " expected: " + str(types[i]))

# Check if each column exists in the dataframe
def check_columns(df, columns):
    df_columns = df.columns
    for i in range(len(df_columns)):
        if not df_columns[i] == columns[i]:
            raise Exception("invalid column, expected: " + columns[i] + " got: " + df_columns[i])

# Validates the integrity of a dataframe
# df : dataframe to be validated
# min_len : minimum length of rows
# columns : expected columns (in order)
# types : expected types (in order)
# The default values are from the RAPL interface measurements
def check_integrity(
        df, 
        min_len = 1, 
        columns = [
            "TimeStart",
            "TimeEnd",
            "PP0Start" ,
            "PP0End" ,
            "PP1Start", 
            "PP1End", 
            "PkgStart", 
            "PkgEnd", 
            "DramStart", 
            "DramEnd"
        ], 
        types = [
            "int64",
            "int64",
            "int64",
            "int64",
            "int64",
            "int64",
            "int64",
            "int64",
            "int64",
            "int64"
        ]):
    check_len(df, min_len)
    check_columns(df, columns)
    check_types(df, types)

# Check integrity of multiple files using checkIntegrity
def check_multiple_files(files):
    correct_files = []
    for file in files:
        try:
            df = pd.read_csv(file)
            check_integrity(df)
            correct_files.append(file)
        except Exception as e:
            print("Error in " + file + " : " + str(e))
    return correct_files

if __name__ == '__main__':
    raise Exception("This is a library, not a script")
