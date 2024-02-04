import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="MAHARASHTRA University Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Load data
# df = pd.read_csv('data/CollegeCourseList.csv', encoding='ISO-8859-1')
try:
    df = pd.read_csv('data/CollegeCourseList.csv', encoding='ISO-8859-1')
except UnicodeDecodeError:
    df = pd.read_csv('data/CollegeCourseList.csv', encoding='cp1252')



# Filter out specific university
df_filtered = df[df['University'] != "MAHARASHTRA STATE BOARD OF SECONDARY AND HIGHER SECONDARY EDUCATION"]
unique_universities = df_filtered['University'].unique()
unique_course_categories = df_filtered['Course_Category'].unique()

#######################
# Sidebar
with st.sidebar:
    st.title('MAHARASHTRA University Dashboard')
    year_list = list(unique_universities)
    selected_University = st.selectbox('Select a University', year_list)
    df_selected_University = df_filtered[df_filtered.University == selected_University]
    df_selected_University_sorted = df_selected_University.sort_values(by="University", ascending=False)
    
    categories_list = list(unique_course_categories)
    selected_categories = st.selectbox('Select a Course', categories_list)
    df_selected_categories = df_filtered[df_filtered.Course_Category == selected_categories]
    df_selected_categories_sorted = df_selected_categories.sort_values(by="Course_Category", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Overall Universities')
    total_colleges = len(df_filtered['Sr_No'])
    total_unique_universities = df_filtered['University'].nunique()
    
    st.metric(label="Total Colleges", value=total_colleges, delta= 49)
    st.metric(label="Total Universities", value=total_unique_universities, delta = -78)

    st.markdown('#### Targeted Universities')
    universities = [
        "MUMBAI UNIVERSITY",
        "SAVITRIBAI PHULE PUNE UNIVERSITY",
        "SHIVAJI UNIVERSITY",
        "SOLAPUR UNIVERSITY"
    ]
    countt=0;
    # Create a column for each university metric
    for university in universities:
        # Filter dataframe for the university
        df_university = df_filtered[df_filtered.University == university]
        # Calculate the count of Sr.No, which is the total number of colleges for the university
        total_colleges = len(df_university['Sr_No'])
        countt=countt+total_colleges
        
        # Display the metric
    st.metric(label=" Total Colleges", value=countt)




with col[1]:
    st.markdown('#### Total Population')


with col[2]:
    st.markdown('#### Top States')

