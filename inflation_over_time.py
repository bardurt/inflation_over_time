import pandas as pd
import matplotlib.pyplot as plt
import sys

def inflation(overTime, startYear, endYear):
    TARGET = 2
    THRESHOLD = 0.1
    TARGET_END = TARGET + THRESHOLD
    COLUMN_NAME = "PCEPILFE_PC1"
    
    # Read CSV file and reverse the table
    table = pd.read_csv("PCEPILFE.csv")
    table = table[::-1]
    
    # Filter the table based on year range
    table['Year'] = pd.to_datetime(table['DATE']).dt.year
    filtered_table = table[(table['Year'] > startYear) & (table['Year'] < endYear)]
    
    # Initialize variables
    inflationOverTime = []
    xAxis = []
    firstIndex = filtered_table.index[0]
    
    # Compute inflation over time
    for index, row in filtered_table.iterrows():
        date = row['DATE']
        rowValue = row[COLUMN_NAME]
        
        # Calculate average inflation if overTime is True
        if overTime:
            avg = filtered_table.loc[firstIndex:index, COLUMN_NAME].mean()
            inflationOverTime.append(avg)
            xAxis.append(index - firstIndex + 1)
        else:
            inflationOverTime.append(rowValue)
            xAxis.append(date)
    
    tableName = f"Inflation, PCE (Ex. Food and Energy) [{startYear}; {endYear-1}]"
    xLabel = "Date"
    
    if overTime:
        tableName = f"Inflation Over Time, PCE (Ex. Food and Energy) [{startYear}; {endYear-1}] Between: {TARGET} and {TARGET_END} %"
        xLabel = "Months back"
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    if overTime:
        colors = ['green' if val >= TARGET and val <= TARGET_END else 'red' for val in inflationOverTime]
        plt.bar(xAxis, inflationOverTime, color=colors)
    else:
        colors = ['red' if val >= TARGET else 'red' for val in inflationOverTime]
        plt.bar(xAxis, inflationOverTime, color=colors)
    
    plt.axhline(TARGET, color='blue', linestyle='--', linewidth=1)

    if overTime:
        plt.axhline(TARGET_END, color='blue', linestyle='--', linewidth=1)
    
    plt.title(tableName)
    plt.xlabel(xLabel)
    plt.ylabel("%")
    plt.ylim(-0.5, 6)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Expected 3 arguments (BOOLEAN, startYear, endYear)")
        sys.exit(1)
    
    arg1 = sys.argv[1].upper()
    if arg1 not in ["TRUE", "FALSE"]:
        print("Error: First argument must be TRUE or FALSE")
        sys.exit(1)
    
    try:
        startYear = int(sys.argv[2])
        endYear = int(sys.argv[3])
    except ValueError:
        print("Error: Second and third arguments must be numbers")
        sys.exit(1)
    
    overTime = arg1 == "TRUE"
    inflation(overTime, startYear, endYear)
