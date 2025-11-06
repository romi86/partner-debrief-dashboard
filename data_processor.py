"""
Partner Debrief Intelligence Dashboard - Data Processing Module
BetterUp Executive Suite Coach Intelligence Platform
Created by Romina Labanca

PRODUCTION VERSION - Enhanced with enterprise-grade error handling
Version: 1.1.0
Last Updated: November 5, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import logging

# Configure logging for production debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DebriefDataProcessor:
    """
    Processes and analyzes Partner Debrief survey data.
    
    This class provides enterprise-grade data processing with automatic
    column detection, robust error handling, and comprehensive analytics
    for executive dashboard reporting.
    """
    
    # Column mapping - finds columns by various possible names
    PARTNER_COL_NAMES = [
        'Which partner program was this Debrief connected to?',
        'Partner',
        'Partner Program',
        'Organization',
        'Company',
        'Client'
    ]
    
    DATE_COL_NAMES = [
        'Debrief Session Date',
        'Date',
        'Session Date',
        'Timestamp',
        'Date/Time'
    ]
    
    PRESSURE_COL_NAMES = [
        'What single organizational pressure is most frequently mentioned by your executives right now?',
        'Organizational Pressure',
        'Organizational Pressures',
        'Pressure',
        'Pressures'
    ]
    
    CHALLENGE_COL_NAMES = [
        'What leadership challenge or development need keeps coming up across multiple executive sessions?',
        'Leadership Challenge',
        'Leadership Challenges',
        'Challenge',
        'Challenges'
    ]
    
    OBSTACLE_COL_NAMES = [
        'What implementation obstacle or barrier to change do you see most consistently across your executive cohorts?',
        'Implementation Obstacle',
        'Implementation Obstacles',
        'Obstacles',
        'Obstacle',
        'Barrier'
    ]
    
    def __init__(self, excel_path: str = None):
        """
        Initialize the data processor.
        
        Args:
            excel_path: Path to Excel file. If None, data must be loaded via load_data_from_dataframe.
        """
        self.excel_path = excel_path
        self.df = None
        self.partners = []
        self.date_range = None
        
        # Column references (populated during load)
        self.partner_col = None
        self.date_col = None
        self.pressure_col = None
        self.challenge_col = None
        self.obstacle_col = None
        
        logger.info("DebriefDataProcessor initialized")
        
    def _find_column(self, possible_names: List[str]) -> Optional[str]:
        """
        Intelligently find column by trying multiple possible names.
        
        Uses fuzzy matching and case-insensitive search to handle
        various naming conventions in Google Forms exports.
        
        Args:
            possible_names: List of possible column names to search for
            
        Returns:
            Matched column name or None if not found
        """
        if self.df is None:
            return None
        
        # First pass: Exact match
        for name in possible_names:
            if name in self.df.columns:
                logger.info(f"Found exact match for column: {name}")
                return name
        
        # Second pass: Case-insensitive partial match
        for name in possible_names:
            name_lower = name.lower()
            for col in self.df.columns:
                if name_lower in str(col).lower():
                    logger.info(f"Found partial match: '{col}' matches '{name}'")
                    return col
        
        # Third pass: Check for key words in long column names
        if possible_names:
            primary_keyword = possible_names[0].split()[0].lower()  # First word
            for col in self.df.columns:
                if primary_keyword in str(col).lower():
                    logger.info(f"Found keyword match: '{col}' contains '{primary_keyword}'")
                    return col
        
        logger.warning(f"No column found matching any of: {possible_names[:3]}...")
        return None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load and preprocess survey data from Excel file.
        
        Returns:
            Preprocessed DataFrame or None if loading fails
        """
        try:
            if self.excel_path:
                logger.info(f"Loading data from Excel: {self.excel_path}")
                self.df = pd.read_excel(self.excel_path, sheet_name='Form_Responses')
                logger.info(f"Loaded {len(self.df)} rows from Excel")
            
            if self.df is None:
                logger.error("No data loaded - df is None")
                return None
            
            return self._process_dataframe()
            
        except Exception as e:
            logger.error(f"Error loading data from Excel: {str(e)}")
            raise
    
    def load_data_from_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Load and preprocess survey data from an existing DataFrame.
        
        This method is used when data comes from Google Sheets or other sources.
        
        Args:
            df: Source DataFrame containing survey responses
            
        Returns:
            Preprocessed DataFrame
        """
        try:
            logger.info(f"Loading data from DataFrame with {len(df)} rows")
            self.df = df.copy()
            return self._process_dataframe()
            
        except Exception as e:
            logger.error(f"Error loading data from DataFrame: {str(e)}")
            raise
    
    def _process_dataframe(self) -> pd.DataFrame:
        """
        Internal method to process and validate the DataFrame.
        
        Returns:
            Processed DataFrame
        """
        if self.df is None:
            return None
        
        # Clean column names - remove extra whitespace
        self.df.columns = self.df.columns.str.strip()
        
        # Handle duplicate column names by making them unique
        cols = pd.Series(self.df.columns)
        for dup in cols[cols.duplicated()].unique():
            dup_indices = cols[cols == dup].index.values
            for i, idx in enumerate(dup_indices):
                cols.iloc[idx] = f"{dup}_{i}" if i > 0 else dup
        self.df.columns = cols
        
        logger.info(f"DataFrame has {len(self.df.columns)} columns")
        
        # Find the correct columns using intelligent matching
        self.partner_col = self._find_column(self.PARTNER_COL_NAMES)
        self.date_col = self._find_column(self.DATE_COL_NAMES)
        self.pressure_col = self._find_column(self.PRESSURE_COL_NAMES)
        self.challenge_col = self._find_column(self.CHALLENGE_COL_NAMES)
        self.obstacle_col = self._find_column(self.OBSTACLE_COL_NAMES)
        
        # Log what we found
        logger.info(f"Column mapping - Partner: {self.partner_col}, Date: {self.date_col}")
        
        # Validate critical columns
        if not self.partner_col:
            logger.warning("Partner column not found - some features may not work")
        if not self.date_col:
            logger.warning("Date column not found - some features may not work")
        
        # Convert date column with robust error handling
        if self.date_col and self.date_col in self.df.columns:
            try:
                self.df[self.date_col] = pd.to_datetime(self.df[self.date_col], errors='coerce')
                logger.info(f"Converted {self.date_col} to datetime")
            except Exception as e:
                logger.error(f"Error converting dates: {str(e)}")
        
        # Extract unique partners
        if self.partner_col and self.partner_col in self.df.columns:
            self.partners = sorted(self.df[self.partner_col].dropna().unique().tolist())
            logger.info(f"Found {len(self.partners)} unique partners")
        
        # Calculate date range from valid dates only
        if self.date_col and self.date_col in self.df.columns:
            valid_dates = self.df[self.date_col].dropna()
            if len(valid_dates) > 0:
                self.date_range = (valid_dates.min(), valid_dates.max())
                days_span = (self.date_range[1] - self.date_range[0]).days
                logger.info(f"Date range: {days_span} days ({self.date_range[0]} to {self.date_range[1]})")
        
        return self.df
    
    def get_session_count(self) -> int:
        """
        Calculate total number of valid debrief sessions.
        
        A valid session requires BOTH a partner name AND a session date.
        This ensures we only count complete, meaningful debrief records.
        
        Returns:
            Count of valid sessions
        """
        if self.df is None:
            logger.warning("get_session_count called but df is None")
            return 0
        
        # Start with all rows
        valid_rows = self.df.copy()
        
        # Filter to rows with valid partner
        if self.partner_col and self.partner_col in self.df.columns:
            before_count = len(valid_rows)
            valid_rows = valid_rows[valid_rows[self.partner_col].notna()]
            logger.info(f"Filtered by partner: {before_count} -> {len(valid_rows)} rows")
        
        # Filter to rows with valid date
        if self.date_col and self.date_col in self.df.columns:
            before_count = len(valid_rows)
            valid_rows = valid_rows[valid_rows[self.date_col].notna()]
            logger.info(f"Filtered by date: {before_count} -> {len(valid_rows)} rows")
        
        count = len(valid_rows)
        logger.info(f"Total valid sessions: {count}")
        return count
    
    def get_partner_data(self, partner_name: str) -> pd.DataFrame:
        """
        Get all debrief data for a specific partner.
        
        Args:
            partner_name: Name of the partner organization
            
        Returns:
            DataFrame containing only that partner's debriefs
        """
        if self.df is None or self.partner_col is None:
            logger.warning(f"Cannot get partner data - df or partner_col is None")
            return pd.DataFrame()
        
        partner_df = self.df[self.df[self.partner_col] == partner_name].copy()
        logger.info(f"Retrieved {len(partner_df)} records for partner: {partner_name}")
        return partner_df
    
    def extract_themes(self, data: pd.DataFrame, theme_type: str) -> List[str]:
        """
        Extract themes of specified type from the data.
        
        Args:
            data: DataFrame to extract from
            theme_type: Type of theme ('organizational_pressures', 'leadership_challenges', 
                       or 'implementation_obstacles')
                       
        Returns:
            List of theme strings
        """
        column_map = {
            'organizational_pressures': self.pressure_col,
            'leadership_challenges': self.challenge_col,
            'implementation_obstacles': self.obstacle_col
        }
        
        col_name = column_map.get(theme_type)
        if col_name is None or col_name not in data.columns:
            logger.warning(f"Column for theme type '{theme_type}' not found")
            return []
        
        # Get non-null values
        themes = data[col_name].dropna().tolist()
        
        # Clean and deduplicate
        themes = [str(t).strip() for t in themes if str(t).strip() and str(t).lower() != 'nan']
        
        logger.info(f"Extracted {len(themes)} themes of type '{theme_type}'")
        return themes
    
    def extract_theme_frequencies(self, theme_type: str) -> Dict[str, int]:
        """
        Extract and count theme frequencies across all debriefs.
        
        Args:
            theme_type: Type of theme to analyze
            
        Returns:
            Dictionary mapping theme text to frequency count
        """
        if self.df is None:
            return {}
        
        themes = self.extract_themes(self.df, theme_type)
        frequencies = dict(Counter(themes).most_common())
        
        logger.info(f"Theme frequencies for '{theme_type}': {len(frequencies)} unique themes")
        return frequencies
    
    def generate_partner_report(self, partner_name: str) -> Dict:
        """
        Generate comprehensive intelligence report for a partner.
        
        This is the primary method for generating executive-level insights
        about a specific partner organization.
        
        Args:
            partner_name: Name of the partner organization
            
        Returns:
            Dictionary containing comprehensive partner analytics
        """
        logger.info(f"Generating report for partner: {partner_name}")
        
        partner_data = self.get_partner_data(partner_name)
        
        if partner_data.empty:
            logger.warning(f"No data found for partner: {partner_name}")
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
        coach_cols = ['Coach ID', 'BetterUp Email (optional)', 'Coach', 'Coach Email']
        for col in coach_cols:
            if col in partner_data.columns:
                coach_count = partner_data[col].nunique()
                logger.info(f"Found {coach_count} unique coaches using column: {col}")
                break
        
        report = {
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
        
        logger.info(f"Report generated - {report['session_count']} sessions, "
                   f"{len(report['organizational_pressures'])} pressures")
        return report
    
    def get_partner_comparison_data(self, partner_names: List[str]) -> Dict:
        """
        Get comparison data for multiple partners.
        
        Args:
            partner_names: List of partner organization names
            
        Returns:
            Dictionary with comparison data for each partner
        """
        logger.info(f"Generating comparison data for {len(partner_names)} partners")
        
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
        """
        Get summary statistics across all debriefs.
        
        Returns:
            Dictionary containing high-level dashboard metrics
        """
        if self.df is None:
            logger.warning("get_summary_stats called but df is None")
            return {}
        
        # Count unique coaches
        coach_count = 0
        coach_cols = ['Coach ID', 'BetterUp Email (optional)', 'Coach', 'Coach Email']
        for col in coach_cols:
            if col in self.df.columns:
                coach_count = self.df[col].nunique()
                break
        
        stats = {
            'total_sessions': self.get_session_count(),
            'unique_partners': len(self.partners),
            'unique_coaches': coach_count,
            'date_range': self.date_range,
            'date_range_days': (self.date_range[1] - self.date_range[0]).days if self.date_range else 0
        }
        
        logger.info(f"Summary stats - Sessions: {stats['total_sessions']}, "
                   f"Partners: {stats['unique_partners']}, "
                   f"Coaches: {stats['unique_coaches']}")
        
        return stats
