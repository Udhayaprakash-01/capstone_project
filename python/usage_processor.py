import pandas as pd
import glob


class UsageProcessor:
    def __init__(self):
        self.df = None

    def load_data(self, path):
        """Load only telecom CSV files"""
        try:
            import os
        # ✅ Get all CSV files
            all_files = glob.glob(os.path.join(path, "*.csv"))
            # ✅ Filter only telecom files
            files = [f for f in all_files if "sms-call-internet" in os.path.basename(f)]
            print("Files selected:", files[:3])
            if len(files) == 0:
                raise Exception("No telecom files found!")

        # ✅ Load first 3 files
            df_list = [pd.read_csv(f) for f in files[:3]]
            self.df = pd.concat(df_list, ignore_index=True)
            print("Data loaded successfully")

        except Exception as e:
            print("Error loading data:", e)

    def clean_data(self):
        """Clean dataset"""
        try:
           # ✅ Rename columns
            self.df = self.df.rename(columns={
                'datetime': 'timestamp',
                'CellID': 'grid_id',
               'internet': 'internet_usage'
           })

          # ✅ Create required columns
            self.df['call_count'] = self.df['callin'] + self.df['callout']
            self.df['sms_count'] = self.df['smsin'] + self.df['smsout']

         # ✅ Convert timestamp
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

        # Remove null timestamps
            self.df = self.df.dropna(subset=['timestamp'])

        # ✅ Extract features
            self.df['hour'] = self.df['timestamp'].dt.hour
            self.df['day'] = self.df['timestamp'].dt.date

        # ✅ Convert numeric columns
            cols = ['call_count', 'sms_count', 'internet_usage']
            for col in cols:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # ✅ Remove invalid values
            self.df = self.df[
                (self.df['call_count'] >= 0) &
                (self.df['sms_count'] >= 0) &
                (self.df['internet_usage'] >= 0)
            ]

        # Drop null rows
            self.df = self.df.dropna()

        # Remove duplicates
            self.df = self.df.drop_duplicates()

            print("Data cleaned successfully")

        except Exception as e:
            print("Error cleaning data:", e)


    def compute_daily_usage(self):
        """Total usage per day"""
        return self.df.groupby('day')[
            ['call_count', 'sms_count', 'internet_usage']
        ].sum()

    def compute_kpis(self):
        """Compute KPIs"""
        kpis = {}

        # Total usage per region
        kpis['region_usage'] = self.df.groupby('grid_id')[
            ['call_count', 'sms_count', 'internet_usage']
        ].sum()

        # Average usage per hour
        kpis['hourly_avg'] = self.df.groupby('hour')[
            ['call_count', 'sms_count', 'internet_usage']
        ].mean()

        # Peak usage hour
        total_by_hour = self.df.groupby('hour')['internet_usage'].sum()
        kpis['peak_hour'] = total_by_hour.idxmax()

        return kpis


# ✅ Task 1.3 — API Stub Function
def call_plan_api(customer_id):
    """Mock API response"""
    return {
        "customer_id": customer_id,
        "plan_name": "Premium Plan",
        "data_limit_gb": 50,
        "sms_limit": 1000,
        "call_minutes": "Unlimited"
    }