"""
Partner Debrief Intelligence Dashboard - Data Processing Module
BetterUp Executive Suite Coach Intelligence Platform
Created by Romina Labanca
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter


class DebriefDataProcessor:
    """Processes and analyzes Partner Debrief survey data."""
    
    # Column mapping - finds columns by various possible names
    PARTNER_COL_NAMES = [
        'Which partner program was this Debrief connected to?',
        'Partner',
        'Partner Program',
        'Organization',
        'Company'
    ]
    
    DATE_COL_NAMES = [
        'Debrief Session Date',
        'Date',
        'Session Date',
        'Timestamp'
    ]
    
    PRESSURE_COL_NAMES = [
        'What single organizational pressure is most frequently mentioned by your executives right now?',
        'Organizational Pressure',
        'Organizational Pressures',
        'Pressure'
    ]
    
    CHALLENGE_COL_NAMES = [
        'What leadership challenge or development need keeps coming up across multiple executive sessions?',
        'Leadership Challenge',
        'Leadership Challenges'
    ]
    
    OBSTACLE_COL_NAMES = [
        'What implementation obstacle or barrier to change do you see most consistently across your executive cohorts?',
        'Implementation Obstacle',
        'Implementation Obstacles',
        'Obstacles'
    ]
    
    def __init__(self, excel_path: str):
        """Initialize with path to Excel file containing survey responses."""
        self.excel_path = excel_path
        self.df = None
        self.partners = []
        self.date_range = None
        self.partner_col = None
        self.date_col = None
        self.pressure_col = None
        self.challenge_col = None
        self.obstacle_col = None
        
    def _find_column(self, possible_names: List[str]) -> Optional[str]:
        """Find column by trying multiple possible names."""
        if self.df is None:
            return None
        
        for name in possible_names:
            # Try exact match
            if name in self.df.columns:
                return name
            # Try case-insensitive partial match
            for col in self.df.columns:
                if name.lower() in str(col).lower():
                    return col
        return None
    
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess survey data from Excel."""
        if self.excel_path:
            self.df = pd.read_excel(self.excel_path, sheet_name='Form_Responses')
        
        if self.df is None:
            return None
            
        # Clean column names
        self.df.columns = self.df.columns.str.strip()
        
        # Find the correct columns
        self.partner_col = self._find_column(self.PARTNER_COL_NAMES)
        self.date_col = self._find_column(self.DATE_COL_NAMES)
        self.pressure_col = self._find_column(self.PRESSURE_COL_NAMES)
        self.challenge_col = self._find_column(self.CHALLENGE_COL_NAMES)
        self.obstacle_col = self._find_column(self.OBSTACLE_COL_NAMES)
        
        # Convert date column
        if self.date_col and self.date_col in self.df.columns:
            self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
        
        # Extract unique partners
        if self.partner_col and self.partner_col in self.df.columns:
            self.partners = sorted(self.df[self.partner_col].dropna().unique().tolist())
        
        # Calculate date range
        if self.date_col and self.date_col in self.df.columns:
            valid_dates = self.df[self.date_col].dropna()
            if len(valid_dates) > 0:
                self.date_range = (valid_dates.min(), valid_dates.max())
        
        return self.df
    
    def get_session_count(self) -> int:
        """Calculate total number of debrief sessions (rows with valid date and partner)."""
        if self.df is None:
            return 0
        
        # Count rows that have both a partner and a date
        valid_rows = self.df.copy()
        
        if self.partner_col:
            valid_rows = valid_rows[valid_rows[self.partner_col].notna()]
        
        if self.date_col:
            valid_rows = valid_rows[valid_rows[self.date_col].notna()]
        
        return len(valid_rows)
    
    def get_partner_data(self, partner_name: str) -> pd.DataFrame:
        """Get all debrief data for a specific partner."""
        if self.df is None or self.partner_col is None:
            return pd.DataFrame()
        
        return self.df[self.df[self.partner_col] == partner_name].copy()
    
    def extract_themes(self, data: pd.DataFrame, theme_type: str) -> List[str]:
        """Extract themes of specified type from the data."""
        column_map = {
            'organizational_pressures': self.pressure_col,
            'leadership_challenges': self.challenge_col,
            'implementation_obstacles': self.obstacle_col
        }
        
        col_name = column_map.get(theme_type)
        if col_name is None or col_name not in data.columns:
            return []
        
        # Get non-null values
        themes = data[col_name].dropna().tolist()
        
        # Clean and deduplicate
        themes = [str(t).strip() for t in themes if str(t).strip() and str(t).lower() != 'nan']
        
        return themes
    
    def extract_theme_frequencies(self, theme_type: str) -> Dict[str, int]:
        """Extract and count theme frequencies across all debriefs."""
        if self.df is None:
            return {}
        
        themes = self.extract_themes(self.df, theme_type)
        return dict(Counter(themes).most_common())
    
    def generate_partner_report(self, partner_name: str) -> Dict:
        """Generate comprehensive intelligence report for a partner."""
        partner_data = self.get_partner_data(partner_name)
        
        if partner_data.empty:
            return {
                'partner_name': partner_name,
                'session_count': 0,
                'date_range': None,
                'organizational_pressures': [],
                'leadership_challenges': [],
                'implementation_obstacles': [],
                'metrics': {}
            }
        
        # Extract dates
        dates = []
        if self.date_col and self.date_col in partner_data.columns:
            dates = pd.to_datetime(partner_data[self.date_col], errors='coerce').dropna()
        
        date_range = None
        if len(dates) > 0:
            date_range = (dates.min(), dates.max())
        
        # Count unique coaches
        coach_count = 0
        coach_cols = ['Coach ID', 'BetterUp Email (optional)', 'Coach']
        for col in coach_cols:
            if col in partner_data.columns:
                coach_count = partner_data[col].nunique()
                break
        
        return {
            'partner_name': partner_name,
            'session_count': len(partner_data),
            'date_range': date_range,
            'organizational_pressures': self.extract_themes(partner_data, 'organizational_pressures'),
            'leadership_challenges': self.extract_themes(partner_data, 'leadership_challenges'),
            'implementation_obstacles': self.extract_themes(partner_data, 'implementation_obstacles'),
            'metrics': {
                'total_sessions': len(partner_data),
                'unique_coaches': coach_count,
                'date_range_days': (date_range[1] - date_range[0]).days if date_range else 0
            }
        }
    
    def get_partner_comparison_data(self, partner_names: List[str]) -> Dict:
        """Get comparison data for multiple partners."""
        comparison_data = {}
        
        for partner in partner_names:
            partner_data = self.get_partner_data(partner)
            comparison_data[partner] = {
                'session_count': len(partner_data),
                'pressures': self.extract_themes(partner_data, 'organizational_pressures'),
                'challenges': self.extract_themes(partner_data, 'leadership_challenges'),
                'obstacles': self.extract_themes(partner_data, 'implementation_obstacles')
            }
        
        return comparison_data
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics across all debriefs."""
        if self.df is None:
            return {}
        
        # Count unique coaches
        coach_count = 0
        coach_cols = ['Coach ID', 'BetterUp Email (optional)', 'Coach']
        for col in coach_cols:
            if col in self.df.columns:
                coach_count = self.df[col].nunique()
                break
        
        return {
            'total_sessions': self.get_session_count(),
            'unique_partners': len(self.partners),
            'unique_coaches': coach_count,
            'date_range': self.date_range,
            'date_range_days': (self.date_range[1] - self.date_range[0]).days if self.date_range else 0
        }
