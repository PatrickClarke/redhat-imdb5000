import pandas as pd
import utils.dbaccess as db


def profitability_setup(df, include_zeroes=True):
	# only those rows whose gross and budget values are not null
	pbix = df[['gross', 'budget']].notnull().all(axis=1)
	if not include_zeroes:
		pbix = pbix & (~(df['budget'].astype(float) == 0.0))
	return pbix


def profitability(df, genre):
	bix = profitability_setup(df) & df['genres'].str.contains(genre)
	# slice dataframe
	sli = df.loc[bix].reset_index(drop=True)
	# total budget, gross
	budget = sli['budget'].astype(float).sum()
	gross = sli['gross'].astype(float).sum()
	return (gross - budget) / budget


tablename = 'dataraw_moviemetadata'
database = 'imdb5k.db'

conn = db.create_connection(database)

sql = "select * from {tablename}".format(tablename=tablename)
data = pd.read_sql(sql, conn)

genres = set('|'.join(data['genres'].unique()).split('|'))

res = dict()

# genre profitability
for k in genres:
	# genre weighted profitability (to avoid higher/lower grossing/budgeted
	# movies from skewing the results)
	res[k] = profitability(data, k)

# sort by weighted profitability
res = list(reversed(sorted([(res[k], k) for k in res])))

# print results. We can write this using open(...)
# see dataraw-moviemetadata.py for an example
print("calculated using genre totals: (gross - budget) / budget\n")
for result in res[:10]:
	print(result[1], '\n==========\n ', result[0], '\n')

# best actor, director pair
# In the interest of time, I skipped writing functions here
# this is basically the weighted profitability of an actor/director pair
# Arguably we could go by likes, but this is quick and dirty.
acols = [k for k in data.columns if 'actor' in k and 'name' in k]
bix = profitability_setup(data, include_zeroes=False)
lst = list()
print(data.loc[data['budget'].astype(float) == 0].shape)
for k in acols:
	cols = ['director_name', k]
	tdf = data.loc[bix].reset_index(drop=True)
	cname = 'director_{}'.format(k.replace('_name', ''))
	tdf[cname] = tdf[cols].apply(lambda x: '&'.join(x.values), axis=1)
	renamer = {cname: 'actor-director_combo'}
	tdf = tdf[[cname, 'budget', 'gross']].rename(columns=renamer)
	tdf['budget'] = tdf['budget'].astype(float)
	tdf['gross'] = tdf['gross'].astype(float)
	lst.append(tdf.reset_index(drop=True))

tdf = pd.concat(lst)
gbs = tdf.groupby('actor-director_combo').sum()
# remove total 0s
bix = gbs['budget'] != 0
gbs = gbs.loc[bix]
result = (gbs['gross'] - gbs['budget']) / gbs['budget']
print(result.sort_values(ascending=False).head(10))
