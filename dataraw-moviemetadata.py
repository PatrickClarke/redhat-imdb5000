import utils.dbaccess as db

import pandas as pd


database = "./imdb5k.db"
schema = 'dataraw'
table = 'moviemetadata'
data = '../movie_metadata.csv'

# working with sqlite -- in postgres it would be schema.table
tablename = '_'.join([schema, table])

data = pd.read_csv(data)

# clean
for col in data:
	data[col] = data[col].astype(str)
	data[col] = data[col].str.lower().str.strip()

renamer = {k: k.lower().strip() for k in data.columns}
data = data.rename(columns=renamer)

# generate create table sql
drop_sql = "DROP TABLE IF EXISTS {TABLENAME};".format(TABLENAME=tablename)
create_sql = """
CREATE TABLE {TABLENAME} (
	{COLS}
);
""".format(
	TABLENAME=tablename
	,COLS='TEXT\n  ,'.join(data.columns)
)

with open('./{tablename}.sql'.format(tablename=tablename), 'w') as f:
	f.write(drop_sql)
	f.write(create_sql)

# connect and create
conn = db.create_connection(database)
conn.execute(drop_sql)
conn.execute(create_sql)

data.to_sql(
	name=tablename
	,con=conn
	,if_exists='replace'
	,index=False
	,chunksize=50000
)
