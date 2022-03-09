import streamlit as st 
import pandas as pd 
import psycopg2
import datetime 
import sys
import connection.queries as queries
import connection.connection as connection

#Page configuration
st.set_page_config(layout="wide")

st.title("""
GetHired Community Dashboard
""")

#Sidebar configuration

date_min = st.sidebar.date_input(
     "Select initial date",
     datetime.date(2021, 12, 1))
date_max = st.sidebar.date_input(
     "Select End date",
     datetime.date(2023, 1, 1))

st.write('Range from: ' + str(date_min) + ' to ' + str(date_max) )


#SQL connection data

#Parameters
params_dict = {
    "database" : st.secrets.postgres.database,
    "user" : st.secrets.postgres.user,
    "password" : st.secrets.postgres.password,
    "host" : st.secrets.postgres.host,
    "port" : st.secrets.postgres.port

}

#Connection to the DB
connection1 = connection.connect(params_dict)

#Info about users 
users_df = connection.postgresql_to_dataframe(connection1, queries.queries_dict['users'], queries.queries_dict['users_columns'])
users_df['sign_up_date'] = pd.to_datetime(users_df['sign_up_date'])



#Get the data from a CSV
df_users  = pd.read_csv('data/USERS_MOCK_DATA_1.csv')


#Users per month analys
created_by_2 = users_df.groupby(pd.Grouper(key='sign_up_date',freq='M'))['id'].count()
created_by_indexes_2 = created_by_2.index

st.subheader('Users analysis')

st.subheader('New Users per month')
st.line_chart(data=created_by_2)


#Column adjustment
col1, col2 = st.columns([3, 1])
#col3, col4  = st.columns(2)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


#Analysis per country 

countries_count = df_users.groupby('pais')['id'].count()
countries_count_sorted = countries_count.sort_values( ascending=False)
countries_count_countries_name = countries_count_sorted.index


col1.subheader('Countries with most users')
col1.bar_chart(countries_count_sorted.head(6))


#Gender analysis 

df_gender = pd.read_csv('data/gender_mock_data.csv')
gender_analysis = (df_gender.groupby('genero').count() / df_gender.groupby('genero').count().sum()) * 100
col2.subheader('Gender analysis')
col2.bar_chart(data=gender_analysis)


#Challenges and community analysis 



st.subheader('Community analysis')
col3, col4  = st.columns(2)

#popular_post_count = challenges_df.groupby('discussion-post')['likes'].sum()
popular_post_count = connection.postgresql_to_dataframe(connection1, queries.queries_dict['networking_posts'], queries.queries_dict['networking_posts_columns'])
col3.subheader('Popular posts')
col3.table(popular_post_count)


#Networking categories analysis

categories_count = connection.postgresql_to_dataframe(connection1, queries.queries_dict['networking_categories'], queries.queries_dict['networking_categories_columns'])
col4.subheader('Popular categories')
col4.table(categories_count)




#Challenges analysis 

st.subheader('Challenges analysis')

challenges_df = connection.postgresql_to_dataframe(connection1, queries.queries_dict['challenges'], queries.queries_dict['challenges_columns'])
st.subheader('Popular challenges')
st.table(challenges_df)




