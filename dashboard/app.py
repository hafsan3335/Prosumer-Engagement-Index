"""
Interactive Plotly Dash Web Application for Prosumer Behavioral Index research.
Run with `python dashboard/app.py` to view locally at http://127.0.0.1:8050.
"""
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from src.config import PROC_INDEX_CSV, PROC_SEGMENTS_CSV, PALETTE

# Initialize Dash application
app = Dash(__name__, title="Prosumer Behavioral Index Dashboard")
server = app.server

# Load datasets
df = pd.read_csv(PROC_INDEX_CSV)
seg_df = pd.read_csv(PROC_SEGMENTS_CSV)
users_df = df[df["is_active_user"] == 1]

app.layout = html.Div(
    style={"fontFamily": "Inter, sans-serif", "backgroundColor": "#0B0F19", "color": "#F8FAFC", "padding": "24px"},
    children=[
        html.Div([
            html.Span("Research Portfolio • Quantitative Consumer Analytics", style={"backgroundColor": "rgba(59, 130, 246, 0.2)", "color": "#60A5FA", "padding": "4px 12px", "borderRadius": "16px", "fontSize": "12px", "fontWeight": "600"}),
            html.H1("Prosumer Engagement in the Sharing Economy", style={"fontSize": "28px", "fontWeight": "800", "marginTop": "8px"}),
            html.P("Empirical Consumer Behaviour Research using Flash Eurobarometer 467 (N = 26,544 across EU-28)", style={"color": "#94A3B8", "fontSize": "14px"})
        ], style={"borderBottom": "1px solid #232E47", "paddingBottom": "16px", "marginBottom": "24px"}),
        
        # KPI Row
        html.Div([
            html.Div([html.P("Total Surveyed", style={"color": "#94A3B8", "fontSize": "12px"}), html.H3("26,544", style={"fontSize": "24px", "fontWeight": "700"}), html.Span("EU-28 Sample", style={"fontSize": "11px", "color": "#64748B"})], style={"backgroundColor": "#151C2C", "padding": "16px", "borderRadius": "8px", "flex": "1"}),
            html.Div([html.P("Active Users", style={"color": "#94A3B8", "fontSize": "12px"}), html.H3("5,872", style={"fontSize": "24px", "fontWeight": "700"}), html.Span("22.1% Adoption", style={"fontSize": "11px", "color": "#3B82F6"})], style={"backgroundColor": "#151C2C", "padding": "16px", "borderRadius": "8px", "flex": "1"}),
            html.Div([html.P("Dual Prosumers", style={"color": "#94A3B8", "fontSize": "12px"}), html.H3("1,149", style={"fontSize": "24px", "fontWeight": "700"}), html.Span("19.6% of Users", style={"fontSize": "11px", "color": "#8B5CF6"})], style={"backgroundColor": "#151C2C", "padding": "16px", "borderRadius": "8px", "flex": "1"}),
            html.Div([html.P("Mean PEI (Users)", style={"color": "#94A3B8", "fontSize": "12px"}), html.H3("18.2 / 100", style={"fontSize": "24px", "fontWeight": "700"}), html.Span("Prosumers: 37.4", style={"fontSize": "11px", "color": "#10B981"})], style={"backgroundColor": "#151C2C", "padding": "16px", "borderRadius": "8px", "flex": "1"}),
        ], style={"display": "flex", "gap": "16px", "marginBottom": "24px"}),
        
        # Tabs
        dcc.Tabs(
            id="dash-tabs",
            value="overview",
            colors={"border": "#232E47", "primary": "#3B82F6", "background": "#151C2C"},
            children=[
                dcc.Tab(label="1. Market Overview", value="overview", style={"color": "#94A3B8"}),
                dcc.Tab(label="2. Prosumer Index (PEI)", value="pei", style={"color": "#94A3B8"}),
                dcc.Tab(label="3. Consumer vs Prosumer", value="contrast", style={"color": "#94A3B8"}),
                dcc.Tab(label="4. Personas & Segments", value="segments", style={"color": "#94A3B8"}),
            ]
        ),
        html.Div(id="tab-content", style={"marginTop": "20px"})
    ]
)

@app.callback(Output("tab-content", "children"), Input("dash-tabs", "value"))
def render_tab_content(tab):
    if tab == "overview":
        counts = df["user_profile"].value_counts()
        fig_pie = px.pie(names=counts.index, values=counts.values, hole=0.5, title="Market Participation Structure")
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        return html.Div([dcc.Graph(figure=fig_pie)], style={"backgroundColor": "#151C2C", "padding": "20px", "borderRadius": "8px"})
    elif tab == "pei":
        fig_hist = px.histogram(users_df, x="PEI", color="user_profile", nbins=30, title="PEI Distribution by User Role")
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        return html.Div([dcc.Graph(figure=fig_hist)], style={"backgroundColor": "#151C2C", "padding": "20px", "borderRadius": "8px"})
    elif tab == "contrast":
        fig_box = px.box(users_df, x="user_profile", y="PEI", color="user_profile", title="PEI Score Spread across Roles")
        fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        return html.Div([dcc.Graph(figure=fig_box)], style={"backgroundColor": "#151C2C", "padding": "20px", "borderRadius": "8px"})
    elif tab == "segments":
        seg_counts = seg_df["segment_name"].value_counts().reset_index()
        fig_bar = px.bar(seg_counts, x="count", y="segment_name", orientation="h", title="Consumer Segments Distribution", color="segment_name")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        return html.Div([dcc.Graph(figure=fig_bar)], style={"backgroundColor": "#151C2C", "padding": "20px", "borderRadius": "8px"})

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
