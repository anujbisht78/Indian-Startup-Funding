import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv('startup_cleaned.csv')

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['Year']=df['date'].dt.year


def load_investor_detail(investor):
    st.title(investor)
    
    # load the recent 5 investment 
    last_5df=df[df['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']].head()
    
    st.subheader('Most Rrcent Investment')
    st.dataframe(last_5df)
    
    col1,col2=st.columns(2)
    

    with col1:
        
        #Biggest Investments
        big_invest=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        
        st.subheader('Biggest Investments')
        # st.dataframe(big_invest)
        fig, ax = plt.subplots()
        ax.bar(big_invest.index, big_invest.values)

        st.pyplot(fig)
        
        
    # Generaly investment
    with col2:
        
        gen_invest= df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors Investments')
        # st.dataframe(big_invest)
        fig1, ax1 = plt.subplots()
        ax1.pie(gen_invest, labels=gen_invest.index, autopct="%0.01f%%")

        st.pyplot(fig1)
        
        
    # Year on Year Investment
    
    # extracting the year
    df['Year']=df['date'].dt.year
    
    yoy=df[df['investors'].str.contains(investor)].groupby('Year')['amount'].sum()
    
    st.subheader('Year-on-Year Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(yoy.index,yoy.values)

    st.pyplot(fig2)
    
    

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])


def load_overall_analysis():
    st.title('Overall Analysis')
    
    # total Investments in Indian Startup
    total=round(df['amount'].sum())
    
    
    #Max investment in Indian Startup
    max_invest=df.groupby('startup')['amount'].max().sort_values(ascending=False).iloc[[0]][0]
    
    # Avg funding
    avg_fund=df.groupby('startup')['amount'].sum().mean()
    
    # total Funding startups
    total_startups = df['startup'].nunique()
    
    col1,col2,col3,col4=st.columns(4)
    
    with col1:
        st.metric("Total Investment: ",str(total)+" Cr")

        
    with col2:
        st.metric("Maximum Investment: ",str(max_invest)+" Cr")
        
    
    with col3:
        st.metric("Avg Funding: ",str(round(avg_fund))+" Cr")
        

    with col4:
        st.metric("Funded Startups: ",str(total_startups))
        

    st.header('Month-on-Month Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
    
        temp_df=df.groupby(['Year','month'])['amount'].sum().reset_index()
        temp_df['x-axis']=temp_df['month'].astype('str') + '-' + temp_df['Year'].astype('str')
        
        temp_df['x-axis']=temp_df['month'].astype('str') + '-' + temp_df['Year'].astype('str')
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x-axis'],temp_df['amount'])

        st.pyplot(fig3)
        
    else:
        temp_df=df.groupby(['Year','month'])['startup'].count().reset_index()
        
        temp_df['x-axis']=temp_df['month'].astype('str') + '-' + temp_df['Year'].astype('str')
        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x-axis'],temp_df['startup'])

        st.pyplot(fig3)
        
        
    
           
    

if option=='Overall Analysis':
    
    load_overall_analysis()
        

elif option=='Startup':
    
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    
    selected_investor=st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        
        load_investor_detail(selected_investor)
        
    # st.title('Investor Analysis')