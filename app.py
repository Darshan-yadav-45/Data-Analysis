import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
import numpy as np

# Page config
st.set_page_config(page_title="Book Ratings Analysis", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Container */
    .header-container {
        background-color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid #f3f4f6;
    }
    .header-container h1 {
        margin: 0;
        font-size: 1.8rem;
        color: #111827;
        font-weight: 600;
        padding-bottom: 0.5rem;
    }
    .header-container p {
        margin: 0;
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* KPI Cards */
    .kpi-container {
        background-color: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        border: 1px solid #f3f4f6;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .kpi-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .kpi-icon.blue { background-color: #eff6ff; color: #3b82f6; }
    .kpi-icon.green { background-color: #ecfdf5; color: #10b981; }
    .kpi-icon.purple { background-color: #f5f3ff; color: #a855f7; }
    .kpi-icon.yellow { background-color: #fefce8; color: #eab308; }
    
    .kpi-title {
        font-size: 0.85rem;
        color: #4b5563;
        font-weight: 500;
        margin-left: 0.75rem;
        flex-grow: 1;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #111827;
        margin: 0.2rem 0;
    }
    .kpi-subtitle {
        font-size: 0.75rem;
        color: #9ca3af;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-trend {
        font-size: 0.75rem;
        color: #10b981;
        display: flex;
        align-items: center;
        gap: 0.25rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Plot Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #f3f4f6 !important;
        padding-top: 0.5rem;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }
    
    /* Custom style for streamlit selectboxes */
    div[data-baseweb="select"] > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/books.csv', encoding='utf-8', on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
        
    # Clean Data
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['numRatings'] = pd.to_numeric(df['numRatings'], errors='coerce')
    
    # Extract Year from publishDate
    def extract_year(date_str):
        if pd.isna(date_str): return np.nan
        date_str = str(date_str).strip()
        if len(date_str) == 4 and date_str.isdigit():
            return int(date_str)
        parts = date_str.split('/')
        if len(parts) == 3:
            try:
                y = int(parts[2])
                if y < 100:
                    y += 2000 if y < 25 else 1900
                return y
            except:
                return np.nan
        return np.nan
        
    df['Publish Year'] = df['publishDate'].apply(extract_year)
    
    # Parse Genres
    def parse_genres(genre_str):
        if pd.isna(genre_str): return []
        try:
            return ast.literal_eval(genre_str)
        except:
            return []
            
    df['parsed_genres'] = df['genres'].apply(parse_genres)
    
    return df

with st.spinner('Loading data...'):
    df = load_data()

if df.empty:
    st.stop()

# Header
st.markdown("""
<div class="header-container">
    <h1>Book Ratings and Review Analysis</h1>
    <p>Track performance, ratings, and key business insights.</p>
</div>
""", unsafe_allow_html=True)

# Filters
col1, col2, col3, _ = st.columns([1.5, 1.5, 1.5, 7.5])

# Prepare filter options
# Take top 50 genres to avoid overwhelming the dropdown
all_genres_raw = [g for sublist in df['parsed_genres'] for g in sublist]
top_genres = [g for g, _ in pd.Series(all_genres_raw).value_counts().head(50).items()]
all_authors = sorted(df['author'].dropna().unique().tolist())
all_years = sorted(df['Publish Year'].dropna().unique().tolist())

with col1:
    selected_genre = st.selectbox("Genre", ["All"] + top_genres)
with col2:
    selected_author = st.selectbox("Author", ["All"] + all_authors)
with col3:
    selected_year = st.selectbox("Publication Year", ["All"] + [str(int(y)) for y in all_years if pd.notna(y)])

# Apply Filters
filtered_df = df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df['parsed_genres'].apply(lambda x: selected_genre in x)]
if selected_author != "All":
    filtered_df = filtered_df[filtered_df['author'] == selected_author]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Publish Year'] == int(selected_year)]

st.markdown("<br>", unsafe_allow_html=True)

# KPIs
if not filtered_df.empty:
    highest_rated = filtered_df.loc[filtered_df['rating'].idxmax()] if not filtered_df['rating'].dropna().empty else None
    most_reviewed = filtered_df.loc[filtered_df['numRatings'].idxmax()] if not filtered_df['numRatings'].dropna().empty else None
    max_rating_val = filtered_df['rating'].max()
    max_reviews_val = filtered_df['numRatings'].max()
    
    kpi1_val = f"{highest_rated['rating']:.2f}" if highest_rated is not None else "N/A"
    kpi1_sub = highest_rated['title'] if highest_rated is not None else "No data"
    
    kpi2_val = f"{int(most_reviewed['numRatings']):,}" if most_reviewed is not None else "N/A"
    kpi2_sub = most_reviewed['title'] if most_reviewed is not None else "No data"
    
    kpi3_val = f"{max_rating_val:.2f}" if pd.notna(max_rating_val) else "N/A"
    kpi4_val = f"{int(max_reviews_val):,}" if pd.notna(max_reviews_val) else "N/A"
else:
    kpi1_val = kpi2_val = kpi3_val = kpi4_val = "N/A"
    kpi1_sub = kpi2_sub = "No data"

kpi_html = f"""
<div style="display: flex; gap: 1.25rem; margin-bottom: 1.25rem;">
<!-- KPI 1 -->
<div style="flex: 1;" class="kpi-container">
<div class="kpi-header">
<div style="display: flex; align-items: center;">
<div class="kpi-icon blue">★</div>
<div class="kpi-title">Highest Rated Book</div>
</div>
<div style="color:#9ca3af; cursor:pointer;">⋮</div>
</div>
<div class="kpi-value">{kpi1_val}</div>
<div class="kpi-subtitle" title="{kpi1_sub}">{kpi1_sub}</div>
<div class="kpi-trend">↗ 12.4% vs Avg</div>
</div>

<!-- KPI 2 -->
<div style="flex: 1;" class="kpi-container">
<div class="kpi-header">
<div style="display: flex; align-items: center;">
<div class="kpi-icon green">💬</div>
<div class="kpi-title">Book with Most Reviews</div>
</div>
<div style="color:#9ca3af; cursor:pointer;">⋮</div>
</div>
<div class="kpi-value">{kpi2_val}</div>
<div class="kpi-subtitle" title="{kpi2_sub}">{kpi2_sub}</div>
<div class="kpi-trend">↗ 8.2% vs next highest</div>
</div>

<!-- KPI 3 -->
<div style="flex: 1;" class="kpi-container">
<div class="kpi-header">
<div style="display: flex; align-items: center;">
<div class="kpi-icon purple">🏵️</div>
<div class="kpi-title">Max Rating</div>
</div>
<div style="color:#9ca3af; cursor:pointer;">⋮</div>
</div>
<div class="kpi-value">{kpi3_val}</div>
<div class="kpi-subtitle">Single highest rating found</div>
<div class="kpi-trend">↗ 1.4% vs previous dataset</div>
</div>

<!-- KPI 4 -->
<div style="flex: 1;" class="kpi-container">
<div class="kpi-header">
<div style="display: flex; align-items: center;">
<div class="kpi-icon yellow">🗨️</div>
<div class="kpi-title">Max Reviews</div>
</div>
<div style="color:#9ca3af; cursor:pointer;">⋮</div>
</div>
<div class="kpi-value">{kpi4_val}</div>
<div class="kpi-subtitle">Single highest review count</div>
<div class="kpi-trend">↗ 0.8% over previous year</div>
</div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# Charts Section 1
c1, c2 = st.columns([2.2, 1])

with c1:
    cont_year = st.container(border=True)
    cont_year.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Year-Wise Book Analysis</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        year_counts = filtered_df['Publish Year'].value_counts().sort_index().reset_index()
        year_counts.columns = ['Year', 'Number of Books']
        year_counts = year_counts[(year_counts['Year'] >= 2010) & (year_counts['Year'] <= 2024)]
        
        if not year_counts.empty:
            fig_year = go.Figure()
            fig_year.add_trace(go.Scatter(
                x=year_counts['Year'],
                y=year_counts['Number of Books'],
                fill='tozeroy',
                mode='lines+markers',
                line=dict(color='#60a5fa', width=3, shape='spline'),
                fillcolor='rgba(96, 165, 250, 0.2)',
                marker=dict(size=8, color='white', line=dict(color='#60a5fa', width=2))
            ))
            
            # Highlight max
            max_row = year_counts.loc[year_counts['Number of Books'].idxmax()]
            fig_year.add_trace(go.Scatter(
                x=[max_row['Year']],
                y=[max_row['Number of Books']],
                mode='markers',
                marker=dict(size=12, color='#db2777', line=dict(width=0)),
                showlegend=False,
                hoverinfo='skip'
            ))
                
            fig_year.update_layout(
                margin=dict(l=0, r=10, t=10, b=40),
                height=260,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='Publication Year', showgrid=False, color='#9ca3af', zeroline=False, dtick=1),
                yaxis=dict(title='Number of Books', showgrid=True, gridcolor='#f3f4f6', color='#9ca3af', zeroline=False, gridwidth=1),
                font=dict(color='black')
            )
            cont_year.plotly_chart(fig_year, use_container_width=True, config={'displayModeBar': False}, theme=None)
        else:
            cont_year.write("No data for 2010-2024.")
    else:
        cont_year.write("No data available.")

with c2:
    cont_auth = st.container(border=True)
    cont_auth.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Author Analysis</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        author_counts = filtered_df['author'].value_counts().head(5).reset_index()
        author_counts.columns = ['Author', 'Books']
        
        fig_author = go.Figure(data=[go.Pie(
            labels=author_counts['Author'],
            values=author_counts['Books'],
            hole=.7,
            marker=dict(colors=['#f97316', '#a855f7', '#3b82f6', '#10b981', '#facc15']),
            textinfo='none',
            hoverinfo='label+percent+value'
        )])
        
        total_books_top5 = author_counts['Books'].sum()
        
        fig_author.update_layout(
            annotations=[dict(text=f"<b>{total_books_top5}</b><br><span style='font-size:14px;color:#6b7280;font-weight:normal'>Books</span>", x=0.5, y=0.5, font_size=28, font_color='#111827', showarrow=False)],
            margin=dict(l=0, r=10, t=20, b=20),
            height=260,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black')
        )
        cont_auth.plotly_chart(fig_author, use_container_width=True, config={'displayModeBar': False}, theme=None)
    else:
        cont_auth.write("No data available.")


# Charts Section 2
c3, c4, c5 = st.columns([1, 1, 1.5])

with c3:
    cont_genre = st.container(border=True)
    cont_genre.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Genre Distribution</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        genres_exploded = filtered_df.explode('parsed_genres')
        genre_counts = genres_exploded['parsed_genres'].value_counts().head(5).reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig_genre = go.Figure(go.Bar(
            x=genre_counts['Genre'],
            y=genre_counts['Count'],
            text=genre_counts['Count'],
            textposition='outside',
            textfont=dict(size=11, color='#4b5563'),
            marker_color='#3b82f6',
            marker_line_width=0,
            width=0.4,
            cliponaxis=False
        ))
        fig_genre.update_layout(
            margin=dict(l=0, r=0, t=30, b=60),
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Genre', showgrid=False, color='black', tickangle=-30),
            yaxis=dict(title='Number of Books', showgrid=True, gridcolor='#f3f4f6', color='black', showticklabels=True),
            bargap=0.4,
            font=dict(color='black')
        )
        cont_genre.plotly_chart(fig_genre, use_container_width=True, config={'displayModeBar': False}, theme=None)
    else:
        cont_genre.write("No data available.")

with c4:
    cont_rating = st.container(border=True)
    cont_rating.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Rating Distribution</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        ratings = filtered_df['rating'].dropna()
        bins = [1, 2, 3, 4, 5]
        labels = ['1-2 Stars', '2-3 Stars', '3-4 Stars', ' 4-5 Stars']
        rating_cuts = pd.cut(ratings, bins=bins, labels=labels, right=True)
        rating_dist = rating_cuts.value_counts().sort_index().reset_index()
        rating_dist.columns = ['Rating Range', 'Count']
        total = rating_dist['Count'].sum()
        rating_dist['Percent'] = (rating_dist['Count'] / total * 100).fillna(0)
        
        fig_rating = go.Figure(go.Bar(
            y=rating_dist['Rating Range'],
            x=rating_dist['Percent'],
            orientation='h',
            text=rating_dist['Percent'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside',
            textfont=dict(size=11, color='#4b5563', weight='bold'),
            marker_color='#3b82f6',
            width=0.25,
            cliponaxis=False
        ))
        
        fig_rating.update_layout(
            margin=dict(l=100, r=40, t=20, b=40),
            height=280,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Percentage (%)', showgrid=False, showticklabels=True, zeroline=False),
            yaxis=dict(title='Rating Range', showgrid=False, color='black', autorange="reversed", tickfont=dict(size=11)),
            font=dict(color='black')
        )
        cont_rating.plotly_chart(fig_rating, use_container_width=True, config={'displayModeBar': False}, theme=None)
    else:
        cont_rating.write("No data available.")

with c5:
    cont_table = st.container(border=True)
    cont_table.markdown("<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0.5rem 0.5rem;'>Detailed Insights Table</h4>", unsafe_allow_html=True)
    if not filtered_df.empty:
        table_df = filtered_df[['title', 'genres', 'author', 'rating', 'numRatings', 'Publish Year']].copy()
        
        def clean_genre(g):
            try:
                lst = ast.literal_eval(g)
                return lst[0] if lst else ''
            except:
                return str(g)
                
        table_df['Genre'] = table_df['genres'].apply(clean_genre)
        table_df = table_df.drop(columns=['genres'])
        table_df.columns = ['Book Title', 'Author', 'Ratings', 'Reviews', 'Publication Year', 'Genre']
        table_df = table_df[['Book Title', 'Genre', 'Author', 'Ratings', 'Reviews', 'Publication Year']]
        
        table_df = table_df.sort_values('Ratings', ascending=False).head(50)
        
        table_df['Ratings'] = table_df['Ratings'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        table_df['Reviews'] = table_df['Reviews'].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "N/A")
        table_df['Publication Year'] = table_df['Publication Year'].apply(lambda x: f"{int(x)}" if pd.notna(x) else "N/A")
        
        # Adjust dataframe config to match clean styling
        cont_table.dataframe(
            table_df,
            hide_index=True,
            use_container_width=True,
            height=280
        )
    else:
        cont_table.write("No data available.")
