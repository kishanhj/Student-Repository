""" Test class for HW09 """

import unittest
from Student_Repository_Kishan_Huliyar_Jagadeesh import Universities, University

class HW09Test(unittest.TestCase):
    """ Test class for HW09"""

    def test_stevens(self):
        "Test for stevens"
        univs : Universities = Universities.get_instance()
        univs.add_university("Stevens","C:\Stevens\Sem 3\SSW - 810\Assignments\HW09_kishan_Huliyar_jagadeesh\Stevens")
        stevens : University = univs.universities["Stevens"]
        self.assertEqual(stevens.students["10103"].name,"Baldwin, C")
        self.assertEqual(stevens.students["11788"].major,"SYEN")
        self.assertEqual(stevens.instructors["98765"].name,"Einstein, A")
        self.assertEqual(stevens.instructors["98760"].department,"SYEN")
        self.assertEqual(len(stevens.students["10115"].courses),4)
        self.assertEqual(sorted([key for key in stevens.students["10115"].courses]),['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])

    def test_NYU(self):
        "Test for nyu"
        univs : Universities = Universities.get_instance()
        univs.add_university("Stevens","C:\Stevens\Sem 3\SSW - 810\Assignments\HW09_kishan_Huliyar_jagadeesh\\nyu")
        nyu : University = univs.universities["Stevens"]
        self.assertEqual(nyu.students["10103"].name,"Baldwin, C")
        self.assertEqual(nyu.students["11788"].major,"SYEN")
        self.assertEqual(nyu.instructors["98765"].name,"Einstein, A")
        self.assertEqual(nyu.instructors["98760"].department,"SYEN")
        self.assertEqual(len(nyu.students["10115"].courses),4)
        self.assertEqual(sorted([key for key in nyu.students["10115"].courses]),['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])

if __name__ == "__main__":
    unittest.main(verbosity=2)