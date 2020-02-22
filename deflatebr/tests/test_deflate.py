from unittest import TestCase
import deflatebr as dbr
import numpy as np
from datetime import datetime

class TestDeflate(TestCase):

    def test_clean_date(self):
        self.assertEqual(
            dbr.utils.clean_real_date('2020-01'), '2020-01-01'
        )

    def test_month_type(self):
        self.assertIsInstance(
            dbr.utils.round_date_to_month(datetime(2020,1,28)), 
            str
        )
    
    def test_previous_month(self):
        self.assertEqual(
            dbr.utils.round_date_to_month(datetime(2020,1,28)),
            '2019-12-01'
        )

    def test_deflate_array(self):
        self.assertIsInstance(
            dbr.deflate(100, '2018-01-15', '2018-08'),
            np.ndarray
        )

    def test_deflate_str(self):
        self.assertAlmostEqual(
            dbr.deflate(100, '2018-01-15', '2018-08')[0],
            102.84961131
        )

    def test_deflate_date(self):
        self.assertAlmostEqual(
            dbr.deflate(100, datetime(2018, 1, 28), '2018-08')[0],
            102.84961131
        )

    def test_deflate_list_date(self):
        self.assertAlmostEqual(
            dbr.deflate([100,110], [datetime(2018, 1, 28), datetime(2018, 2, 28)], '2018-08')[1],
            112.80737904
        )

    def test_deflate_list_str(self):
        self.assertAlmostEqual(
            dbr.deflate([100,110], ['2018-01-28', '2018-02-15'], '2018-08')[1],
            112.80737904
        )
    
    def test_deflate_error_message(self):
        with self.assertRaises(Exception) as context:
            dbr.deflate([100,110], ['2018-01-28', '2018-02-15'], '2018-08', index='indc')
        self.assertTrue("index must be one of 'ipca', 'igpm', 'igpdi', 'ipc', 'inpc'" in str(context.exception))

    def test_deflate_igpm(self):
        self.assertAlmostEqual(
            dbr.deflate(100, '2018-01-15', '2018-08', index='igpm')[0],
            106.66069780910499
        )
    
    def test_deflate_igpdi(self):
        self.assertAlmostEqual(
            dbr.deflate(100, '2018-01-15', '2018-08', index='igpdi')[0],
            106.63376401612987
        )
    
    def test_deflate_ipc(self):
        self.assertAlmostEqual(
            dbr.deflate(100, '2018-01-15', '2018-08', index='ipc')[0],
            103.24647272393032
        )

    def test_deflate_inpc(self):
        self.assertAlmostEqual(
            dbr.deflate(100, '2018-01-15', '2018-08', index='inpc')[0],
            102.82693360196076
        )
    