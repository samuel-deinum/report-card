import pandas as pd
from pandas import DataFrame


#Three Classes were created
class Report:
        def __init__(self):
                self.students = {}

class Student: 
        def __init__(self, id, name):
                self.id = id
                self.name = name 
                self.tests = {}
                self.courses = {}
        
        def totalAvg(self):
                totalMarks = 0.0
                for key,value in self.courses.items():
                        totalMarks = totalMarks + value.finalGrade
                return "%.2f" % round(totalMarks/len(self.courses.items()),2)
class Course: 
        def __init__(self):
                self.finalGrade = 0.0
                self.allWeights = 0

        def addTest(self,m,w):
                self.finalGrade = self.finalGrade + m*w/100
                self.allWeights = self.allWeights + w


#Open CSV files using pandas, move data into dataframes
try:
        with open("courses.csv", mode='r') as csv_file:
                courses = pd.read_csv(csv_file, delimiter=',' , keep_default_na=False) 
except OSError as e:
        print("Can not access courses.csv")
        exit()

try:
        with open("students.csv", mode='r') as csv_file:
                students = pd.read_csv(csv_file, delimiter=',' , keep_default_na=False) 
except OSError as e:
        print("Can not access students.csv")
        exit()

try:
        with open("tests.csv", mode='r') as csv_file:
                testsData = pd.read_csv(csv_file, delimiter=',' , keep_default_na=False) 
except OSError as e:
        print("Can not access tests.csv")
        exit()

try:
        with open("marks.csv", mode='r') as csv_file:
                marks = pd.read_csv(csv_file, delimiter=',' , keep_default_na=False)
except OSError as e:
        print("Can not access marks.csv")
        exit() 

def printReport(): 
        #Create Report Object
        report = Report()

        #Fill Report Objects student dictionary with Student Objects from the students.csv file
        for x in range(students.shape[0]):
                report.students[students["id"][x]] = Student(students["id"][x], students["name"][x])

        #Fill the Student Objects tests dictionary test results
        #Organise each test with each student object
        for x in range(marks.shape[0]):
                report.students[marks["student_id"][x]].tests[marks["test_id"][x]] = marks["mark"][x]

        #Loop through each test with each student. 
        #If the student wrote the test, It will create a course object if not created already, the perform
        #the add test function that will add the percent results to the total amount
        for x in range(testsData.shape[0]):
                for y in range(len(report.students.keys())):
                        k = list(report.students.keys())[y]
                        if testsData["id"][x] in report.students[k].tests:
                                testMark = report.students[k].tests[testsData["id"][x]]
                                testWeight = testsData["weight"][x]
                                if (not testsData["course_id"][x] in report.students[k].courses.keys()):
                                        mCourse = Course()
                                        mCourse.addTest(testMark,testWeight)
                                        report.students[k].courses[testsData["course_id"][x]] = mCourse
                                else:
                                        report.students[k].courses[testsData["course_id"][x]].addTest(testMark,testWeight)


        #Use the report object to print out the results
        s = ""
        for sKey, sValue in report.students.items():
                s = s + "Student Id: " + str(sKey) + ", name: " + sValue.name + "\n"
                s = s + "Total Average:     " + str(sValue.totalAvg())+"%\n\n"
                
                for cKey,cValue in sValue.courses.items():
                        if cValue.allWeights != 100:
                                raise Exception("Test do not add up to a hundred for "+ courses["name"][cKey-1])

                        s = s + "       Course: " + courses["name"][cKey-1] + ", Teacher: " + courses["teacher"][cKey-1] + "\n"
                        s = s + "       Final Grade:     " + str("%.2f" % round(cValue.finalGrade,2)) + "%\n\n"
                s = s + "\n\n"

        print(s)
        f = open("results.txt", "w+")
        f.write(s)
        f.close()


printReport()