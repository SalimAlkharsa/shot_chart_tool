from Utils.gather_data import Query
from Utils.shot_chart import ShotChart

# Path: main.py
# Get the data from a query
print('Enter the query: ')
print('Query Format: ')
print('Player Name,Team Name,LastNGames,DateFrom,DateTo')
print('Fill a 0 if you do not want to specify a field // Date is in YYYYMMDD format')
print('Note currently date does not work')
print('Example: 0,Boston Celtics,0,0,0')
#query = input()
query = Query('0,Boston Celtics,0,0,0')
# query = Query(query)
df = query.data
print(df)

# Generate a shot chart
chart = ShotChart(df)
chart.make_shot_chart() # This will show the shot chart and it just throws a pic
