import pandas as pd
import sqlite3

def process_binding_constraints_daily(conn):
    """Process BINDING_CONSTRAINTS_DAILY table"""
    print("Processing BINDING_CONSTRAINTS_DAILY...")
    df = pd.read_sql_query('SELECT * FROM BINDING_CONSTRAINTS_HOURLY', conn, parse_dates=['Interval', 'Date'])
    df['Interval'] = df['Interval'] - pd.Timedelta(minutes=15)
    df['Interval'] = df['Interval'].dt.strftime('%Y-%m-%d')
    df = df.groupby(['Interval', 'Constraint Name']).sum()['Shadow Price'].to_frame()
    df.reset_index(inplace=True)
    
    # Save to SQL
    df.to_sql(
        name='BINDING_CONSTRAINTS_DAILY',
        con=conn,
        if_exists='replace',
        index=False
    )
    
    # Save to CSV
    df.to_csv('data/BINDING_CONSTRAINTS_DAILY.csv', index=False)
    print("BINDING_CONSTRAINTS_DAILY processing completed")

def process_nodes_congestion_daily(conn):
    """Process NODES_CONGESTION_DAILY table"""
    print("Processing NODES_CONGESTION_DAILY...")
    query = '''
    SELECT Date, Node, 
           COALESCE(HE01, 0) + COALESCE(HE02, 0) + COALESCE(HE03, 0) + 
           COALESCE(HE04, 0) + COALESCE(HE05, 0) + COALESCE(HE06, 0) + 
           COALESCE(HE07, 0) + COALESCE(HE08, 0) + COALESCE(HE09, 0) + 
           COALESCE(HE10, 0) + COALESCE(HE11, 0) + COALESCE(HE12, 0) + 
           COALESCE(HE13, 0) + COALESCE(HE14, 0) + COALESCE(HE15, 0) + 
           COALESCE(HE16, 0) + COALESCE(HE17, 0) + COALESCE(HE18, 0) + 
           COALESCE(HE19, 0) + COALESCE(HE20, 0) + COALESCE(HE21, 0) + 
           COALESCE(HE22, 0) + COALESCE(HE23, 0) + COALESCE(HE24, 0) AS Congestion 
    FROM NODES_CONGESTION_HOURLY
    '''
    df = pd.read_sql_query(query, conn, parse_dates=['Interval', 'Date'])
    df = df.groupby(['Date', 'Node']).sum()
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Save to SQL
    df.to_sql(
        name='NODES_CONGESTION_DAILY',
        con=conn,
        if_exists='replace',
        index=False
    )
    
    # Save to CSV
    df.to_csv('data/NODES_CONGESTION_DAILY.csv', index=False)
    print("NODES_CONGESTION_DAILY processing completed")

def process_binding_constraints_monthly(conn):
    """Process BINDING_CONSTRAINTS_MONTHLY table"""
    print("Processing BINDING_CONSTRAINTS_MONTHLY...")
    df = pd.read_sql_query('SELECT * FROM BINDING_CONSTRAINTS_DAILY', conn)
    df['Interval'] = pd.to_datetime(df['Interval'])
    df['Interval'] = df['Interval'].dt.strftime('%Y-%m')
    df = df.groupby(['Interval', 'Constraint Name']).sum()
    df.reset_index(inplace=True)
    df['Interval'] = pd.to_datetime(df['Interval'])
    df['Interval'] = df['Interval'].dt.strftime('%Y-%m-01')
    df['Interval'] = pd.to_datetime(df['Interval'])
    
    # Save to SQL
    df.to_sql(
        name='BINDING_CONSTRAINTS_MONTHLY',
        con=conn,
        if_exists='replace',
        index=False
    )
    
    # Save to CSV
    df.to_csv('data/BINDING_CONSTRAINTS_MONTHLY.csv', index=False)
    print("BINDING_CONSTRAINTS_MONTHLY processing completed")

def process_nodes_congestion_monthly(conn):
    """Process NODES_CONGESTION_MONTHLY table"""
    print("Processing NODES_CONGESTION_MONTHLY...")
    df = pd.read_sql_query('SELECT * FROM NODES_CONGESTION_DAILY', conn)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%m')
    df = df.groupby(['Date', 'Node']).sum()
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%m-01')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Save to SQL
    df.to_sql(
        name='NODES_CONGESTION_MONTHLY',
        con=conn,
        if_exists='replace',
        index=False
    )
    
    # Save to CSV
    df.to_csv('data/NODES_CONGESTION_MONTHLY.csv', index=False)
    print("NODES_CONGESTION_MONTHLY processing completed")

def main():
    """Main function to process all data"""
    print("Starting data processing...")
    
    # Connect to database
    conn = sqlite3.connect('data/database.db')
    
    try:
        # Process all tables
        process_binding_constraints_daily(conn)
        process_nodes_congestion_daily(conn)
        process_binding_constraints_monthly(conn)
        process_nodes_congestion_monthly(conn)
        
        print("All data processing completed successfully")
    except Exception as e:
        print(f"Error during processing: {str(e)}")
    finally:
        # Close connection
        conn.close()

if __name__ == "__main__":
    main()
