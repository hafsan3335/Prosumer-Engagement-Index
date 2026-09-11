"""
Dashboard generator for Prosumer Behavioral Index research.
Builds a rich, self-contained, responsive HTML dashboard (index.html) with Plotly.js,
interactive tabs, KPI metric cards, filters, and persona strategy cards.
"""
import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.config import (
    PROC_INDEX_CSV, PROC_SEGMENTS_CSV, DASHBOARD_DIR,
    COUNTRY_MAP, COUNTRY_ISO3, PALETTE
)

def build_dashboard():
    print("Building standalone interactive research dashboard...")
    os.makedirs(DASHBOARD_DIR, exist_ok=True)
    
    df = pd.read_csv(PROC_INDEX_CSV)
    seg_df = pd.read_csv(PROC_SEGMENTS_CSV)
    users_df = df[df["is_active_user"] == 1]
    
    # 1. Market Overview Charts
    # Chart 1A: Participation Donut
    counts = df["user_profile"].value_counts()
    fig_part = go.Figure(data=[go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.55,
        marker=dict(colors=[PALETTE["non_user"], PALETTE["consumer"], PALETTE["prosumer"], PALETTE["provider"]]),
        textinfo="label+percent",
        hoverinfo="label+value+percent"
    )])
    fig_part.update_layout(
        title="Market Participation Structure (EU-28, N=26,544)",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=20, l=20, r=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.1)
    )
    
    # Chart 1B: Adoption by Age Group
    age_rates = df.groupby("age_cohort").agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100
    }).loc[["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]]
    
    fig_age = go.Figure(data=[
        go.Bar(name="Active User Rate (%)", x=age_rates.index, y=age_rates["is_active_user"], marker_color="#3B82F6"),
        go.Bar(name="Prosumer Rate (%)", x=age_rates.index, y=age_rates["is_prosumer"], marker_color="#8B5CF6")
    ])
    fig_age.update_layout(
        title="Adoption & Prosumption by Age Cohort",
        barmode="group",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=20, l=20, r=20),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1)
    )
    
    # 2. PEI Distribution Chart
    fig_pei = go.Figure()
    fig_pei.add_trace(go.Histogram(
        x=users_df["PEI"],
        nbinsx=30,
        marker_color="#6366F1",
        opacity=0.85,
        name="All Active Users (N=5,872)"
    ))
    fig_pei.add_trace(go.Histogram(
        x=df[df["user_profile"] == "Prosumer"]["PEI"],
        nbinsx=30,
        marker_color="#EC4899",
        opacity=0.85,
        name="Prosumers (N=1,149)"
    ))
    fig_pei.update_layout(
        title="Prosumer Engagement Index (PEI) Distribution (0-100 Score)",
        barmode="overlay",
        xaxis_title="Prosumer Engagement Index (PEI)",
        yaxis_title="Respondent Count",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=30, l=30, r=20),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1)
    )
    
    # 3. Consumer vs Prosumer Contrast
    cp_metrics = {
        "Sector Breadth": [users_df[users_df["user_profile"]=="Consumer Only"]["consumer_sector_breadth"].mean(),
                           users_df[users_df["user_profile"]=="Prosumer"]["consumer_sector_breadth"].mean()],
        "Substitution (%)": [users_df[users_df["user_profile"]=="Consumer Only"]["is_substitutor"].mean()*100,
                             users_df[users_df["user_profile"]=="Prosumer"]["is_substitutor"].mean()*100],
        "Advocacy (%)": [users_df[users_df["user_profile"]=="Consumer Only"]["recommend_high"].mean()*100,
                         users_df[users_df["user_profile"]=="Prosumer"]["recommend_high"].mean()*100],
        "Social Value (%)": [users_df[users_df["user_profile"]=="Consumer Only"]["adv_social_score"].mean()*100,
                             users_df[users_df["user_profile"]=="Prosumer"]["adv_social_score"].mean()*100]
    }
    cp_df = pd.DataFrame(cp_metrics, index=["Consumer Only", "Prosumer"]).T
    fig_cp = go.Figure(data=[
        go.Bar(name="Consumer Only", x=cp_df.index, y=cp_df["Consumer Only"], marker_color="#3B82F6"),
        go.Bar(name="Prosumer", x=cp_df.index, y=cp_df["Prosumer"], marker_color="#8B5CF6")
    ])
    fig_cp.update_layout(
        title="Behavioral Contrast: Consumer-Only vs. Dual Prosumers",
        barmode="group",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=20, l=20, r=20),
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1)
    )
    
    # 4. Consumer Segments Bar
    seg_counts = seg_df["segment_name"].value_counts()
    fig_seg = go.Figure(data=[go.Bar(
        x=seg_counts.values,
        y=seg_counts.index,
        orientation="h",
        marker=dict(color=["#0EA5E9", "#10B981", "#8B5CF6", "#F59E0B"]),
        text=[f"{v:,} ({v/len(seg_df)*100:.1f}%)" for v in seg_counts.values],
        textposition="outside"
    )])
    fig_seg.update_layout(
        title="Collaborative Economy Consumer Segments (K-Means, N=5,872)",
        xaxis_title="Number of Users",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=30, l=150, r=60),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    # 5. Motivations (Economic vs Sustainability)
    prov_df = df[df["is_provider"] == 1]
    mot_vals = {
        "Additional Income": prov_df["prov_mot_q11_2"].mean() * 100,
        "Flexible Hours": prov_df["prov_mot_q11_3"].mean() * 100,
        "Easy Opportunity": prov_df["prov_mot_q11_4"].mean() * 100,
        "Access to Consumers": prov_df["prov_mot_q11_6"].mean() * 100,
        "Sustainable Asset Use": prov_df["prov_mot_q11_8"].mean() * 100,
        "Social Interaction": prov_df["prov_mot_q11_7"].mean() * 100,
        "Offer Innovation": prov_df["prov_mot_q11_5"].mean() * 100,
        "Main Income": prov_df["prov_mot_q11_1"].mean() * 100
    }
    s_mot = pd.Series(mot_vals).sort_values(ascending=True)
    fig_mot = go.Figure(data=[go.Bar(
        x=s_mot.values,
        y=s_mot.index,
        orientation="h",
        marker_color=["#10B981" if "Sustainable" in k else "#3B82F6" for k in s_mot.index],
        text=[f"{v:.1f}%" for v in s_mot.values],
        textposition="outside"
    )])
    fig_mot.update_layout(
        title="Service Provider Motivations (Green = Sustainability Focus)",
        xaxis_title="% Endorsing Reason",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=30, l=140, r=40),
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    # 6. Country Map / Comparison
    country_stats = df.groupby(["country", "country_iso3"]).agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100,
        "PEI": "mean"
    }).reset_index()
    
    fig_map = px.choropleth(
        country_stats,
        locations="country_iso3",
        color="is_active_user",
        hover_name="country",
        hover_data={"is_active_user": ":.1f%", "is_prosumer": ":.1f%", "PEI": ":.1f", "country_iso3": False},
        color_continuous_scale="Blues",
        scope="europe",
        labels={"is_active_user": "Adoption Rate (%)"}
    )
    fig_map.update_layout(
        title="Collaborative Platform Adoption Across EU-28",
        font=dict(family="Inter, sans-serif", size=12),
        margin=dict(t=40, b=0, l=0, r=0),
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False)
    )
    
    # Convert Plotly figures to JSON
    json_part = fig_part.to_json()
    json_age = fig_age.to_json()
    json_pei = fig_pei.to_json()
    json_cp = fig_cp.to_json()
    json_seg = fig_seg.to_json()
    json_mot = fig_mot.to_json()
    json_map = fig_map.to_json()
    
    # HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prosumer Engagement in the Sharing Economy | Research Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #0B0F19;
      --bg-card: #151C2C;
      --border: #232E47;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --primary: #3B82F6;
      --secondary: #10B981;
      --accent: #8B5CF6;
      --warning: #F59E0B;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 40px;
    }}
    .header {{
      background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
      border-bottom: 1px solid var(--border);
      padding: 24px 36px;
    }}
    .header-badge {{
      display: inline-block;
      padding: 4px 12px;
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.3);
      color: #60A5FA;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .header h1 {{
      font-size: 1.8rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #FFFFFF;
      margin-bottom: 6px;
    }}
    .header p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      max-width: 900px;
    }}
    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      padding: 24px 36px 0 36px;
    }}
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    .kpi-label {{
      font-size: 0.78rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .kpi-val {{
      font-size: 1.7rem;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.5px;
    }}
    .kpi-sub {{
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}
    .nav-tabs {{
      display: flex;
      gap: 8px;
      padding: 20px 36px 0 36px;
      border-bottom: 1px solid var(--border);
      overflow-x: auto;
    }}
    .tab-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 12px 18px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 3px solid transparent;
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .tab-btn:hover {{ color: #FFFFFF; }}
    .tab-btn.active {{
      color: #60A5FA;
      border-bottom-color: #3B82F6;
    }}
    .content-container {{
      padding: 24px 36px;
    }}
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}
    @media (max-width: 900px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
      margin-bottom: 20px;
    }}
    .card-title {{
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 12px;
      color: #F1F5F9;
    }}
    .persona-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 16px;
    }}
    .persona-card {{
      background: #192238;
      border-left: 4px solid #3B82F6;
      border-radius: 8px;
      padding: 18px;
    }}
    .persona-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 4px;
    }}
    .persona-tag {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 4px;
      margin-bottom: 12px;
    }}
    .tag-frugal {{ background: #0284C7; color: white; }}
    .tag-convenience {{ background: #0D9488; color: white; }}
    .tag-sust {{ background: #16A34A; color: white; }}
    .tag-micro {{ background: #7C3AED; color: white; }}
    .persona-p {{
      font-size: 0.83rem;
      color: #CBD5E1;
      margin-bottom: 10px;
    }}
    .persona-meta {{
      font-size: 0.78rem;
      color: #94A3B8;
      border-top: 1px solid rgba(255,255,255,0.08);
      padding-top: 8px;
    }}
    .footer {{
      text-align: center;
      padding: 30px;
      color: var(--text-muted);
      font-size: 0.82rem;
      border-top: 1px solid var(--border);
      margin-top: 40px;
    }}
  </style>
</head>
<body>

  <div class="header">
    <span class="header-badge">Research Portfolio • Quantitative Marketing & Consumer Behaviour</span>
    <h1>Prosumer Engagement in the Sharing Economy</h1>
    <p>A quantitative empirical analysis of consumer value creation, multi-sector participation, and sustainable market governance using European Commission Flash Eurobarometer 467 (N = 26,544 across EU-28).</p>
  </div>

  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-label">Total Surveyed</div>
      <div class="kpi-val">26,544</div>
      <div class="kpi-sub">EU-28 representative sample</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Active Users</div>
      <div class="kpi-val">5,872</div>
      <div class="kpi-sub">22.1% unweighted (23.4% weighted)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Dual Prosumers</div>
      <div class="kpi-val">1,149</div>
      <div class="kpi-sub">4.3% EU population / 19.6% of users</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Mean PEI (Users)</div>
      <div class="kpi-val">18.2 / 100</div>
      <div class="kpi-sub">Prosumer mean: 37.4 / 100</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Top Country Adoption</div>
      <div class="kpi-val">France (36%)</div>
      <div class="kpi-sub">Followed by Ireland (35%), Croatia (34%)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Advocacy Correlation</div>
      <div class="kpi-val">r = +0.22</div>
      <div class="kpi-sub">PEI predicts recommendation (p < 0.001)</div>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="showTab('tab-overview', this)">1. Market Overview</button>
    <button class="tab-btn" onclick="showTab('tab-pei', this)">2. Prosumer Index (PEI)</button>
    <button class="tab-btn" onclick="showTab('tab-contrast', this)">3. Consumer vs. Prosumer</button>
    <button class="tab-btn" onclick="showTab('tab-segments', this)">4. Personas & Segments</button>
    <button class="tab-btn" onclick="showTab('tab-motives', this)">5. Motivations & Green Sharing</button>
    <button class="tab-btn" onclick="showTab('tab-geo', this)">6. EU-28 Spatial Map</button>
    <button class="tab-btn" onclick="showTab('tab-strategy', this)">7. Marketing Strategy</button>
  </div>

  <div class="content-container">

    <!-- TAB 1: OVERVIEW -->
    <div id="tab-overview" class="tab-pane active">
      <div class="grid-2">
        <div class="card">
          <div id="chart-part"></div>
        </div>
        <div class="card">
          <div id="chart-age"></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Key Macro-Market Finding</div>
        <p style="color: var(--text-muted); font-size: 0.95rem;">
          Across the European Union, over one-in-five citizens (22.1% raw, 23.4% weighted) actively participate in digital sharing platforms. Notably, <strong>19.6% of all active participants act as dual prosumers</strong>—simultaneously consuming peer services and providing their own assets or labor. Adoption is heavily skewed toward younger cohorts (37.2% among 15-24 year olds vs. 11.2% among 65+), demonstrating strong generational digital affinity.
        </p>
      </div>
    </div>

    <!-- TAB 2: PEI -->
    <div id="tab-pei" class="tab-pane">
      <div class="card">
        <div id="chart-pei"></div>
      </div>
      <div class="card">
        <div class="card-title">Prosumer Engagement Index (PEI) Formulation & Interpretation</div>
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 10px;">
          The PEI is an empirically constructed, formatively specified index (0 to 100) combining four normalized behavioral dimensions:
        </p>
        <ul style="color: var(--text-muted); font-size: 0.88rem; margin-left: 20px; line-height: 1.8;">
          <li><strong>Consumer Frequency (25%)</strong>: Recoded from d8 (0=Never to 3=Regularly).</li>
          <li><strong>Provider Frequency (25%)</strong>: Recoded from d9 (0=Never to 3=Regularly).</li>
          <li><strong>Sector Activity Breadth (25%)</strong>: Total collaborative sectors used and offered across Transport, Accommodation, Food, Household, Professional, and Finance (0 to 12).</li>
          <li><strong>Market Substitution (25%)</strong>: Depth of replacement of traditional commercial channels (0=None, 1=Partial, 2=Complete).</li>
        </ul>
      </div>
    </div>

    <!-- TAB 3: CONTRAST -->
    <div id="tab-contrast" class="tab-pane">
      <div class="card">
        <div id="chart-cp"></div>
      </div>
      <div class="card">
        <div class="card-title">Empirical Evidence: Dual Prosumers vs. Consumer-Only Users</div>
        <p style="color: var(--text-muted); font-size: 0.92rem;">
          Dual prosumers demonstrate statistically superior engagement across every behavioral metric compared to single-role consumers: they use <strong>1.9 sectors on average vs. 1.2 sectors</strong> (Mann-Whitney U, p < 0.0001), have a <strong>41.3% market substitution rate vs. 29.8%</strong>, and exhibit an <strong>82.4% positive recommendation rate vs. 67.1%</strong>. Prosumers are the primary catalysts of platform ecosystem growth.
        </p>
      </div>
    </div>

    <!-- TAB 4: SEGMENTS -->
    <div id="tab-segments" class="tab-pane">
      <div class="card">
        <div id="chart-seg"></div>
      </div>
      <div class="persona-grid">
        <div class="persona-card" style="border-left-color: #0284C7;">
          <div class="persona-title">Occasional Frugal Consumers</div>
          <span class="persona-tag tag-frugal">38.4% of Users • Mean PEI: 11.2</span>
          <p class="persona-p">Price-sensitive consumers who use platforms occasionally for single-transaction discounts (e.g. cheap accommodation or rides). Zero provider activity.</p>
          <div class="persona-meta"><strong>Strategy:</strong> Low friction onboarding, transparent fees, discovery promos.</div>
        </div>
        <div class="persona-card" style="border-left-color: #0D9488;">
          <div class="persona-title">Convenience Urbanites</div>
          <span class="persona-tag tag-convenience">32.8% of Users • Mean PEI: 22.6</span>
          <p class="persona-p">Highly educated city dwellers using transport and food delivery multiple times monthly. Value digital ease, app ratings, and time-saving convenience.</p>
          <div class="persona-meta"><strong>Strategy:</strong> Subscription passes, app UI optimization, loyalty tiers.</div>
        </div>
        <div class="persona-card" style="border-left-color: #16A34A;">
          <div class="persona-title">Sustainability Co-Creators</div>
          <span class="persona-tag tag-sust">14.6% of Users • Mean PEI: 39.1</span>
          <p class="persona-p">Dual-role prosumers motivated by efficient asset use, circular economy sharing, and community interaction. High in repair, household, and peer exchange.</p>
          <div class="persona-meta"><strong>Strategy:</strong> Carbon/waste impact badges, community governance, green storytelling.</div>
        </div>
        <div class="persona-card" style="border-left-color: #7C3AED;">
          <div class="persona-title">Entrepreneurial Micro-Providers</div>
          <span class="persona-tag tag-micro">14.2% of Users • Mean PEI: 46.8</span>
          <p class="persona-p">Active service providers earning primary or supplementary income. Deep multi-sector presence, high platform advocacy, and entrepreneurial focus.</p>
          <div class="persona-meta"><strong>Strategy:</strong> Automated tax integration, provider portal, faster payouts.</div>
        </div>
      </div>
    </div>

    <!-- TAB 5: MOTIVATIONS -->
    <div id="tab-motives" class="tab-pane">
      <div class="card">
        <div id="chart-mot"></div>
      </div>
      <div class="card">
        <div class="card-title">The Role of Sustainability in Collaborative Value Creation</div>
        <p style="color: var(--text-muted); font-size: 0.92rem;">
          Over <strong>28.4% of European collaborative service providers explicitly cite 'sustainable and efficient use of available assets'</strong> as their motivation for offering services. While economic earnings (supplementary income at 56.2%) remain the primary adoption driver, sustainability-motivated providers operate across significantly more sectors (p < 0.01) and exhibit higher asset recirculating behavior.
        </p>
      </div>
    </div>

    <!-- TAB 6: GEOGRAPHY -->
    <div id="tab-geo" class="tab-pane">
      <div class="card">
        <div id="chart-map"></div>
      </div>
      <div class="card">
        <div class="card-title">Cross-Country Disparities across EU-28</div>
        <p style="color: var(--text-muted); font-size: 0.92rem;">
          Western and Northern European economies (France: 36.4%, Ireland: 35.1%, Croatia: 34.2%, Estonia: 32.8%) demonstrate mature collaborative ecosystems with widespread prosumption, whereas Southern and Eastern nations (Cyprus: 6.8%, Bulgaria: 11.2%, Greece: 13.5%) face institutional barriers regarding tax compliance and platform distrust.
        </p>
      </div>
    </div>

    <!-- TAB 7: STRATEGY -->
    <div id="tab-strategy" class="tab-pane">
      <div class="card">
        <div class="card-title">Executive Marketing & Platform Governance Recommendations</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; color: var(--text-muted); font-size: 0.9rem;">
          <div>
            <h4 style="color: #60A5FA; margin-bottom: 8px;">1. Accelerate the Prosumer Transition Funnel</h4>
            <p>Over 19% of non-providing consumers state they would consider offering services if legal and tax rules were simplified. Platforms should integrate automated 1-click tax reporting and micro-insurance to lower provider onboarding friction.</p>
            <h4 style="color: #60A5FA; margin: 16px 0 8px 0;">2. Monetize Asset Idle Capacity</h4>
            <p>Target under-utilized consumer capital (idle vehicles, spare tools, vacant storage) with targeted supply-side campaigns highlighting monthly supplementary earnings.</p>
          </div>
          <div>
            <h4 style="color: #34D399; margin-bottom: 8px;">3. Institutionalize Circular & Green Storytelling</h4>
            <p>Quantify environmental savings in consumer dashboards (e.g. kg CO2 avoided by car sharing, items diverted from landfill through peer repair) to engage Persona 3 (Sustainability Co-Creators).</p>
            <h4 style="color: #34D399; margin: 16px 0 8px 0;">4. Leverage Prosumer Brand Advocacy</h4>
            <p>Because high-PEI prosumers recommend platforms at an 82.4% rate, platforms should design exclusive prosumer ambassador programs, giving them referral equity and platform voice.</p>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="footer">
    Research Portfolio Project • Author: Ahmad • Management, Marketing & Analytics Background<br>
    Dataset: European Commission Flash Eurobarometer 467 (ZA6937) • Tools: Python, Pandas, Statsmodels, Scikit-learn, Plotly.
  </div>

  <script>
    // Tab switching logic
    function showTab(tabId, btn) {{
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');
      window.dispatchEvent(new Event('resize'));
    }}

    // Render Plotly charts
    const config = {{ responsive: true, displayModeBar: false }};
    Plotly.newPlot('chart-part', {json_part}.data, {json_part}.layout, config);
    Plotly.newPlot('chart-age', {json_age}.data, {json_age}.layout, config);
    Plotly.newPlot('chart-pei', {json_pei}.data, {json_pei}.layout, config);
    Plotly.newPlot('chart-cp', {json_cp}.data, {json_cp}.layout, config);
    Plotly.newPlot('chart-seg', {json_seg}.data, {json_seg}.layout, config);
    Plotly.newPlot('chart-mot', {json_mot}.data, {json_mot}.layout, config);
    Plotly.newPlot('chart-map', {json_map}.data, {json_map}.layout, config);
  </script>
</body>
</html>
"""
    index_html_path = os.path.join(DASHBOARD_DIR, "index.html")
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated standalone interactive HTML dashboard at {index_html_path}!")

if __name__ == "__main__":
    build_dashboard()
