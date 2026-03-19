import pandas as pd
import numpy as np

def process_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Data Cleaning
    # Convert dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')

    # Remove zero-sales or invalid profit records
    df = df[df['Sales'] > 0]
    df = df[df['Units'] > 0]
    
    # Standardize labels (just in case)
    df['Division'] = df['Division'].str.strip()
    df['Product Name'] = df['Product Name'].str.strip()

    # Profitability Metric Calculation
    df['Gross Margin (%)'] = (df['Gross Profit'] / df['Sales']) * 100
    df['Profit per Unit'] = df['Gross Profit'] / df['Units']
    
    total_sales = df['Sales'].sum()
    total_profit = df['Gross Profit'].sum()
    
    df['Revenue Contribution'] = (df['Sales'] / total_sales) * 100
    df['Profit Contribution'] = (df['Gross Profit'] / total_profit) * 100

    # Product and Factory Correlations
    factory_mapping = {
        'Wonka Bar - Nutty Crunch Surprise': 'Lot\'s O\' Nuts',
        'Wonka Bar - Fudge Mallows': 'Lot\'s O\' Nuts',
        'Wonka Bar -Scrumdiddlyumptious': 'Lot\'s O\' Nuts',
        'Wonka Bar - Milk Chocolate': 'Wicked Choccy\'s',
        'Wonka Bar - Triple Dazzle Caramel': 'Wicked Choccy\'s',
        'Laffy Taffy': 'Sugar Shack',
        'SweeTARTS': 'Sugar Shack',
        'Nerds': 'Sugar Shack',
        'Fun Dip': 'Sugar Shack',
        'Fizzy Lifting Drinks': 'Sugar Shack',
        'Everlasting Gobstopper': 'Secret Factory',
        'Hair Toffee': 'The Other Factory',
        'Lickable Wallpaper': 'Secret Factory',
        'Wonka Gum': 'Secret Factory',
        'Kazookles': 'The Other Factory'
    }
    
    factory_coords = {
        'Lot\'s O\' Nuts': (32.881893, -111.768036),
        'Wicked Choccy\'s': (32.076176, -81.088371),
        'Sugar Shack': (48.11914, -96.18115),
        'Secret Factory': (41.446333, -90.565487),
        'The Other Factory': (35.1175, -89.971107)
    }

    df['Factory'] = df['Product Name'].map(factory_mapping)
    df['Factory Latitude'] = df['Factory'].map(lambda x: factory_coords.get(x, (None, None))[0] if x else None)
    df['Factory Longitude'] = df['Factory'].map(lambda x: factory_coords.get(x, (None, None))[1] if x else None)

    return df

if __name__ == "__main__":
    raw_data_path = "Nassau Candy Distributor.csv"
    processed_df = process_data(raw_data_path)
    
    # Save processed data for the Streamlit app
    processed_df.to_csv("processed_nassau_candy.csv", index=False)
    print("Data processing complete. Saved to processed_nassau_candy.csv")

    # Quick Summary Statistics for verification
    print("\n--- Summary Statistics ---")
    print(f"Total Records: {len(processed_df)}")
    print(f"Total Sales: ${processed_df['Sales'].sum():.2f}")
    print(f"Total Profit: ${processed_df['Gross Profit'].sum():.2f}")
    print(f"Average Gross Margin: {processed_df['Gross Margin (%)'].mean():.2f}%")
