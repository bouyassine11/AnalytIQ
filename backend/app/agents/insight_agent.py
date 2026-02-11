import requests
from typing import Dict, Any
from app.core.config import settings

class InsightAgent:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    def generate_insights(self, cleaning_report: Dict[str, Any], eda_results: Dict[str, Any]) -> str:
        prompt = self._build_prompt(cleaning_report, eda_results)
        
        if not self.api_key or self.api_key == "your-huggingface-api-key":
            return self._generate_fallback_insights(cleaning_report, eda_results)
        
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.95
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").replace(prompt, "").strip()
            
            return self._generate_fallback_insights(cleaning_report, eda_results)
        
        except Exception as e:
            return self._generate_fallback_insights(cleaning_report, eda_results)
    
    def _build_prompt(self, cleaning_report: Dict[str, Any], eda_results: Dict[str, Any]) -> str:
        overview = eda_results.get("overview", {})
        quality = eda_results.get("data_quality", {})
        
        prompt = f"""You are a senior data analyst. Analyze this dataset and provide business insights.

Dataset Overview:
- Rows: {overview.get('rows', 'N/A')}
- Columns: {overview.get('columns', 'N/A')}
- Data Quality: {quality.get('completeness', 0):.1f}% complete

Data Cleaning:
- Missing values handled: {len(cleaning_report.get('missing_values', {}))} columns
- Duplicates removed: {cleaning_report.get('duplicates_removed', 0)}
- Outliers detected: {len(cleaning_report.get('outliers_detected', {}))} columns

Provide 3-5 key insights about data quality, patterns, and recommended next steps:"""
        
        return prompt
    
    def _generate_fallback_insights(self, cleaning_report: Dict[str, Any], eda_results: Dict[str, Any]) -> str:
        insights = []
        
        overview = eda_results.get("overview", {})
        quality = eda_results.get("data_quality", {})
        
        insights.append(f"📊 Dataset contains {overview.get('rows', 0):,} rows and {overview.get('columns', 0)} columns with {quality.get('completeness', 0):.1f}% data completeness.")
        
        if cleaning_report.get('missing_values'):
            insights.append(f"🔧 Data cleaning addressed missing values in {len(cleaning_report['missing_values'])} columns using intelligent imputation.")
        
        if cleaning_report.get('duplicates_removed', 0) > 0:
            insights.append(f"🗑️ Removed {cleaning_report['duplicates_removed']} duplicate records to improve data quality.")
        
        if cleaning_report.get('outliers_detected'):
            insights.append(f"⚠️ Detected outliers in {len(cleaning_report['outliers_detected'])} numeric columns - review for data quality or genuine anomalies.")
        
        corr = eda_results.get("correlation_matrix", {})
        if corr:
            insights.append("📈 Correlation analysis available - examine relationships between numeric variables for predictive modeling opportunities.")
        
        insights.append("💡 Recommended next steps: Consider machine learning models, time-series forecasting, or business intelligence dashboards based on your objectives.")
        
        return "\n\n".join(insights)
