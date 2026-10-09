import unittest
from pathlib import Path
import pandas as pd
from src.analyze import load_and_validate,compute_summaries,distribution

class RatingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=load_and_validate()
    def test_expected_rows_and_rosters(self):
        self.assertEqual(len(self.df),137)
        self.assertEqual(self.df.groupby('brand').size().to_dict(),{'NXT':32,'Raw':56,'SmackDown':49})
    def test_source_duplicate_is_not_dropped(self):
        self.assertEqual(self.df.superstar.nunique(),136)
        self.assertEqual(self.df[self.df.superstar=='Jinder Mahal'].shape[0],2)
    def test_summary_totals(self):
        s=compute_summaries(self.df)
        self.assertEqual(int(s.entries.sum()),137)
        self.assertEqual(int(s.n_85_plus.sum()),27)
    def test_rating_bands_partition(self):
        self.assertEqual(int(distribution(self.df).to_numpy().sum()),137)
    def test_bad_rating_fails_validation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bad.csv'
            self.df.assign(overall_rating=101).to_csv(p,index=False)
            with self.assertRaises(AssertionError):load_and_validate(p)

if __name__=='__main__':unittest.main()
