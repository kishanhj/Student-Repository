""" Test class for HW09 """

import sqlite3
import unittest
from Student_Repository_Kishan_Huliyar_Jagadeesh import Universities, University

class HW09Test(unittest.TestCase):
    """ Test class for HW09"""

    def test_stevens(self):
        "Test for stevens"
        univs : Universities = Universities.get_instance()
        univs.add_university("Stevens","C:\Stevens\Sem 3\SSW - 810\Assignments\git\Student-Repository\Stevens")
        stevens : University = univs.universities["Stevens"]

        self.assertEqual(stevens.students["10103"].name,"Jobs, S")
        self.assertEqual(stevens.students["11714"].major.name,"CS")
        self.assertEqual(stevens.students["10183"].gpa,4.0)
        self.assertEqual(stevens.students["10103"].get_remaining_req_courses(),['SSW 540', 'SSW 555'])
        self.assertEqual(stevens.students["10115"].get_remaining_ele_courses(),['CS 501', 'CS 546'])
        self.assertEqual(stevens.students["10115"].get_completed_courses(),['SSW 810'])

        self.assertEqual(stevens.instructors["98764"].name,"Cohen, R")
        self.assertEqual(stevens.instructors["98762"].department,"CS")

        self.assertEqual(len(stevens.students["10115"].courses),2)
        self.assertEqual(sorted([key for key in stevens.students["11714"].courses]),['CS 546', 'CS 570', 'SSW 810'])

        db_con = sqlite3.connect('C:\Stevens\Sem 3\SSW - 810\Assignments\git\Student-Repository\HW11_startup.db')
        q : str = """ select instructors.CWID,instructors.Name,instructors.Dept,grades.Course,count(grades.Course) from HW11_Instructors instructors join HW11_Grades grades on CWID = Instructor_CWID group by Grade;"""
        instructors_db = [row for row in db_con.execute(q)]
        expected_instructors_db = [('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),( '98763', 'Rowland, J', 'SFEN', 'SSW 810', 2),( '98762', 'Hawking, S', 'CS', 'CS 501', 1),( '98763', 'Rowland, J', 'SFEN', 'SSW 810', 1),( '98762', 'Hawking, S', 'CS', 'CS 546', 1)]
        self.assertEqual(instructors_db, expected_instructors_db)
        

if __name__ == "__main__":
    unittest.main(verbosity=0)