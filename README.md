# redhat-imdb5000
## Requirements/notes:
* windows (short notice, sorry)
* since the db already exists in repo, we will skip the db creation process - this would occur after 5.i: `python create_db.py`
* since the table, `dataraw_moviemetadata` already exists in the db, we will skip the table creation process - this would occur after the above: `python dataraw-moviemetadata.py`
## Steps
1. download and install python3: https://www.python.org/downloads/release/python-374/
2. download and install git: https://git-scm.com/download/win
3. open git bash and navigate to a directory of your choice. Clone this repo into that directory. close git bash
4. download and unzip the dataset into a folder of your choice. I chose the parent directory of this repo: https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data
5. open powershell, navigate to this directory, and run the following commands:
	1. `.\imdb5k\Scripts\activate` - activates environment
	2. `python tests.py`

## References/Resources
* py3 standard lib
* pandas
* sqlite
* https://www.sqlitetutorial.net/sqlite-python/creating-database/
* https://www.python.org/downloads/release/python-374/
* https://git-scm.com/download/win
* https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data
