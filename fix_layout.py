import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_old = """    /* Plot Containers */
    .plot-container {
        background-color: white;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 1rem;
        border: 1px solid #f3f4f6;
        height: 100%;
    }
    .plot-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 1rem;
    }"""
css_new = """    /* Plot Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #f3f4f6 !important;
        padding-top: 0.5rem;
    }"""
content = content.replace(css_old, css_new)

# 2. Update Charts
chart_replacements = [
    (
        "    st.markdown('<div class=\"plot-container\"><div class=\"plot-title\">Year-Wise Book Analysis</div>', unsafe_allow_html=True)",
        "    cont_year = st.container(border=True)\n    cont_year.markdown(\"<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Year-Wise Book Analysis</h4>\", unsafe_allow_html=True)",
        "st.plotly_chart(fig_year", "cont_year.plotly_chart(fig_year",
        "st.write(\"No data", "cont_year.write(\"No data"
    ),
    (
        "    st.markdown('<div class=\"plot-container\"><div class=\"plot-title\">Author Analysis</div>', unsafe_allow_html=True)",
        "    cont_auth = st.container(border=True)\n    cont_auth.markdown(\"<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Author Analysis</h4>\", unsafe_allow_html=True)",
        "st.plotly_chart(fig_author", "cont_auth.plotly_chart(fig_author",
        "st.write(\"No data", "cont_auth.write(\"No data"
    ),
    (
        "    st.markdown('<div class=\"plot-container\"><div class=\"plot-title\">Genre Distribution</div>', unsafe_allow_html=True)",
        "    cont_genre = st.container(border=True)\n    cont_genre.markdown(\"<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Genre Distribution</h4>\", unsafe_allow_html=True)",
        "st.plotly_chart(fig_genre", "cont_genre.plotly_chart(fig_genre",
        "st.write(\"No data", "cont_genre.write(\"No data"
    ),
    (
        "    st.markdown('<div class=\"plot-container\"><div class=\"plot-title\">Rating Distribution</div>', unsafe_allow_html=True)",
        "    cont_rating = st.container(border=True)\n    cont_rating.markdown(\"<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0 0.5rem;'>Rating Distribution</h4>\", unsafe_allow_html=True)",
        "st.plotly_chart(fig_rating", "cont_rating.plotly_chart(fig_rating",
        "st.write(\"No data", "cont_rating.write(\"No data"
    ),
    (
        "    st.markdown('<div class=\"plot-container\" style=\"overflow: hidden;\"><div class=\"plot-title\">Detailed Insights Table</div>', unsafe_allow_html=True)",
        "    cont_table = st.container(border=True)\n    cont_table.markdown(\"<h4 style='font-size: 0.95rem; font-weight: 600; color: #111827; margin: 0.5rem 0 0.5rem 0.5rem;'>Detailed Insights Table</h4>\", unsafe_allow_html=True)",
        "st.dataframe(", "cont_table.dataframe(",
        "st.write(\"No data", "cont_table.write(\"No data"
    )
]

for title_old, title_new, plt_old, plt_new, err_old, err_new in chart_replacements:
    content = content.replace(title_old, title_new)
    content = content.replace(plt_old, plt_new)
    content = content.replace(err_old, err_new)

# Remove all st.markdown('</div>', unsafe_allow_html=True)
content = content.replace("    st.markdown('</div>', unsafe_allow_html=True)\n", "")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
