import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# データの読み込み
file_path = "/Users/yuu/pythondata/sp500_analysis/data/raw/spy_data_with_3Y_MA_2018-01-01_2021-01-01.csv"
df = pd.read_csv(file_path, index_col=0, parse_dates=True)

# インデックスをDatetimeIndexに変換（必要な場合）
if not pd.api.types.is_datetime64_any_dtype(df.index):
    df.index = pd.to_datetime(df.index, utc=True)  # UTCに変換

# 移動平均線の計算
df['50_MA'] = df['Close'].rolling(window=50).mean()
df['200_MA'] = df['Close'].rolling(window=200).mean()
df['300_MA'] = df['Close'].rolling(window=300).mean()
df['400_MA'] = df['Close'].rolling(window=400).mean()
df['500_MA'] = df['Close'].rolling(window=500).mean()
df['600_MA'] = df['Close'].rolling(window=600).mean()
df['700_MA'] = df['Close'].rolling(window=700).mean()

# ボルプセクションの内容を定義する関数
def show_help():
    help_content = """
    ### Help Section

    **Question: How does the moving average help in understanding price trends?**

    **Answer:** It supports investment decisions by providing the direction of the trend, levels of support and resistance, and trading signals. This allows investors to make more informed decisions.

    ---

    **Question: 移動平均線はどのように価格のトレンドを把握する助けとなりますか？**

    **Answer:** トレンドの方向性、サポート・レジスタンスのレベル、売買シグナルを提供することで、投資判断をサポートします。これにより、投資家はより情報に基づいた意思決定を行うことができます。
    """
    st.sidebar.markdown(help_content)

# アプリケーションの使い方を定義する関数
def show_usage():
    usage_content = """
    ### How to Use the Application:

    1. Select the year and month to filter the data.
    2. View the daily closing prices along with moving averages and Bollinger Bands.
    3. Use the graphs to analyze trends and make investment decisions.

    ---

    ### アプリケーションの使い方:

    1. データをフィルタリングするために年と月を選択します。
    2. 日ごとの終値と移動平均、ボリンジャーバンドを表示します。
    3. グラフを使用してトレンドを分析し、投資判断を行います。
    """
    st.sidebar.markdown(usage_content)

# サイドバーにヘルプボタンを追加
if st.sidebar.button("Show Help"):
    show_help()

# サイドバーに使い方ボタンを追加
if st.sidebar.button("How to Use"):
    show_usage()

# メインのアプリケーションの内容
st.title("S&P 500 Analysis")
# ... ここに他のアプリの内容を追加 ...

# ボリンジャーバンドの計算
window = 20
df['Middle_Band'] = df['Close'].rolling(window=window).mean()
df['Upper_Band'] = df['Middle_Band'] + (df['Close'].rolling(window=window).std() * 2)
df['Lower_Band'] = df['Middle_Band'] - (df['Close'].rolling(window=window).std() * 2)

# 言語選択
language = st.selectbox("Select Language / 言語を選択してください:", ["English", "日本語"])

# 表示するテキストを言語に応じて設定
if language == "English":
    year_label = "Select the year to display (or select 'All' for all years)"
    month_label = "Select the month to display (or select 'All' for the entire year)"
    daily_data_label = "### Daily Data"
    close_price_label = "Close Price"
    moving_average_50_label = "50-Day Moving Average"
    moving_average_200_label = "200-Day Moving Average"
    moving_average_300_label = "300-Day Moving Average"
    moving_average_400_label = "400-Day Moving Average"
    moving_average_500_label = "500-Day Moving Average"
    moving_average_600_label = "600-Day Moving Average"
    moving_average_700_label = "700-Day Moving Average"
    date_label = "Date"
    price_label = "Price"
else:  # 日本語
    year_label = "表示したい年を選択してください (全ての年を表示するには 'All' を選択)"
    month_label = "表示したい月を選択してください (全てのデータを表示するには 'All' を選択)"
    daily_data_label = "### 日ごとのデータ"
    close_price_label = "Close Price"
    moving_average_50_label = "50-Day Moving Average"
    moving_average_200_label = "200-Day Moving Average"
    moving_average_300_label = "300-Day Moving Average"
    moving_average_400_label = "400-Day Moving Average"
    moving_average_500_label = "500-Day Moving Average"
    moving_average_600_label = "600-Day Moving Average"
    moving_average_700_label = "700-Day Moving Average"
    date_label = "Date"
    price_label = "Price"

# ユーザーに年を選択させる（オプション）
unique_years = df.index.year.unique()
year_to_plot = st.selectbox(year_label, list(unique_years) + ['All'])

# 選択した年のデータをフィルタリング
if year_to_plot == 'All':
    df_year = df  # 全データを表示
else:
    df_year = df[df.index.year == year_to_plot]  # 選択した年のデータを表示

# ユーザーに月を選択させる（オプション）
unique_months = df_year.index.month.unique()
month_to_plot = st.selectbox(month_label, list(unique_months) + ['All'])

# 選択した年と月のデータをフィルタリング
if month_to_plot == 'All':
    df_display = df_year  # 全データを表示
else:
    df_display = df_year[df_year.index.month == month_to_plot]  # 選択した月のデータを表示

# 日ごとのデータを表示
st.write(daily_data_label)
st.write(df_display[['Close', '50_MA', '200_MA', '300_MA', '400_MA', '500_MA', '600_MA', '700_MA']])  # 終値と移動平均を表示

# グラフの作成
plt.figure(figsize=(14, 12))

# 1つ目のグラフ（ラインチャート）
plt.subplot(2, 1, 1)  # 2行1列の1つ目
plt.plot(df_display['Close'], label=close_price_label, color='blue', alpha=0.5)
plt.plot(df_display['50_MA'], label=moving_average_50_label, color='orange', linewidth=2)
plt.plot(df_display['200_MA'], label=moving_average_200_label, color='green', linewidth=2)
plt.plot(df_display['300_MA'], label=moving_average_300_label, color='red', linewidth=2)
plt.plot(df_display['400_MA'], label=moving_average_400_label, color='purple', linewidth=2)
plt.plot(df_display['500_MA'], label=moving_average_500_label, color='brown', linewidth=2)
plt.plot(df_display['600_MA'], label=moving_average_600_label, color='pink', linewidth=2)
plt.plot(df_display['700_MA'], label=moving_average_700_label, color='cyan', linewidth=2)
plt.title(f'S&P 500 Close Price' + (f' for {year_to_plot}' if year_to_plot != 'All' else ''), fontsize=16)
plt.xlabel(date_label, fontsize=14)
plt.ylabel(price_label, fontsize=14)
plt.legend()
plt.grid()

# 2つ目のグラフ（棒グラフ）
plt.subplot(2, 1, 2)  # 2行1列の2つ目
plt.bar(df_display.index, df_display['Close'], label=close_price_label, color='lightblue', alpha=0.5)
plt.title(f'S&P 500 Close Price Bar Chart' + (f' for {year_to_plot}' if year_to_plot != 'All' else ''), fontsize=16)
plt.xlabel(date_label, fontsize=14)
plt.ylabel(price_label, fontsize=14)
plt.legend()
plt.grid()

# グラフを表示
st.pyplot(plt)
