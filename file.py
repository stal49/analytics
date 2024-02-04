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

custom_css = """
<style>
    html, body, [class*="st-"] {
        font-family: 'Garamond', serif;
    }
</style>
"""

# custom_css = """
# <head>
# <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
# </head>
# <style>
#     html, body, [class*="st-"] {
#         font-family: 'Roboto', sans-serif;
#     }
# </style>
# """

st.markdown(custom_css, unsafe_allow_html=True)
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
    selected_University = st.selectbox('Select a University', ['All'] + list(year_list))
    # selected_University = st.selectbox('Select a University', year_list)
    df_selected_University = df_filtered[df_filtered.University == selected_University]
    df_selected_University_sorted = df_selected_University.sort_values(by="University", ascending=False)
    
    categories_list = list(unique_course_categories)
    selected_categories = st.selectbox('Select a Course Category', ['All'] + categories_list)
    # selected_categories = st.selectbox('Select a Course', categories_list)
    df_selected_categories = df_filtered[df_filtered.Course_Category == selected_categories]
    df_selected_categories_sorted = df_selected_categories.sort_values(by="Course_Category", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#######################

# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

def uvsc():
    st.markdown('#### Visualisation')

    # Calculate counts of Sr.No for each university
    university_counts = df_filtered.groupby('University')['Sr_No'].count().reset_index()

    # Rename the columns for clarity
    university_counts.columns = ['University', 'Count']

    # Use Altair to create the chart
    alt_chart = alt.Chart(university_counts).mark_bar().encode(
        x='University:N',
        y='Count:Q',
        tooltip=['University', 'Count']
    ).interactive()

    # Or use Plotly to create the chart
    plotly_chart_log = px.bar(university_counts, y='University', x='Count', text='Count', orientation='h')
    plotly_chart_log.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    plotly_chart_log.update_layout(
        xaxis=dict(
            type='log',
            title='Log of Count'
        ),
        title='University vs Count of Colleges (Log Scale)'
    )

    if st.button('Show college_counts'):
        st.altair_chart(alt_chart, use_container_width=True)

    if not st.button('Hide Both'):
        st.plotly_chart(plotly_chart_log, use_container_width=True)

def ccc():
    course_category_counts = df_filtered['Course_Category'].value_counts().reset_index()
    course_category_counts.columns = ['Course_Category', 'Count']

    # Create a bar chart using Plotly
    fig = px.bar(course_category_counts, x='Course_Category', y='Count',
                title='Count of Each Course Category')

    # Show the plotly figure
    st.plotly_chart(fig, use_container_width=True)

def pieofu():
    universities_of_interest = [
        "MUMBAI UNIVERSITY",
        "SAVITRIBAI PHULE PUNE UNIVERSITY",
        "SHIVAJI UNIVERSITY",
        "SOLAPUR UNIVERSITY"
    ]
    df_filtered = df[df['University'].isin(universities_of_interest)]

    # Count the occurrences of College_Name for each University
    college_counts = df_filtered.groupby('University')['College_Name'].nunique().reset_index()
    college_counts.columns = ['University', 'Count']

    # Create a pie chart using Plotly
    fig = px.pie(college_counts, values='Count', names='University', title='Count of Colleges under Target Universities')

    # Show the plotly figure
    st.plotly_chart(fig, use_container_width=True)

def showDistrictCount():
    district_college_counts = df.groupby('District')['College_Name'].nunique().reset_index()
    district_college_counts.columns = ['District', 'College_Count']

    # Get the maximum number of colleges in any district for the progress bar
    max_college_count = district_college_counts['College_Count'].max()

    # Display each district with its progress bar
    if 'show_progress_bars' not in st.session_state:
        st.session_state['show_progress_bars'] = True

    # Button to toggle the visibility of progress bars
    if st.button('Show District wise count'):
        st.session_state['show_progress_bars'] = not st.session_state['show_progress_bars']

    # Conditional rendering of progress bars based on the toggle state
    if st.session_state['show_progress_bars']:
        for index, row in district_college_counts.iterrows():
            # Display the district name and count
            st.text(f"{row['District']} ({row['College_Count']})")

            # Create a progress bar
            progress = row['College_Count'] / max_college_count
            st.progress(progress)

with st.container():
    # Create the first main column
    with st.container():
        col1, col2 = st.columns(2)  # This creates two columns (or a two-column row)
        with col1:
            if selected_University != 'All' and selected_categories == 'All':
                df_filtered_final = df_filtered[df_filtered['University'] == selected_University]
            elif selected_University == 'All' and selected_categories != 'All':
                df_filtered_final = df_filtered[df_filtered['Course_Category'] == selected_categories]
            elif selected_University != 'All' and selected_categories != 'All':
                df_filtered_final = df_filtered[(df_filtered['University'] == selected_University) &
                                        (df_filtered['Course_Category'] == selected_categories)]
            else:
                df_filtered_final = df_filtered
            # Create a row within the main column
            
            # df_filtered_university = df_filtered[df_filtered['University'] == selected_University]
            # df_filtered_category = df_filtered_university[df_filtered_university['Course_Category'] == selected_categories]

            # Display count of colleges under the selected university and course category
            st.write(f"Count of Colleges under {selected_University} offering {selected_categories}: {len(df_filtered_final)}")

            # Display the list of colleges under the selected university and course category
            st.write(f"List of Colleges under {selected_University} offering {selected_categories}:")
            st.write(df_filtered_final[['College_Name']].drop_duplicates())
            
        with col2:
            universities = [
                "MUMBAI UNIVERSITY",
                "SAVITRIBAI PHULE PUNE UNIVERSITY",
                "SHIVAJI UNIVERSITY",
                "SOLAPUR UNIVERSITY"
            ]

            # Display each university name in bold
            for uni in universities:
                st.markdown(f"* #### {uni}")

    # Create the second main column (if needed)
    with st.container():
        col = st.columns((1.2, 4.5, 2.5), gap='medium')
        if 'show_col3' not in st.session_state:
            st.session_state['show_col3'] = True  # Start with column 3 visible

        # Button to toggle the visibility of column 3
        if st.button('Toggle Column 3'):
            st.session_state['show_col3'] = not st.session_state['show_col3']
            if not st.session_state['show_col3']:
                col = st.columns((1.2, 4.5, 0.1))
        with col[0]:
            st.markdown('#### Overall Universities')
            total_colleges = len(df_filtered['Sr_No'])
            total_unique_universities = df_filtered['University'].nunique()
            
            st.metric(label="Total Colleges", value=total_colleges)
            st.metric(label="Total Universities", value=total_unique_universities)

            st.markdown('#### Target')
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
            st.metric(label=" Total Universities", value=len(universities), delta = len(universities))
            donut_chart_greater = make_donut(34, '% Colleges', 'green')
            donut_chart_less = make_donut(8.1, '% Universities', 'blue')

            migrations_col = st.columns((0.2, 1, 0.2))
            with migrations_col[1]:
                st.write('% of Total colleges')
                st.altair_chart(donut_chart_greater)
                st.write('% of Total Universities')
                st.altair_chart(donut_chart_less)
            
        with col[1]:
            uvsc()
            ccc()
            pieofu()
            showDistrictCount()
            
            


        if st.session_state['show_col3']:
            with col[2]:
                st.markdown('#### All Universities')
                # Assuming 'Sr.No' represents a unique identifier for each college
                college_counts = df.groupby('University')['Sr_No'].nunique().reset_index()
                # print(college_counts)

                st.dataframe(college_counts,
                            column_order=("University", "Sr_No"),
                            hide_index=True,
                            width=None,
                            column_config={
                                "University": st.column_config.TextColumn(
                                    "University",
                                ),
                                "Sr_No": st.column_config.TextColumn(
                                    "College Count",
                                ),
                                # "Sr_No": st.column_config.ProgressColumn(
                                #     "College Count",
                                #     format="%f",
                                #     min_value=0,
                                #     max_value=max(college_counts.Sr_No),
                                #  )
                                }
                            )
                
                with st.expander('About', expanded=True):
                    st.write('''
                        - Data: [Our Analysis](https://www.google.com).
                        - :orange[**Visualisation**]: Interactive you can hover a mouse over it to know more
                        - :orange[**Data**]: All the data is updated with MAHARASHTRA EDUCATION report
                        ''')




                # col1, col2 = st.columns(2)
                # with col1:
                #     if st.button('Show Altair Chart'):
                #         st.altair_chart(alt_chart, use_container_width=True)

                # with col2:
                #     if st.button('Show Plotly Chart'):
                #         st.plotly_chart(plotly_chart_log, use_container_width=True)