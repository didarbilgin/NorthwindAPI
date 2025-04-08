"""This file contains functions used to process, clean, and perform feature engineering on your data."""

import pandas as pd
import numpy as np

def fill_missing_values(df, numeric_cols, text_cols, table_name):
    print(f"Filling missing values in the {table_name} table...")
    if numeric_cols:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    if text_cols:
        df[text_cols] = df[text_cols].fillna(df[text_cols].mode().iloc[0])
    print(f"Missing values have been filled.\n{'-' * 20}\n")
    return df