import unittest
import numpy as np
from step_by_step_ks import raw_ks_test, bootstrap_pvalue

class TestRawKS(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.dist_norm_8 = np.random.normal(8,4, size=1000)
		self.dist_norm_8_bis = np.random.normal(8,4, size=1500)
		self.dist_no_overlap = np.random.normal(30,0.5,size=150)

	def test_no_diff_same_distribution(self):

		test = raw_ks_test(self.dist_norm_8, self.dist_norm_8, alternative='1 less than 2',plot=False)
		self.assertEqual(test['stat'],0.0)

		test = raw_ks_test(self.dist_norm_8, self.dist_norm_8, alternative='2 less than 1',plot=False)
		self.assertEqual(test['stat'],0.0)		

	def test_small_difference_similar_distribution(self):
		
		test = raw_ks_test(self.dist_norm_8, self.dist_norm_8_bis, alternative='1 less than 2',plot=False)
		self.assertLess(test['stat'], 0.05)
		
		test = raw_ks_test(self.dist_norm_8, self.dist_norm_8_bis, alternative='2 less than 1',plot=False)
		self.assertLess(test['stat'], 0.05)

	def test_no_overlap_statistic(self):

		test = raw_ks_test(self.dist_norm_8, self.dist_no_overlap, alternative='1 less than 2',plot=False)
		self.assertEqual(test['stat'], 1.0)

		test = raw_ks_test(self.dist_no_overlap,self.dist_norm_8, alternative='1 less than 2',plot=False)
		self.assertEqual(test['stat'], 0.0)

class TestBootstrap(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.dist_norm_8 = np.random.normal(8,4, size=100)
		self.dist_norm_8_bis = np.random.normal(8,4, size=300)
		self.dist_no_overlap = np.random.normal(30,0.5,size=150)
		
		self.test_same = raw_ks_test(self.dist_norm_8, self.dist_norm_8, alternative='1 less than 2', plot=False)
		self.reference_stat_same = self.test_same['stat']

		self.test_similar = raw_ks_test(self.dist_norm_8, self.dist_norm_8_bis, alternative='1 less than 2', plot=False)
		self.reference_stat_similar = self.test_similar['stat']

		self.test_different = raw_ks_test(self.dist_norm_8, self.dist_no_overlap, alternative='1 less than 2', plot=False)
		self.reference_stat_different = self.test_different['stat']

		self.test_different_flip = raw_ks_test(self.dist_norm_8, self.dist_no_overlap, alternative='1 greater than 2', plot=False)
		self.reference_stat_different_flip = self.test_different_flip['stat']

	def test_pvalue_same_is_one(self):
		
		pval = bootstrap_pvalue(self.dist_norm_8, self.dist_norm_8, reference_stat=self.reference_stat_same, alternative='1 less than 2', nloop=1000, plot=False)
		self.assertEqual(pval, 1.0)

	def test_pvalue_similar_is_non_significant(self):
		
		pval = bootstrap_pvalue(self.dist_norm_8, self.dist_norm_8_bis, reference_stat=self.reference_stat_similar, alternative='1 less than 2', nloop=1000, plot=False)
		self.assertGreater(pval, 0.05)

	def test_pvalue_zero_for_far_distributions(self):
		pval = bootstrap_pvalue(self.dist_norm_8, self.dist_no_overlap, reference_stat=self.reference_stat_different, alternative='1 less than 2', nloop=1000, plot=False)
		self.assertEqual(pval, 0.0)

	def test_pvalue_non_significant_different_flipped(self):

		pval = bootstrap_pvalue(self.dist_norm_8, self.dist_no_overlap, reference_stat=self.reference_stat_different_flip, alternative='1 greater than 2', nloop=1000, plot=False)
		self.assertEqual(pval, 1.0)		


if __name__=="__main__":
	unittest.main()