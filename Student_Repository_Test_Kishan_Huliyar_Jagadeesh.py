""" Test class for HW09 """

import unittest
from Student_Repository_Kishan_Huliyar_Jagadeesh import Universities, University

class HW09Test(unittest.TestCase):
    """ Test class for HW09"""

    def test_stevens(self):
        "Test for stevens"
        univs : Universities = Universities.get_instance()
        univs.add_university("Stevens","C:\Stevens\Sem 3\SSW - 810\Assignments\git\Student-Repository\Stevens")
        stevens : University = univs.universities["Stevens"]

        self.assertEqual(stevens.students["10103"].name,"Baldwin, C")
        self.assertEqual(stevens.students["11788"].major.name,"SYEN")
        self.assertEqual(stevens.students["11461"].gpa,3.9166666666666665)
        self.assertEqual(stevens.students["10172"].get_remaining_req_courses(),['SSW 540', 'SSW 564'])
        self.assertEqual(stevens.students["11658"].get_remaining_ele_courses(),['SSW 540', 'SSW 565', 'SSW 810'])
        self.assertEqual(stevens.students["10115"].get_completed_courses(),['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])

        self.assertEqual(stevens.instructors["98765"].name,"Einstein, A")
        self.assertEqual(stevens.instructors["98760"].department,"SYEN")

        self.assertEqual(len(stevens.students["10115"].courses),4)
        self.assertEqual(sorted([key for key in stevens.students["10115"].courses]),['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])

if __name__ == "__main__":
    unittest.main(verbosity=0)