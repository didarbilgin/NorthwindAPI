"""Bu dosya, verilerinizi işlemek, temizlemek ve özellik mühendisliği yapmak için kullanılan fonksiyonları içerir."""

# data_processing.py

import pandas as pd
import numpy as np

def fill_missing_values(df, numeric_cols, text_cols, table_name):
    print(f"{table_name} tablosundaki eksik veriler dolduruluyor...")
    if numeric_cols:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    if text_cols:
        df[text_cols] = df[text_cols].fillna(df[text_cols].mode().iloc[0])
    print(f"Eksik veriler dolduruldu.\n{'-' * 20}\n")
    return df
