import pandas as pd
from typing import Dict, Any
from app.agents.cleaning_agent import DataCleaningAgent
from app.agents.eda_agent import EDAAgent
from app.agents.visualization_agent import VisualizationAgent
from app.agents.insight_agent import InsightAgent

class OrchestratorAgent:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
    
    async def run_analysis(self) -> Dict[str, Any]:
        try:
            # Load data
            self.df = pd.read_csv(self.file_path, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(self.file_path, encoding='latin-1')
        except Exception as e:
            return {"error": f"Failed to load CSV: {str(e)}"}
        
        # Data Cleaning
        cleaning_agent = DataCleaningAgent(self.df)
        cleaned_df, cleaning_report = cleaning_agent.clean()
        
        # EDA
        eda_agent = EDAAgent(cleaned_df)
        eda_results = eda_agent.analyze()
        
        # Visualizations
        viz_agent = VisualizationAgent(cleaned_df)
        visualizations = viz_agent.generate_visualizations()
        
        # AI Insights
        insight_agent = InsightAgent()
        ai_insights = insight_agent.generate_insights(cleaning_report, eda_results)
        
        return {
            "status": "completed",
            "cleaning_report": cleaning_report,
            "eda_results": eda_results,
            "visualizations": visualizations,
            "ai_insights": ai_insights
        }
