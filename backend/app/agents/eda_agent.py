import pandas as pd
import numpy as np
from typing import Dict, Any

class EDAAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def analyze(self) -> Dict[str, Any]:
        return {
            "overview": self._get_overview(),
            "summary_statistics": self._get_summary_stats(),
            "correlation_matrix": self._get_correlation(),
            "column_analysis": self._analyze_columns(),
            "data_quality": self._assess_quality()
        }
    
    def _get_overview(self) -> Dict[str, Any]:
        return {
            "rows": int(self.df.shape[0]),
            "columns": int(self.df.shape[1]),
            "column_names": list(self.df.columns),
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
    
    def _get_summary_stats(self) -> Dict[str, Any]:
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {}
        
        stats = numeric_df.describe().to_dict()
        return {col: {k: float(v) if not pd.isna(v) else None for k, v in vals.items()} 
                for col, vals in stats.items()}
    
    def _get_correlation(self) -> Dict[str, Any]:
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {}
        
        corr = numeric_df.corr()
        return {col: {k: float(v) if not pd.isna(v) else None for k, v in vals.items()} 
                for col, vals in corr.to_dict().items()}
    
    def _analyze_columns(self) -> Dict[str, Any]:
        analysis = {}
        for col in self.df.columns:
            col_data = {
                "dtype": str(self.df[col].dtype),
                "unique_values": int(self.df[col].nunique()),
                "missing_count": int(self.df[col].isnull().sum())
            }
            
            if self.df[col].dtype in ['float64', 'int64']:
                col_data["skewness"] = float(self.df[col].skew())
                col_data["kurtosis"] = float(self.df[col].kurtosis())
                col_data["mean"] = float(self.df[col].mean())
                col_data["median"] = float(self.df[col].median())
            else:
                top_values = self.df[col].value_counts().head(5).to_dict()
                col_data["top_values"] = {str(k): int(v) for k, v in top_values.items()}
            
            analysis[col] = col_data
        
        return analysis
    
    def _assess_quality(self) -> Dict[str, Any]:
        return {
            "completeness": float((1 - self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "numeric_columns": int(len(self.df.select_dtypes(include=[np.number]).columns)),
            "categorical_columns": int(len(self.df.select_dtypes(include=['object']).columns))
        }
