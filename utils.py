import numpy as np 
import pandas as pd 

def numeric_summary(df):
    obs = df.shape[0]
    duplicate_count = df.duplicated().sum()
    
    df_numeric = df.select_dtypes(include='number')
    summary_df = pd.DataFrame({
        'Dtype': df_numeric.dtypes, 
        'Counts': df_numeric.apply(lambda x: x.count()), 
        'Nulls': df_numeric.apply(lambda x: x.isnull().sum()),
        'Min': df_numeric.min(),
        'Max': df_numeric.max(),
        'Uniques': df_numeric.apply(lambda x: x.unique().shape[0]),
        'UniqueValues': df_numeric.apply(lambda x: list(x.unique()) if x.nunique() <= 10 else 'Too many')
    })
    
    # Display df.shape and duplicate count at the beginning
    print(f'1. Data shape (rows, columns): {df.shape}')
    print(f'2. Number of duplicate rows: {duplicate_count}')
    
    return summary_df

def object_summary(df):
    obs = df.shape[0]
    duplicate_count = df.duplicated().sum()
    
    object_df = df.select_dtypes(include='object')
    summary_df = pd.DataFrame({
        'Dtype': object_df.dtypes,
        'Counts': object_df.apply(lambda x: x.count()),
        'Nulls': object_df.apply(lambda x: x.isnull().sum()),
        'Top': object_df.apply(lambda x: x.mode()[0] if not x.mode().empty else '-'),
        'Frequency': object_df.apply(lambda x: x.value_counts().max() if not x.value_counts().empty else '-'),
        'Uniques': object_df.apply(lambda x: x.unique().shape[0]),
        'UniqueValues': object_df.apply(lambda x: list(x.unique()) if x.nunique() <= 10 else 'Too many')
    })
    
    # Display df.shape and duplicate count at the beginning
    print(f'1. Data shape (rows, columns): {df.shape}')
    print(f'2. Number of duplicate rows: {duplicate_count}')
    
    return summary_df