import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour):
  hour_count_df =  hour.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_df

def count_by_day_df(day):
    day_df_count_2011 = day.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day):
   reg =  day.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg = reg.reset_index()
   reg.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg

def total_casual_df(day):
   cas =  day.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas = cas.reset_index()
   cas.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas

def sum_order (hour):
    sum_order_items_df = hour.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day): 
    season = day.groupby(by="season").count_cr.sum().reset_index() 
    return season

days = pd.read_csv("day_clean.csv")
hours = pd.read_csv("hour_clean.csv")

datetime_columns = ["dteday"]
days.sort_values(by="dteday", inplace=True)
days.reset_index(inplace=True)   

hours.sort_values(by="dteday", inplace=True)
hours.reset_index(inplace=True)

for column in datetime_columns:
    days[column] = pd.to_datetime(days[column])
    hours[column] = pd.to_datetime(hours[column])

min_date_days = days["dteday"].min()
max_date_days = days["dteday"].max()

min_date_hour = hours["dteday"].min()
max_date_hour = hours["dteday"].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("mountain-bike-4297972_1280.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days[(days["dteday"] >= str(start_date)) & 
                       (days["dteday"] <= str(end_date))]

main_df_hour = hours[(hours["dteday"] >= str(start_date)) & 
                        (hours["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg = total_registered_df(main_df_days)
cas = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Bagaimana performa penyewaan dalam beberapa tahun 2011 - 2012?")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days["dteday"],
    days["count_cr"],
    marker='*', 
    linewidth=2,
    color="#90D5FF"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Perbandingan Registered dan Casual
st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  
st.pyplot(fig1)


# Perbandingan musim
st.subheader("Musim apa yang paling banyak penyewa?")

colors = ["#9E9E9E", "#9E9E9E", "#9E9E9E", "#90D5FF"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count_cr", 
        x="season",
        data=season.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


# Membuat grafik penyewaan perhari
st.subheader("Intensitas penyewaan per hari")
day_of = days.groupby(by="one_of_week")['one_of_week'].count().reset_index(name="count")

fig, ax = plt.subplots(figsize=(35, 15))

sns.barplot(x="one_of_week", y="count", data=day_of, color="lightblue", ax=ax)
ax.set_title("Data Hari Penyewaan Sepeda", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


st.subheader("Jam paling banyak dan aling sedikit")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

color1 = ["#9E9E9E", "#9E9E9E", "#96F97B", "#9E9E9E", "#9E9E9E"]
color2 = ["#9E9E9E", "#9E9E9E", "#9E9E9E", "#9E9E9E", "#FF3333"]

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=color1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=color2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

