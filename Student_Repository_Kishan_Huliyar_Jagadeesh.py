""" Main class for HW09 """

from collections import defaultdict, OrderedDict
from os import error, name
from typing import Dict, Iterator, List, Tuple
from prettytable import PrettyTable
import os

class Student:
    """ Class representing a student in University """

    def __init__(self, cwid : str, name : str, major : "Major",university : "University") -> None:
        """ Constructor """
        self.cwid : str = cwid
        self.name : str = name
        self.major : "Major" = major
        self.courses : OrderedDict = OrderedDict()
        self.university : "University" = university
        self.gpa : float = 0.0
    
    def add_course(self, course_name : str, grade : str) -> None:
        """ Adds a course to the student """
        self.courses[course_name] = grade
        self.calculate_gpa()
    
    def calculate_gpa(self) -> None:
        gpa_scale : Dict[str,float] = self.university.gpa_scale
        sum : float = 0.0
        for key,value in self.courses.items():
            sum += gpa_scale[value]
        self.gpa = sum / len(self.courses)
    
    def get_completed_courses(self) -> List[str] :
        """ return a list of completed courses """
        return sorted([key for key, val in self.courses.items() if val not in self.university.failing_grade])
    
    def get_remaining_req_courses(self) -> List[str] :
        return sorted([course for course in self.major.required_courses if course not in self.courses or self.courses[course] in self.university.failing_grade])
    
    
    def get_remaining_ele_courses(self) -> List[str] :
        for course in self.major.elective_courses:
            if course in self.courses and self.courses[course] not in self.university.failing_grade:
                return []
        return sorted(list(self.major.elective_courses))

    def table_row(self):
        """ Returns a List os all attibutes for printing """
        return [self.cwid, self.name, self.major.name, self.get_completed_courses(), self.get_remaining_req_courses(), self.get_remaining_ele_courses(), float("{:.2f}".format(self.gpa))]

class Instructor:
    """ Class representing a Instructor in University """

    def __init__(self, cwid : str, name : str, department : str, university : "University") -> None:
        """ Constructor """
        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = defaultdict(set)
        self.university = university
    
    def add_course(self, course_name, student_id):
        """ Adds a course to the Instructor """
        self.courses[course_name].add(student_id)
    
    def table_rows(self):
        """ Returns a List os all attibutes for printing """
        for course, students in self.courses.items():
            yield [self.cwid, self.name, self.department, course, len(students)]

class Major:
    """ Class representing a Major"""

    def __init__(self,name):
        """ Creates a major object """
        self.name = name
        self.required_courses : set[int] = set([])
        self.elective_courses : set[int] = set([])
    
    def add_course(self,course,required) -> None:
        if "R" == required:
            self.add_required_course(course)
            return
        self.add_elective_course(course)
    
    def add_required_course(self,course : str) -> None:
        """ adds a course to required coursers """
        self.required_courses.add(course)
    
    def add_elective_course(self,course : str) -> None:
        """ adds a course to elective coursers """
        self.elective_courses.add(course)

    def table_row(self):
        """ Returns a List of all attibutes for printing """
        return [self.name,list(self.required_courses),list(self.elective_courses)]


class University:
    """ Class representing a University """

    def __init__(self, name : str) -> None:
        """ Constructor """
        self.name = name
        self.students : Dict[str : Student] = {}
        self.instructors : Dict[str : Instructor] = {}
        self.majors : Dict[str : Major] = {}
        self.gpa_scale : Dict[str,float] = {
            "A" : 4.0, "A-" : 3.75 , "B+" : 3.25, "B" : 3.0 , "B-" : 2.75, "C+" : 2.25,
            "C" : 2.0, "C-" : 0.0, "D-" : 0.0, "D" : 0.0, "D+" : 0.0, "F" : 0.0  
        }
        self.failing_grade : List[str] = ["C-","D-","D","D+","F"]      
    
    # summary fo the student information allocated using prettytable
    def student_table(self):
        """ Prints student table """
        pt = PrettyTable(field_names=['CWID','Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Elective','GPA'])
        for student in self.students.values():
            pt.add_row(student.table_row())
        print(pt)
    

    # summary of the instructor information allocated using prettytable
    def instructor_table(self):
        """ Prints instructor table """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Student'])
        for instructor in self.instructors.values():
            for row in instructor.table_rows():
                pt.add_row(row)
        print(pt)
    
    # summary of the majors information allocated using prettytable
    def major_table(self):
        """ Prints instructor table """
        pt = PrettyTable(field_names=['Name', 'Required Courses', 'Elective Courses'])
        for major in self.majors.values():
            pt.add_row(major.table_row())
        print(pt)


