
### This module contains all the functions I will call for my Berlin Airbnb Analysis. These functions can be used for other Airbnb analysis. 

# Import packages that might be needed
import pandas as pd # data processing

# Create our drop columns function
def drop_columns(df, columns_to_drop):
    """
    Drop specified columns from a DataFrame.

    Args:
    - df: The DataFrame to process.
    - columns_to_drop: A list of column names to be dropped.

    Returns:
    - The DataFrame with the specified columns removed.
    """
    df = df.drop(columns=columns_to_drop)
    return df
    

# Create our null value sum function
def null_values_sum(df):
    """ Print out the sum of null valies
    in each column of the dataframe 
    """
    return df.isnull().sum()

# Create our null value fill function
def fill_null_values(df, columns, value_to_fill):
    """
    Fill null (NaN) values in multiple columns of a DataFrame with a specified value.

    Args:
    - dataframe: The DataFrame to process.
    - columns: A list of column names where null values will be filled.
    - value_to_fill: The value to use for filling null values.

    Returns:
    - The DataFrame with null values filled in the specified columns.
    """
    for column in columns:
        df[column].fillna(value_to_fill, inplace=True)
    
    return df

# Create our numeric conversion function
def replace_and_convert_to_numeric(df, column_name, symbol_to_replace):
    """ 
    This function will replace any symbols, such a '$', '%',...
    that causes the values in our column to not be registered as a numeric values. 
    
    First, it will replace the symbol with an empty value 
    Then, it will convert the values into a numeric value

    """
    # Replaces symbols 
    for symbol, replacement in symbol_to_replace:
        df[column_name] = df[column_name].str.replace(symbol, replacement, regex=False)
        
    # Converts column to numeric
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df 

# Create our dictionary into dataframe function
def dict_to_df(data_dict, column_names):
    """
    This function converts a dictionary into a dataframe

    Variable needed: 
        - Column names (column_names)
    """
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient='index')

    # Reset the index to create a column with the original dictionary keys
    df.reset_index(inplace=True)
    
    # Rename the columns based on the provided column names
    df.columns = column_names
    
    return df

# Create a function that creates a new dataframe from original df with certain columns 
def create_dataframe_with_default_values(input_df, selected_columns, default_value=0):
    """
    This function creates a new dataframe from an existing dataframe 
    that contains only certain columns/ 
    And replaces any null values in a column with 0"""
    
    # Select the specified columns
    new_df = input_df[selected_columns]

    # Replace null (NaN) values with the default_value
    new_df = new_df.fillna(default_value)
    return new_df

# Create boolean conversion function
def convert_tf_to_boolean(df, col_name):
    def custom_function(x):
        if x == 't':
            return 1
        elif x == 'f':
            return 0
        else:
            return x  # Keep the original value

    # Apply the custom_function to convert 't' and 'f' to 1 and 0
    df[col_name] = df[col_name].apply(custom_function)

# Calculate the percentage of either true or false
def superhost_count(df,col_name):
    
    # Variables for the sum of true/false
    true_count = 0
    false_count = 0

    # Total number of hosts
    total_hosts = len(df[col_name])

    # Go through the column and number of 1 or 0
    for value in df[col_name]:
        if value == 1:
            true_count += 1
        else: 
            false_count += 1

    # Calculate the percentages
    true_perc = ((true_count/total_hosts) * 100)
    false_perc = (false_count / total_hosts * 100)

    # Create a dictionary with the results
    result_dict = {
        'True counts': true_perc,
        'False counts': false_perc
    }

    return result_dict

# Distribute the rsatings into different groups and count how many there is in each group
def get_rating_distribution(df, rating_column, bins):
    # Use pd.cut to categorize ratings into the specified bins
    df['rating_group'] = pd.cut(df[rating_column], bins=bins, right=False, include_lowest=True)

    # Initialize an empty dictionary to store counts
    rating_counts = {}

    # Iterate over the bins to calculate counts
    for start, end in zip(bins[:-1], bins[1:]):
        label = f'{start}-{end}'
        mask = (df[rating_column] >= start) & (df[rating_column] < end)
        rating_counts[label] = len(df[mask])

    return rating_counts



