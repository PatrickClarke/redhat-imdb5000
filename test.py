import unittest
import pandas as pd

from imdb5kstats import profitability_setup, profitability


cols = ['budget', 'gross', 'actor-director_combo', 'genres']
vals = [
	['0.0', '100.0', 'john&sally', 'action']
	,['20.0', '100.0', 'john&sally', 'action|drama']
	,[None, '1000.0', 'john&sally', 'action']
	,['100.0', None, 'john&sally', 'action']
]
test_df = pd.DataFrame(data=vals, columns=cols)


class TestProfitabilitySetups(unittest.TestCase):

	def test_profitability_setup_nozeroes(self):
		bix = profitability_setup(test_df, include_zeroes=False)
		# filter out nulls and 0s
		self.assertEqual(test_df.loc[bix].shape[0], 1)

	def test_profitability_setup_zeroes(self):
		bix = profitability_setup(test_df, include_zeroes=True)
		# filter out nulls only
		self.assertEqual(test_df.loc[bix].shape[0], 2)

	def test_profitability_nozeroes(self):
		bix = profitability_setup(test_df, include_zeroes=False)
		tdf = test_df.loc[bix].reset_index(drop=True)
		val = profitability(tdf, 'action')
		print(val)
		self.assertEqual(val, 4)

	def test_profitability_zeroes(self):
		self.assertEqual(profitability(test_df, 'action'), 9)
		self.assertEqual(profitability(test_df, 'drama'), 4)

if __name__ == '__main__':
	unittest.main()