import pandas as pd
import utils.dbaccess as db


tablename = 'dataraw_moviemetadata'
database = 'imdb5k.db'

conn = db.create_connection(database)

sql = "select * from {tablename}".format(tablename=tablename)
data = pd.read_sql(sql, conn)

genres = set('|'.join(data['genres'].unique()).split('|'))

res = dict()

# genre profitability
for k in genres:
	# only those rows whose gross and budget values are not null
	bix = data['gross'].notnull() & data['budget'].notnull()
	# only those rows whose genres contain the given genre
	bix = bix & data['genres'].str.contains(k)
	# filtered data
	tdf = data.loc[bix].reset_index(drop=True)
	# total budget
	budget = tdf['budget'].astype(float).sum()
	# total gross
	gross = tdf['gross'].astype(float).sum()
	# genre weighted profitability (to avoid higher/lower grossing/budgeted
	# movies from skewing the results)
	res[k] = (gross - budget) / budget

# sort by weighted profitability
res = list(reversed(sorted([(res[k], k) for k in res])))

# print results. We can write this using open(...)
# see dataraw-moviemetadata.py for an example
print("calculated using genre totals: (gross - budget) / budget\n")
for result in res[:10]:
	print(result[1], '\n==========\n ', result[0], '\n')

# best actor, director pair
acols = [k for k in data.columns if 'actor' in k and 'name' in k]
lst = list()
for k in acols:
	cols = ['director_name', k]
	bix = data[cols].notnull().all(axis=1)
	bix = bix & data['budget'].astype(float) != 0.
	tdf = data.loc[bix].reset_index(drop=True)
	cname = 'director_{}'.format(k.replace('_name', ''))
	tdf[cname] = tdf[cols].apply(lambda x: '&'.join(x.values), axis=1)
	tdf = tdf[[cname, 'budget', 'gross']].rename(columns={cname: 'adc'})
	tdf['budget'] = tdf['budget'].astype(float)
	tdf['gross'] = tdf['gross'].astype(float)
	lst.append(tdf)

tdf = pd.concat(lst)
gbs = tdf.groupby('adc').sum()
profitability = (gbs['gross'] - gbs['budget']) / gbs['budget']
print(profitability.sort_values(ascending=False).head())
