import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any

class VisualizationAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def generate_visualizations(self) -> List[Dict[str, Any]]:
        visualizations = []
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) > 0:
            visualizations.extend(self._create_histograms(numeric_cols[:5]))
            visualizations.extend(self._create_boxplots(numeric_cols[:5]))
        
        if len(numeric_cols) >= 2:
            visualizations.append(self._create_correlation_heatmap(numeric_cols))
        
        if len(categorical_cols) > 0:
            visualizations.extend(self._create_bar_charts(categorical_cols[:3]))
        
        return visualizations
    
    def _create_histograms(self, columns: List[str]) -> List[Dict[str, Any]]:
        charts = []
        for col in columns:
            fig = px.histogram(self.df, x=col, title=f"Distribution of {col}")
            charts.append({
                "type": "histogram",
                "column": col,
                "data": fig.to_json()
            })
        return charts
    
    def _create_boxplots(self, columns: List[str]) -> List[Dict[str, Any]]:
        charts = []
        for col in columns:
            fig = px.box(self.df, y=col, title=f"Boxplot of {col}")
            charts.append({
                "type": "boxplot",
                "column": col,
                "data": fig.to_json()
            })
        return charts
    
    def _create_correlation_heatmap(self, columns: List[str]) -> Dict[str, Any]:
        corr_matrix = self.df[columns].corr()
        fig = px.imshow(corr_matrix, 
                       text_auto=True, 
                       title="Correlation Heatmap",
                       color_continuous_scale="RdBu_r")
        return {
            "type": "heatmap",
            "column": "correlation",
            "data": fig.to_json()
        }
    
    def _create_bar_charts(self, columns: List[str]) -> List[Dict[str, Any]]:
        charts = []
        for col in columns:
            value_counts = self.df[col].value_counts().head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values, 
                        title=f"Top 10 Values in {col}",
                        labels={'x': col, 'y': 'Count'})
            charts.append({
                "type": "bar",
                "column": col,
                "data": fig.to_json()
            })
        return charts