class Universities:
    """ Class for Universities """
    __instance = None

    @staticmethod
    def get_instance():
        """ Returns the singleton instance of universites """
        if Universities.__instance == None:
            Universities()
        return Universities.__instance

    
    
    def __init__(self):
        """ Constructor """
        if Universities.__instance != None:
            raise Exception("This is a singleton class. Please use get_instance() method")
        self.universities = {}
        self.process_errors = []
        Universities.__instance = self
    
    def file_reader(self, path : str, fields : int, error_list : List[str], sep : str = "\t", header : bool = False) -> Iterator[List[str]]:
        ''' defining the function to read the lines of the file
            and separate with header and rows of lines''' 
        try:
            fp = open(path,"r")
        except FileNotFoundError:
            raise FileNotFoundError()
        else:
            with fp:
                line_number : int = 0
                for line in open(path):
                    line_number += 1
                    if line_number == 1 and header:
                        continue
                    
                    line_items = [word for word in line.strip().split(sep)]
                    
                    if(len(line_items) != fields):
                        error_list.append(f"Error : In the file {path}, the number of fields in line {line_number} is not equal to {fields}(is {len(line_items)})")
                        continue

                    line_items.append(line_number)
                    line_tuple : Tuple[str] = tuple(line_items)


                    yield line_tuple
    
    def __process_directory(self, directory : str, university : University):
        """ process the directory and looks for files"""
        if not os.path.isdir(directory):
            raise Exception("Not a directory")
        
        self.process_errors = []
        for file in os.listdir(directory):
            if file.endswith("majors.txt"):
                for major, required, course, line_number in self.file_reader(os.path.join(directory,file), 3, self.process_errors,"\t",True):
                    if major not in university.majors:
                        university.majors[major] = Major(major)
                    university.majors[major].add_course(course,required)
                    
        for file in os.listdir(directory):
            if file.endswith("students.txt"):
                for cwid, name, major, line_number in self.file_reader(os.path.join(directory,file), 3, self.process_errors,";",True):
                    if cwid in university.students:
                        self.process_errors.append(f"Error in Student.txt:{line_number} - Student with cwid {cwid} already exist")
                        continue
                    university.students[cwid] = Student(cwid,name,university.majors[major],university)
            elif file.endswith("instructors.txt"):
                for cwid, name, dept, line_number in self.file_reader(os.path.join(directory,file), 3, self.process_errors, "|", True):
                    if cwid in university.instructors:
                        self.process_errors.append(f"Error in instrtuctors.txt:{line_number} - Instructor with cwid {cwid} already exist")
                        continue
                    university.instructors[cwid] = Instructor(cwid,name,dept,university)

        for file in os.listdir(directory):
            if file.endswith("grades.txt"):
                for student_cwid, course, grade, instructor_cwid,line_number in self.file_reader(os.path.join(directory,file), 4, self.process_errors, "|", True):
                    
                    if instructor_cwid not in university.instructors:
                        self.process_errors.append(f"Error in grades.txt:{line_number} - Instructor with cwid {instructor_cwid} doesnot exist")
                        continue
                    if student_cwid not in university.students:
                        self.process_errors.append(f"Error in grades.txt:{line_number} - Student with cwid {student_cwid} doesnot exist")
                        continue
                    university.students[student_cwid].add_course(course,grade)
                    university.instructors[instructor_cwid].add_course(course,student_cwid)
        
        if(len(self.process_errors) != 0):
            print("There were errors processing the file")
            for error in self.process_errors:
                print(error)

                
    def add_university(self, university_name : str, directory : str):
        """ Adds a new university """
        new_university = University(university_name)
        self.__process_directory(directory, new_university)
        self.universities[university_name] = new_university
        

if __name__ == "__main__":
    univs = Universities.get_instance()
    univs.add_university("stevens","C:\Stevens\Sem 3\SSW - 810\Assignments\git\Student-Repository\Stevens")
    print("------------------Stevens-----------------------")
    stevens = univs.universities["stevens"]
    stevens.major_table()
    stevens.student_table()
    stevens.instructor_table()

    # univs.add_university("NYU","C:\Stevens\Sem 3\SSW - 810\Assignments\HW09_kishan_Huliyar_jagadeesh\Stevens")
    # nyu = univs.universities["NYU"]
    # print("--------------------NYU----------------------")
    # nyu.student_table()
    # nyu.instructor_table()
    




        


    