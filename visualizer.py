"""
Partner Debrief Intelligence Dashboard - Visualization Module
Professional visualizations with BetterUp branding
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional


# BetterUp Brand Colors
BETTERUP_COLORS = {
    'primary': '#4A90E2',      # BetterUp Blue
    'secondary': '#7B68EE',    # Purple
    'accent': '#50C878',       # Emerald
    'warning': '#FFA500',      # Orange
    'danger': '#E74C3C',       # Red
    'neutral': '#95A5A6',      # Gray
    'dark': '#2C3E50',         # Dark Blue-Gray
    'light': '#ECF0F1'         # Light Gray
}

RATING_COLORS = {
    5: '#50C878',  # Excellent - Green
    4: '#4A90E2',  # Good - Blue
    3: '#FFA500',  # Average - Orange
    2: '#E74C3C',  # Below Average - Red
    1: '#C0392B'   # Poor - Dark Red
}


class DebriefVisualizer:
    """Creates professional visualizations for Partner Debrief data."""
    
    def __init__(self):
        self.font_family = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif"
        
    def create_metrics_overview(self, metrics: Dict) -> go.Figure:
        """Create overview cards showing key metrics."""
        fig = go.Figure()
        
        # Create gauge charts for ratings
        ratings = [
            ('Relevance', metrics.get('avg_relevance', 0)),
            ('Support', metrics.get('avg_support', 0)),
            ('Urgency', metrics.get('avg_urgency', 0))
        ]
        
        for i, (label, value) in enumerate(ratings):
            fig.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={'row': 0, 'column': i},
                title={'text': label, 'font': {'size': 16, 'family': self.font_family}},
                delta={'reference': 4.0},
                gauge={
                    'axis': {'range': [None, 5], 'tickwidth': 1},
                    'bar': {'color': self._get_rating_color(value)},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': BETTERUP_COLORS['neutral'],
                    'steps': [
                        {'range': [0, 2], 'color': '#FFE5E5'},
                        {'range': [2, 3.5], 'color': '#FFF4E5'},
                        {'range': [3.5, 5], 'color': '#E5F5E5'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4.5
                    }
                }
            ))
        
        fig.update_layout(
            grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white',
            font={'family': self.font_family}
        )
        
        return fig
    
    def create_partner_comparison(self, comparison_df: pd.DataFrame) -> go.Figure:
        """Create comparison chart across partners."""
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Relevance Score', 'Support Score', 'Urgency Score'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
        )
        
        metrics = [
            ('avg_relevance', 1, BETTERUP_COLORS['primary']),
            ('avg_support', 2, BETTERUP_COLORS['accent']),
            ('avg_urgency', 3, BETTERUP_COLORS['warning'])
        ]
        
        for metric, col, color in metrics:
            if metric in comparison_df.columns:
                fig.add_trace(
                    go.Bar(
                        x=comparison_df['Partner'],
                        y=comparison_df[metric],
                        name=metric.replace('avg_', '').title(),
                        marker_color=color,
                        text=comparison_df[metric].round(2),
                        textposition='outside',
                        showlegend=False
                    ),
                    row=1, col=col
                )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': self.font_family, 'size': 12},
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        fig.update_yaxes(range=[0, 5], gridcolor='#E5E5E5')
        fig.update_xaxes(tickangle=-45)
        
        return fig
    
    def create_time_series_chart(self, time_series_df: pd.DataFrame) -> go.Figure:
        """Create time series trends chart."""
        fig = go.Figure()
        
        metrics = [
            ('Relevance', BETTERUP_COLORS['primary']),
            ('Support', BETTERUP_COLORS['accent']),
            ('Urgency', BETTERUP_COLORS['warning'])
        ]
        
        for metric, color in metrics:
            if metric in time_series_df.columns:
                fig.add_trace(go.Scatter(
                    x=time_series_df['Date'],
                    y=time_series_df[metric],
                    mode='lines+markers',
                    name=metric,
                    line=dict(color=color, width=3),
                    marker=dict(size=8, color=color, line=dict(width=2, color='white'))
                ))
        
        fig.update_layout(
            title={
                'text': 'Coach Satisfaction Trends Over Time',
                'font': {'size': 20, 'family': self.font_family, 'color': BETTERUP_COLORS['dark']}
            },
            xaxis_title='Session Date',
            yaxis_title='Rating (1-5 Scale)',
            yaxis=dict(range=[0, 5.5], gridcolor='#E5E5E5'),
            xaxis=dict(gridcolor='#E5E5E5'),
            hovermode='x unified',
            height=450,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': self.font_family},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        return fig
    
    def create_theme_distribution(self, themes: List[tuple], title: str) -> go.Figure:
        """Create horizontal bar chart for theme distribution."""
        if not themes:
            return self._create_empty_chart(f"No data available for {title}")
        
        themes_df = pd.DataFrame(themes, columns=['Theme', 'Count'])
        themes_df = themes_df.sort_values('Count', ascending=True).tail(10)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=themes_df['Count'],
            y=themes_df['Theme'],
            orientation='h',
            marker=dict(
                color=themes_df['Count'],
                colorscale=[
                    [0, BETTERUP_COLORS['light']],
                    [0.5, BETTERUP_COLORS['primary']],
                    [1, BETTERUP_COLORS['secondary']]
                ],
                line=dict(color=BETTERUP_COLORS['dark'], width=1)
            ),
            text=themes_df['Count'],
            textposition='outside'
        ))
        
        fig.update_layout(
            title={
                'text': title,
                'font': {'size': 16, 'family': self.font_family}
            },
            xaxis_title='Frequency',
            yaxis_title='',
            height=max(300, len(themes_df) * 40),
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': self.font_family},
            margin=dict(l=250, r=40, t=60, b=40),
            xaxis=dict(gridcolor='#E5E5E5'),
            yaxis=dict(tickfont={'size': 11})
        )
        
        return fig
    
    def create_session_volume_chart(self, comparison_df: pd.DataFrame) -> go.Figure:
        """Create chart showing session volumes by partner."""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=comparison_df['Partner'],
            y=comparison_df['unique_sessions'],
            marker=dict(
                color=comparison_df['unique_sessions'],
                colorscale=[
                    [0, BETTERUP_COLORS['light']],
                    [0.5, BETTERUP_COLORS['accent']],
                    [1, BETTERUP_COLORS['secondary']]
                ],
                line=dict(color=BETTERUP_COLORS['dark'], width=1.5)
            ),
            text=comparison_df['unique_sessions'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': 'Debrief Session Volume by Partner',
                'font': {'size': 18, 'family': self.font_family}
            },
            xaxis_title='Partner Program',
            yaxis_title='Number of Sessions',
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': self.font_family},
            margin=dict(l=60, r=40, t=80, b=60),
            yaxis=dict(gridcolor='#E5E5E5'),
            xaxis=dict(tickangle=-45)
        )
        
        return fig
    
    def create_response_distribution(self, df: pd.DataFrame, column: str, title: str) -> go.Figure:
        """Create distribution chart for rating responses."""
        if column not in df.columns:
            return self._create_empty_chart(f"No data available for {title}")
        
        values = df[column].dropna()
        value_counts = values.value_counts().sort_index()
        
        colors = [RATING_COLORS.get(int(rating), BETTERUP_COLORS['neutral']) 
                 for rating in value_counts.index]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=value_counts.index,
            y=value_counts.values,
            marker=dict(color=colors, line=dict(color=BETTERUP_COLORS['dark'], width=1)),
            text=value_counts.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            title={'text': title, 'font': {'size': 16, 'family': self.font_family}},
            xaxis_title='Rating',
            yaxis_title='Number of Responses',
            height=350,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': self.font_family},
            margin=dict(l=60, r=40, t=60, b=40),
            xaxis=dict(tickmode='linear', tick0=1, dtick=1, range=[0.5, 5.5]),
            yaxis=dict(gridcolor='#E5E5E5')
        )
        
        return fig
    
    def create_heatmap_comparison(self, comparison_df: pd.DataFrame) -> go.Figure:
        """Create heatmap comparing all metrics across partners."""
        metrics_to_plot = ['avg_relevance', 'avg_support', 'avg_urgency', 'unique_sessions']
        available_metrics = [m for m in metrics_to_plot if m in comparison_df.columns]
        
        if not available_metrics:
            return self._create_empty_chart("No metrics available for comparison")
        
        # Prepare data for heatmap
        heatmap_data = comparison_df[['Partner'] + available_metrics].set_index('Partner')
        
        # Normalize session count for visualization
        if 'unique_sessions' in heatmap_data.columns:
            max_sessions = heatmap_data['unique_sessions'].max()
            heatmap_data['unique_sessions'] = (heatmap_data['unique_sessions'] / max_sessions) * 5
        
        metric_labels = {
            'avg_relevance': 'Relevance',
            'avg_support': 'Support',
            'avg_urgency': 'Urgency',
            'unique_sessions': 'Session Volume (Normalized)'
        }
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=[metric_labels.get(col, col) for col in heatmap_data.columns],
            y=heatmap_data.index,
            colorscale=[
                [0, '#E74C3C'],
                [0.4, '#FFA500'],
                [0.7, '#4A90E2'],
                [1, '#50C878']
            ],
            text=heatmap_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 14},
            colorbar=dict(title="Score", titleside="right"),
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': 'Partner Program Performance Heatmap',
                'font': {'size': 18, 'family': self.font_family}
            },
            height=max(300, len(comparison_df) * 60),
            paper_bgcolor='white',
            font={'family': self.font_family},
            margin=dict(l=150, r=100, t=80, b=60)
        )
        
        return fig
    
    def _get_rating_color(self, rating: float) -> str:
        """Get color based on rating value."""
        if rating >= 4.5:
            return RATING_COLORS[5]
        elif rating >= 3.5:
            return RATING_COLORS[4]
        elif rating >= 2.5:
            return RATING_COLORS[3]
        elif rating >= 1.5:
            return RATING_COLORS[2]
        else:
            return RATING_COLORS[1]
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create empty chart with message."""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font={'size': 14, 'color': BETTERUP_COLORS['neutral']}
        )
        
        fig.update_layout(
            height=300,
            paper_bgcolor='white',
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        
        return fig
