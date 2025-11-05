"""
Partner Debrief Intelligence Dashboard - Data Processing Module
BetterUp Executive Suite Coach Intelligence Platform
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter


class DebriefDataProcessor:
    """Processes and analyzes Partner Debrief survey data."""
    
    def __init__(self, excel_path: str):
        """Initialize with path to Excel file containing survey responses."""
        self.excel_path = excel_path
        self.df = None
        self.partners = []
        self.date_range = None
        
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess survey data from Excel."""
        self.df = pd.read_excel(self.excel_path, sheet_name='Form_Responses')
        
        # Clean column names
        self.df.columns = self.df.columns.str.strip()
        
        # Convert date columns
        date_columns = ['Timestamp', 'Debrief Session Date']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Extract unique partners
        if 'Which partner program was this Debrief connected to?' in self.df.columns:
            self.partners = sorted(self.df['Which partner program was this Debrief connected to?'].dropna().unique().tolist())
        
        # Calculate date range
        if 'Debrief Session Date' in self.df.columns:
            valid_dates = self.df['Debrief Session Date'].dropna()
            if len(valid_dates) > 0:
                self.date_range = (valid_dates.min(), valid_dates.max())
        
        return self.df
    
    def get_session_count(self) -> int:
        """Calculate total number of unique debrief sessions."""
        if 'Debrief Session Date' not in self.df.columns:
            return 0
        
        # Count unique combinations of date and partner
        unique_sessions = self.df.groupby([
            'Debrief Session Date', 
            'Which partner program was this Debrief connected to?'
        ]).size()
        
        return len(unique_sessions)
    
    def get_partner_metrics(self, partner: Optional[str] = None) -> Dict:
        """Calculate key metrics for a partner or all partners."""
        df = self.df if partner is None else self.df[
            self.df['Which partner program was this Debrief connected to?'] == partner
        ]
        
        metrics = {
            'total_responses': len(df),
            'unique_sessions': self._count_unique_sessions(df),
            'avg_relevance': self._safe_mean(df, 'How relevant was today\'s discussion to your current executive coaching challenges?'),
            'avg_support': self._safe_mean(df, 'How supported do you feel by BetterUp to show up fully in your executive coaching sessions?'),
            'avg_urgency': self._safe_mean(df, 'How urgent is the primary pressure/challenge you discussed today?'),
            'date_range': self._get_date_range(df)
        }
        
        return metrics
    
    def get_theme_analysis(self, partner: Optional[str] = None) -> Dict[str, List[Tuple[str, int]]]:
        """Analyze themes from qualitative responses."""
        df = self.df if partner is None else self.df[
            self.df['Which partner program was this Debrief connected to?'] == partner
        ]
        
        theme_columns = {
            'organizational_pressures': 'What single organizational pressure is most frequently mentioned by your executives right now?',
            'leadership_challenges': 'What leadership challenge or development need keeps coming up across multiple executive sessions?',
            'implementation_obstacles': 'What\'s the biggest obstacle preventing your executives from implementing what they learn in coaching?',
            'valuable_takeaways': 'What was the most valuable takeaway from today\'s session for your coaching practice?'
        }
        
        themes = {}
        for key, column in theme_columns.items():
            if column in df.columns:
                themes[key] = self._extract_top_themes(df[column])
        
        return themes
    
    def get_time_series_data(self, partner: Optional[str] = None) -> pd.DataFrame:
        """Get time series data for trend analysis."""
        df = self.df if partner is None else self.df[
            self.df['Which partner program was this Debrief connected to?'] == partner
        ]
        
        if 'Debrief Session Date' not in df.columns:
            return pd.DataFrame()
        
        # Group by session date and calculate metrics
        time_series = df.groupby('Debrief Session Date').agg({
            'How relevant was today\'s discussion to your current executive coaching challenges?': 'mean',
            'How supported do you feel by BetterUp to show up fully in your executive coaching sessions?': 'mean',
            'How urgent is the primary pressure/challenge you discussed today?': 'mean',
            'Coach ID': 'count'
        }).reset_index()
        
        time_series.columns = ['Date', 'Relevance', 'Support', 'Urgency', 'Response_Count']
        time_series = time_series.sort_values('Date')
        
        return time_series
    
    def compare_partners(self, metrics: List[str]) -> pd.DataFrame:
        """Compare metrics across all partners."""
        comparison_data = []
        
        for partner in self.partners:
            partner_metrics = self.get_partner_metrics(partner)
            row = {'Partner': partner}
            
            for metric in metrics:
                if metric in partner_metrics:
                    row[metric] = partner_metrics[metric]
            
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def get_qualitative_insights(self, partner: Optional[str] = None) -> Dict[str, List[str]]:
        """Extract qualitative insights and quotes."""
        df = self.df if partner is None else self.df[
            self.df['Which partner program was this Debrief connected to?'] == partner
        ]
        
        insights = {}
        
        # Key insights columns
        insight_columns = [
            'Is there anything you didn\'t get to share in today\'s session that feels important for the group or BetterUp to know?',
            'What was the most valuable takeaway from today\'s session for your coaching practice?',
            'What barriers are you seeing that make it harder for executives to apply what they\'re learning?'
        ]
        
        for col in insight_columns:
            if col in df.columns:
                # Filter out empty responses and convert to string
                responses = df[col].dropna().astype(str)
                responses = responses[responses.str.strip() != '']
                responses = responses[responses.str.lower() != 'nan']
                insights[col] = responses.tolist()
        
        return insights
    
    def _count_unique_sessions(self, df: pd.DataFrame) -> int:
        """Count unique debrief sessions."""
        if 'Debrief Session Date' not in df.columns:
            return 0
        
        unique_sessions = df.groupby([
            'Debrief Session Date'
        ]).size()
        
        return len(unique_sessions)
    
    def _safe_mean(self, df: pd.DataFrame, column: str) -> float:
        """Safely calculate mean, handling missing values."""
        if column not in df.columns:
            return 0.0
        
        values = pd.to_numeric(df[column], errors='coerce')
        return values.mean() if len(values) > 0 else 0.0
    
    def _get_date_range(self, df: pd.DataFrame) -> Tuple[str, str]:
        """Get date range for the dataframe."""
        if 'Debrief Session Date' not in df.columns:
            return ('N/A', 'N/A')
        
        valid_dates = df['Debrief Session Date'].dropna()
        if len(valid_dates) == 0:
            return ('N/A', 'N/A')
        
        min_date = valid_dates.min().strftime('%Y-%m-%d')
        max_date = valid_dates.max().strftime('%Y-%m-%d')
        
        return (min_date, max_date)
    
    def _extract_top_themes(self, series: pd.Series, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extract and count top themes from text responses."""
        # Clean and filter responses
        responses = series.dropna()
        responses = responses[responses.str.strip() != '']
        
        # Count occurrences
        theme_counts = Counter(responses)
        
        # Return top themes
        return theme_counts.most_common(top_n)
    
    def export_partner_report_data(self, partner: str) -> Dict:
        """Export comprehensive data for a partner report."""
        partner_df = self.df[self.df['Which partner program was this Debrief connected to?'] == partner]
        
        report_data = {
            'partner_name': partner,
            'metrics': self.get_partner_metrics(partner),
            'themes': self.get_theme_analysis(partner),
            'time_series': self.get_time_series_data(partner),
            'qualitative_insights': self.get_qualitative_insights(partner),
            'session_details': partner_df.to_dict('records')
        }
        
        return report_data
