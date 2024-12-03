import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import DataAnalyzer
from babel.numbers import format_currency
sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv(
    './Ecommerce-public-dataset/all_data.csv')
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv(
    './Ecommerce-public-dataset/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Yusfi Syawali")

    # Logo Image
    st.image("./dashboard/dicoding.jpg")

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) &
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)

daily_orders_data = function.create_daily_orders_data()
monthly_data = function.create_order_pattern_df()
sum_spend_df = function.create_sum_spend_df()
monthly_spend_data = function.create_monthly_spend_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_data = function.create_sum_order_items_data()
order_status, common_status = function.create_order_status()

# Title
st.header("E-Commerce Dashboard")

# Daily Orders
st.subheader("Monthly Orders")

col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_data["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = format_currency(
        daily_orders_data["revenue"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(
    monthly_data["month_year"],
    monthly_data["order_count"],
    marker='o',
    linewidth=2.5,
    color="#FF6F61"
)
# Mengatur tampilan axis x dan y
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)

# Menambahkan elemen visual pada plot
ax.set_title("Jumlah Pesanan per Bulan (September 2016 - September 2018)",
             fontsize=18, color="#444444", loc="center")
ax.set_xlabel("Bulan", fontsize=14, color="#444444")
ax.set_ylabel("Jumlah Pesanan", fontsize=14, color="#444444")

# Menambahkan grid untuk membantu pembacaan data
ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.7)

# Menambahkan anotasi pada puncak data
max_order = monthly_data["order_count"].max()
max_month = monthly_data.loc[monthly_data["order_count"].idxmax(
), "month_year"]
ax.annotate(
    f"Puncak: {max_order} pesanan",
    xy=(max_month, max_order),
    xytext=(max_month, max_order + 50),
    fontsize=12,
    color="#333333",
    arrowprops=dict(facecolor='gray', arrowstyle="->", lw=1)
)

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend")
col1, col2 = st.columns(2)

with col1:
    total_spend = format_currency(
        sum_spend_df["total_spend"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = format_currency(
        sum_spend_df["total_spend"].mean(), "IDR", locale="id_ID")
    st.markdown(f"Average Spend: **{avg_spend}**")

# Membuat figure dan plotting
fig, ax = plt.subplots(figsize=(20, 8))

# Plotting total pengeluaran pelanggan per bulan
ax.plot(
    # Menggunakan 'year_month' yang sudah diatur
    monthly_spend_data["order_approved_at"],
    monthly_spend_data["total_spend"],
    marker='o',
    linewidth=2,
    color="#D2691E"  # Ubah warna garis menjadi coklat tembaga
)

# Menambahkan elemen visual
ax.set_title(
    "Total Customer Spend per Month (September 2016 - September 2018)",
    loc="center", fontsize=20, color="#444444"
)  # Menambahkan warna pada judul
# Menambahkan label sumbu x
ax.set_xlabel("Month", fontsize=14, color="#000000")
ax.set_ylabel("Total Spend ($)", fontsize=14,
              color="#000000")  # Menambahkan label sumbu y
# Mengubah ukuran font dan warna sumbu x
ax.tick_params(axis="x", labelsize=12, rotation=45, colors="#000000")
# Mengubah ukuran font dan warna sumbu y
ax.tick_params(axis="y", labelsize=12, colors="#000000")

# Menambahkan grid
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Menampilkan grafik di aplikasi Streamlit
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_data["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_data["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")


# Membuat subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 18))

# Warna untuk produk dengan penjualan tertinggi dan terendah
colors_high = ["#1f77b4", "#aec7e8", "#aec7e8", "#aec7e8", "#aec7e8"]
colors_low = ["#ff7f0e", "#ffbb78", "#ffbb78", "#ffbb78", "#ffbb78"]

# Visualisasi produk dengan penjualan tertinggi
sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=sum_order_items_data.head(5),
    palette=colors_high,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk dengan Penjualan Tertinggi", loc="center", fontsize=45)
ax[0].tick_params(axis='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=40)

# Visualisasi produk dengan penjualan terendah
sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=sum_order_items_data.sort_values(
        by="product_count", ascending=True).head(5),
    palette=colors_low,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk dengan Penjualan Terendah", loc="center", fontsize=45)
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=40)

# Menambahkan judul keseluruhan
fig.suptitle(
    "Produk yang menjadi favorit pelanggan dan yang kurang diminati dalam penjualan", fontsize=50)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["Order Status", "Geolocation"])

with tab1:
    common_status_ = order_status.value_counts().index[0]
    st.markdown(f"Most Common Order Status: **{common_status_}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=order_status.index,
                y=order_status.values,
                order=order_status.index,
                palette=["#068DA9" if score ==
                         common_status else "#D3D3D3" for score in order_status.index]
                )

    plt.title("Order Status", fontsize=15)
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    url = 'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'
    brazil = mpimg.imread(urllib.request.urlopen(url), 'jpg')
    ax = data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(
        10, 10), alpha=0.3, s=0.3, c='blue')
    plt.axis('off')
    plt.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
    st.pyplot(plt)

    with st.expander("See Explanation"):
        st.write('Sesuai dengan grafik yang sudah dibuat, ada lebih banyak pelanggan di bagian tenggara dan selatan. Informasi lainnya, ada lebih banyak pelanggan di kota-kota yang merupakan ibu kota (São Paulo, Rio de Janeiro, Porto Alegre, dan lainnya).')

st.caption('Copyright(C) Yusfi Syawali 2024')
