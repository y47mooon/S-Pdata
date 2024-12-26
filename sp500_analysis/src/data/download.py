import yfinance as yf
import pandas as pd
from pathlib import Path
import logging
import matplotlib.pyplot as plt

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SPYDataDownloader:
    def __init__(self):
        self.data_dir = Path(__file__).parents[2] / 'data' / 'raw'
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_spy_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        S&P500のデータをダウンロードする
        
        Args:
            start_date (str): 開始日 (YYYY-MM-DD)
            end_date (str): 終了日 (YYYY-MM-DD)
            
        Returns:
            pd.DataFrame: ダウンロードしたデータ
        """
        try:
            logger.info(f"データのダウンロードを開始: {start_date}から{end_date}まで")
            
            spy = yf.Ticker("SPY")
            df = spy.history(
                start=start_date,
                end=end_date,
                interval="1d"
            )
            
            # データを保存
            output_file = self.data_dir / f"spy_data_{start_date}_{end_date}.csv"
            df.to_csv(output_file)
            logger.info(f"データを保存しました: {output_file}")
            
            # データの読み込み
            file_path = self.data_dir / f"spy_data_{start_date}_{end_date}.csv"
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)

            # 3年間の移動平均を計算
            df['3Y_MA'] = df['Close'].rolling(window=756).mean()

            # 結果の表示
            print(df[['Close', '3Y_MA']].tail())  # 最後の数行を表示

            # 結果を新しいCSVファイルとして保存（オプション）
            output_file_path = self.data_dir / f"spy_data_with_3Y_MA_{start_date}_{end_date}.csv"
            df.to_csv(output_file_path)
            
            return df
            
        except Exception as e:
            logger.error(f"データのダウンロード中にエラーが発生しました: {str(e)}")
            raise

if __name__ == "__main__":
    downloader = SPYDataDownloader()
    df = downloader.download_spy_data("2018-01-01", "2021-01-01")
    print("\nデータの行数:", len(df))
    print("取得された期間:", df.index[0].strftime('%Y-%m-%d'), "から", df.index[-1].strftime('%Y-%m-%d'))

    # データの読み込み
    file_path = "/Users/yuu/pythondata/sp500_analysis/data/raw/spy_data_with_3Y_MA_2018-01-01_2021-01-01.csv"
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # 移動平均線の計算
    df['50_MA'] = df['Close'].rolling(window=50).mean()
    df['200_MA'] = df['Close'].rolling(window=200).mean()

    # ボリンジャーバンドの計算
    window = 20
    df['Middle_Band'] = df['Close'].rolling(window=window).mean()
    df['Upper_Band'] = df['Middle_Band'] + (df['Close'].rolling(window=window).std() * 2)
    df['Lower_Band'] = df['Middle_Band'] - (df['Close'].rolling(window=window).std() * 2)

    # グラフの作成
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close Price', color='blue', alpha=0.5)
    plt.plot(df['50_MA'], label='50-Day Moving Average', color='orange', linewidth=2)
    plt.plot(df['200_MA'], label='200-Day Moving Average', color='green', linewidth=2)
    plt.plot(df['Middle_Band'], label='Middle Band (20-Day MA)', color='orange', linewidth=2)
    plt.plot(df['Upper_Band'], label='Upper Band', color='green', linestyle='--')
    plt.plot(df['Lower_Band'], label='Lower Band', color='red', linestyle='--')
    plt.fill_between(df.index, df['Upper_Band'], df['Lower_Band'], color='lightgray', alpha=0.5)

    # グラフの装飾
    plt.title('S&P 500 Close Price with Moving Averages and Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()
