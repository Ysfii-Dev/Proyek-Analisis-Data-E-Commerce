class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_data(self):
        daily_orders_data = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_data = daily_orders_data.reset_index()
        daily_orders_data.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)

        return daily_orders_data

    def create_order_pattern_df(self):
        # Mengelompokkan data berdasarkan bulan dengan resampling
        monthly_data = self.df.resample(rule='M', on='order_approved_at').agg({
            "order_id": "nunique",
        })

        # Mengubah format indeks menjadi nama bulan dan tahun
        monthly_data.index = monthly_data.index.strftime('%Y-%B')
        monthly_data = monthly_data.reset_index()

        # Mengubah nama kolom agar lebih deskriptif
        monthly_data.rename(columns={
            "order_approved_at": "month_year",  # Kolom baru ini menggantikan "month"
            "order_id": "order_count",
        }, inplace=True)

        # Menampilkan data bulanan yang telah diatur
        monthly_data = monthly_data.sort_values(
            by="order_count", ascending=False).drop_duplicates(subset='month_year', keep='last')

        # Sort ulang berdasarkan tahun dan bulan dengan mapping
        month_mapping = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        # Menambahkan kolom numerik untuk sorting berdasarkan tahun dan bulan
        monthly_data["year_month_numeric"] = monthly_data["month_year"].apply(
            lambda x: int(x.split('-')[0]) * 100 +
            month_mapping[x.split('-')[1]]
        )

        # Mengurutkan berdasarkan kolom numerik gabungan tahun dan bulan
        monthly_data = monthly_data.sort_values(
            by="year_month_numeric").drop("year_month_numeric", axis=1)

        # Menampilkan data yang telah diatur
        return monthly_data

    def create_sum_spend_df(self):
        sum_spend_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "payment_value": "sum"
        })
        sum_spend_df = sum_spend_df.reset_index()
        sum_spend_df.rename(columns={
            "payment_value": "total_spend"
        }, inplace=True)

        return sum_spend_df

    def create_monthly_spend_df(self):
        import pandas as pd
        # Menghitung total pengeluaran per bulan
        monthly_spend_data = self.df.resample(rule='M', on='order_approved_at').agg({
            "payment_value": "sum"
        })

        # Mengubah format indeks menjadi nama bulan dan tahun
        monthly_spend_data.index = monthly_spend_data.index.strftime('%Y-%B')
        monthly_spend_data = monthly_spend_data.reset_index()

        # Mengubah nama kolom agar lebih deskriptif
        monthly_spend_data.rename(columns={
            "payment_value": "total_spend",
            "index": "order_approved_at"
        }, inplace=True)

        # Sorting berdasarkan total pengeluaran
        monthly_spend_data = monthly_spend_data.sort_values(
            by="total_spend", ascending=False)

        # Menyimpan data unik berdasarkan 'order_approved_at'
        monthly_spend_data = monthly_spend_data.drop_duplicates(
            'order_approved_at', keep='last')

        # Sort ulang berdasarkan tahun dan bulan dengan mapping
        month_mapping = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        # Fungsi untuk mendapatkan nomor bulan dan tahun secara bersamaan
        monthly_spend_data["year_month"] = monthly_spend_data["order_approved_at"].apply(
            # Menggabungkan tahun dan bulan numerik
            lambda x: f"{x.split('-')[0]}-{month_mapping[x.split('-')[1]]}"
        )

        # Mengubah kolom 'year_month' menjadi tipe data datetime untuk pengurutan
        monthly_spend_data["year_month"] = pd.to_datetime(
            monthly_spend_data["year_month"], format="%Y-%m")

        # Mengurutkan berdasarkan 'year_month'
        monthly_spend_data = monthly_spend_data.sort_values(by="year_month")

        return monthly_spend_data

    def create_sum_order_items_data(self):
        sum_order_items_data = self.df.groupby("product_category_name_english")[
            "product_id"].count().reset_index()
        sum_order_items_data.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_data = sum_order_items_data.sort_values(
            by='product_count', ascending=False)

        return sum_order_items_data

    def create_order_status(self):
        order_status_df = self.df["order_status"].value_counts(
        ).sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()

        return order_status_df, most_common_status
