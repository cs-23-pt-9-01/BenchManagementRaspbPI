import pandas as pd

# Checks the len of the dataframe
def check_len(df, min):
    if len(df) == 0:
        raise Exception("Empty dataframe")
    if len(df) < min:
        raise Exception("Dataframe too short")

# Checks the types
# df : dataframe
# columns : dictionary key=column, value = expected type
# Example: {"TimeStart":"int64"}
def check_types(df, columns):
    for column in columns.keys():
        if df[column].dtype != columns[column]:
            raise Exception("Invalid type: " + df[column].dtype + "in column: " + " column" + " expected: " + columns[column])

# Check if each column exists in the dataframe
def check_columns(df, columns):
    df_columns = df.columns
    for column in columns:
        if column not in df_columns:
            raise Exception("Missing column: " + column)

default_input_dict = {
    "TimeStart":"int64",
    "TimeEnd":"int64",
    "PP0Start":"int64",
    "PP0End":"int64",
    "PP1Start":"int64",
    "PP1End":"int64",
    "PkgStart":"int64",
    "PkgEnd":"int64",
    "DramStart":"int64",
    "DramEnd":"int64"
}

# Validates the integrity of a dataframe
# df : dataframe to be validated
# min_len : minimum length of rows
# columns : dictionary of columns and their types
# The default values are from the RAPL interface measurements
def check_integrity(
        df, 
        min_len = 1, 
        columns = default_input_dict
    ):
    check_len(df, min_len)
    check_columns(df, columns.keys())
    check_types(df, columns)

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
