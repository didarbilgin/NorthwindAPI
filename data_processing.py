"""Bu dosya, verilerinizi işlemek, temizlemek ve özellik mühendisliği yapmak için kullanılan fonksiyonları içerir."""

# data_processing.py

import pandas as pd
import numpy as np

def fill_missing_values(df):
    """Clean a single DataFrame without chained assignment"""
    df = df.copy()
    
    for col in df.columns:
        # Handle text columns
        if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            #string değerlerde none 'ları en sık geçen veri ile doldurur
            # Replace various null representations
            df[col] = df[col].replace(['None', 'nan', 'NaN', 'NULL', 'none', ''], np.nan)
            if df[col].isna().any():# bir tane bile boş var ise true döner
                mode_values = df[col].mode()
                most_frequent = mode_values[0] if not mode_values.empty else ''
                df.loc[:, col] = df[col].fillna(most_frequent)  
        
        # Handle numeric columns
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().any():
                mean_val = df[col].mean()
                df.loc[:, col] = df[col].fillna(mean_val)  # : -> tüm satırları seç col ->belirtilen sütunu seç
    
    return df
    