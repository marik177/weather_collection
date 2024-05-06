# Weather Data Collection and Export Script

This script automatically fetches weather data in the Skolkovo area at regular intervals (e.g., every 3 minutes) and adds it to a database. The collected weather data includes:

- Temperature (in Celsius)
- Wind direction and speed (in m/s, with directional indicators such as NE, NW, N, etc.)
- Air pressure (in mmHg)
- Precipitation type and amount (in mm)

## Installation
Clone the repository:
```bash
git clone https://github.com/marik177/weather_collection.git
``` 
Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
Data Collection

To start fetching weather data and storing it in the database, run the script without any arguments:

```bash
python src/main.py
```
Export to Excel

To export the weather data from the database to an Excel file, 
use the following command in new terminal:

```bash
python src/main.py --make_report
```
