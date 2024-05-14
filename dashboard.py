#=======================================================================
## Importing libraries and setting up streamlit web app

# Importing the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title = "Superstore",
    page_icon= ':bar_chart:',
    layout= 'wide'
)

st.title(":chart_with_upwards_trend: Superstore Exploratory Data Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")

    
st.sidebar.header("Choose your Filter for analysis")
    # Create for region
region = st.sidebar.multiselect("Select your Region", df["Region"].unique())

if not region:
        df2 = df.copy()
else:
        df2 = df[df["Region"].isin(region)]

    # Create for state
state = st.sidebar.multiselect("Select your State", df2["State"].unique())

if not state:
        df3 = df2.copy()
else:
        df3 = df2[df2['State'].isin(state)]

    # Create for city
city = st.sidebar.multiselect("Select your City", df3["City"].unique())
    
if not city:
        df4 = df3.copy()
else:
        df4 = df3[df3["City"].isin(city)]

if not region and not state and not city:
        filtered_df = df
elif not state and not city:
        filtered_df = df2
elif not region and not city:
        filtered_df = df3
elif state and city:
        filtered_df = df[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
        filtered_df = df[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
        filtered_df = df[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
        filtered_df = df4
else:
        filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]




col1, col2 = st.columns((2))
filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

StartDate = pd.to_datetime(filtered_df["Order Date"]).min()
EndDate = pd.to_datetime(filtered_df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", StartDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", EndDate))

df_ = filtered_df[(filtered_df["Order Date"] >= date1) & (filtered_df["Order Date"] <= date2)].copy()

st.title("Dataset")
st.dataframe(df_)
st.write('This Dataset has dimensions :',df_.shape)

category_df = df_.groupby(by=["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Category-wise Sales")
    fig = px.bar(category_df, x= "Category", y= "Sales",text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)

with col2:
    st.subheader("Region-wise Sales")
    fig = px.pie(df_, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width = True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode("utf_8")
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = "Click here to download the data as a CSV file")
    
with cl2:
    with st.expander("Region_ViewData"):
        region = df_.groupby(by = "Region", as_index= False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode("utf_8")
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = "Click here to download the data as a CSV file")

# Assuming "Order Date" column is in string format, convert it to datetime
filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

# Now you can use the .dt accessor on "Order Date" column
df_["month_year"] = df_["Order Date"].dt.to_period("M")

st.subheader("Time Series Analysis")
linechart = pd.DataFrame(df_.groupby(df_["month_year"].dt.strftime("%b %Y"))["Sales"].sum().reset_index())
linechart = linechart.sort_values(by="month_year", ascending=True)
fig2= px.line(linechart, x= "month_year", y = "Sales", labels = {"Sales" : "Amount ($)"}, height = 500, width = 1000, template = "gridon")
st.plotly_chart(fig2,use_container_width = True)

with st.expander("View TimeSeries Data"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index = False).encode("utf_8")
    st.download_button("Download Data", data = csv, file_name = "TimeSeries.csv", mime = "text/csv",
                        help = "Click here to download the data as a CSV file")
# T is for transpose

# Create a Treemap based on Region, Category and Sub-category
st.subheader("Hierachial view of Sales using TreeMap")
fig3 = px.treemap(df_, path = ["Region","Category","Sub-Category"], values = "Sales", hover_data = ["Sales"],
                  color = "Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width = True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader("Segment-wise Sales")
    fig = px.pie(df_, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = df_["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width = True)

with chart2:
    st.subheader("Category-wise Profits")
    fig = px.pie(df_, values = "Profit", names = "Category", template = "gridon")
    fig.update_traces(text = df_["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width = True)

co1, co2 = st.columns(2)
with co1:
    with st.expander("Segment_ViewData"):
        segment = df_.groupby(by = "Segment", as_index= False)["Sales"].sum()
        st.write(segment.style.background_gradient(cmap="Blues"))
        csv = df_.to_csv(index = False).encode("utf_8")
        st.download_button("Download Data", data = csv, file_name = "Segment.csv", mime = "text/csv",
                            help = "Click here to download the data as a CSV file")

with co2:
    with st.expander("Category_ViewData"):
        Category_Profits = df_.groupby(by = "Category", as_index= False)["Profit"].sum()
        st.write(Category_Profits.style.background_gradient(cmap="Oranges"))
        csv = df_.to_csv(index = False).encode("utf_8")
        st.download_button("Download Data", data = csv, file_name = "Category_Profits.csv", mime = "text/csv",
                            help = "Click here to download the data as a CSV file")


import plotly.figure_factory as ff

st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width = True)

    st.markdown("Month wise Sub-Category Table")
    df_["month"] = df_["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = df_, values = "Sales", index = ["Sub-Category"], columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap = "Blues"))

# Create a scatter plot
data1 = px.scatter(df_, x = "Sales", y = "Profit", size = "Quantity")
data1['layout'].update(title = "Relationship between sales and profits using Scatter Plot.",
                       titlefont = dict(size = 20), xaxis = dict(title = "Sales",titlefont = dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size = 19)))
st.plotly_chart(data1, use_container_width = True)

with st.expander("View Data"):
    st.write(df_.iloc[:500,1:20:2].style.background_gradient(cmap = "Oranges"))

# Download Original Dataset
csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download Data", data = csv, file_name = "Data.csv", mime = "text.csv")


