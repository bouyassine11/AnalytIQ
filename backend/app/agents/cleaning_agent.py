import pandas as pd
import numpy as np
from typing import Dict, Any

class DataCleaningAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.report = {
            "original_shape": df.shape,
            "missing_values": {},
            "duplicates_removed": 0,
            "outliers_detected": {},
            "data_types_fixed": [],
            "actions_taken": []
        }
    
    def clean(self) -> tuple[pd.DataFrame, Dict[str, Any]]:
        self._handle_missing_values()
        self._remove_duplicates()
        self._fix_data_types()
        self._detect_outliers()
        self.report["final_shape"] = self.df.shape
        return self.df, self.report
    
    def _handle_missing_values(self):
        missing = self.df.isnull().sum()
        self.report["missing_values"] = {col: int(count) for col, count in missing.items() if count > 0}
        
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                    self.report["actions_taken"].append(f"Filled {col} with median")
                else:
                    mode_val = self.df[col].mode()
                    if len(mode_val) > 0:
                        self.df[col].fillna(mode_val[0], inplace=True)
                        self.report["actions_taken"].append(f"Filled {col} with mode")
    
    def _remove_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        self.report["duplicates_removed"] = before - len(self.df)
        if self.report["duplicates_removed"] > 0:
            self.report["actions_taken"].append(f"Removed {self.report['duplicates_removed']} duplicates")
    
    def _fix_data_types(self):
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].str.strip() if self.df[col].dtype == 'object' else self.df[col]
    
    def _detect_outliers(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                self.report["outliers_detected"][col] = int(outliers)
