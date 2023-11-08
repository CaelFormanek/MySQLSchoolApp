import random
import sqlite3
import csv

print("")

# connect to database
conn = sqlite3.connect('./StudentDB.db')

# cursor allows python to execute SQL statements
mycursor = conn.cursor()

# create Student table
mycursor.execute("CREATE TABLE IF NOT EXISTS Student (StudentId INTEGER PRIMARY KEY,FirstName TEXT,LastName TEXT,GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT, State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER DEFAULT 0)")
conn.commit()

# function to validate GPA
def validateGPA():
    GPA = ""
    while 5:
        GPA = input("Enter GPA: ")
        try:
            GPA = float(GPA)
        except:
            print("Cannot convert " + GPA + " to float.")
            print("Try again")
            continue
        if (GPA < 0):
            print("GPA can't be negative")
            print("Try again")
            continue
        else:
            break
    return GPA

# function to validate FacultyAdvisor
def validateFacultyAdvisor():
    FacultyAdvisor = ""
    facultynames = ["Rene", "FooBar", "BarFoo", "Ener", "German"]
    while 5:
        FacultyAdvisor = input("Enter FacultyAdvisor (Rene, FooBarr, BarFoo, Ener, or German): ")
        if (FacultyAdvisor not in facultynames):
            print("Please retry, only use Rene, FooBarr, BarFoo, Ener, or German")
            continue
        else:
            break
    return FacultyAdvisor

# function to validate ZipCode
def validateZipCode():
    ZipCode = ""
    while 5:
        ZipCode = input("Enter ZipCode with 5 numbers: ")
        try:
            testZip = int(ZipCode)
        except:
            print("Cannot convert " + ZipCode + " to int.")
            print("Try again")
            continue
        if ((len(ZipCode) != 5 )):
            print("ZipCode must be exactly 5 numbers")
            print("Try again")
            continue
        else:
            break
    return ZipCode

def validateState():
    State = ""
    while 5:
        State = input("Enter State: ")
        state_names = {"Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado",
                       "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii",
                       "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts",
                       "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana",
                       "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico",
                       "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico",
                       "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia",
                       "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"}
        if (State not in state_names):
            print("Must be a valid state fully spelled out")
            print("Try again")
            continue
        else:
            break
    return State

def validateStudentID(deleteorupdate):
    StudentID = ""
    while 5:
        StudentID = input("Enter the StudentID for the student you would like to " + deleteorupdate + ": ")
        try:
            StudentID = int(StudentID)
        except:
            print("Cannot convert " + StudentID + " to integer.")
            print("Try again")
            continue
        # check if StudentID exists
        query = mycursor.execute("SELECT * FROM Student WHERE StudentID = ?", (StudentID,))
        size = 0
        for student in query:
            size += 1
        if size < 1:
            print("StudentID " + str(StudentID) + " does not exist.")
            print("Try a different StudentID")
            continue
        break
    return StudentID

# function to handle query results
def handleQuery(query):
    size = 0
    for student in query:
        size += 1
        print(student)
    if size < 1:
        print("No students with this criteria exist.")
        return

# function to import data into the table
def importDataIntoTable(filename):
    # get input file
    input_file = csv.DictReader(open(filename))

    # put data into table if it is empty
    sizequery = mycursor.execute("SELECT COUNT(*) from Student")
    actualsize = 0
    for size in sizequery:
        actualsize = size[0]

    if (actualsize == 0):
        print("executing")
        for row in input_file:
            facultynames = ["Rene", "FooBar", "BarFoo", "Ener", "German"]
            chosenname = facultynames[random.randint(0,4)]
            mycursor.execute(
                "INSERT INTO Student ('FirstName', 'LastName', 'GPA', 'Major', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'FacultyAdvisor') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['FirstName'], row['LastName'], row['GPA'], row['Major'], row['Address'],
                 row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber'],chosenname,))
            conn.commit()

# function to display students
def displayStudents():
    query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0")
    for student in query:
        print(student)

# function to add a student
def addNewStudent():
    FirstName = input("Enter student FirstName: ")
    LastName = input("Enter student LastName: ")
    GPA = validateGPA()
    Major = input("Enter major: ")
    FacultyAdvisor = validateFacultyAdvisor()
    Address = input("Enter Address: ")
    City = input("Enter City: ")
    State = validateState()
    ZipCode = validateZipCode()
    MobilePhoneNumber = input("Enter MobilePhoneNumber: ")

    mycursor.execute("INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber,))
    conn.commit()
    print("Insertion complete.")

# function to update student
def updateStudent():
    StudentID = validateStudentID("update")
    Major = input("Enter major: ")
    FacultyAdvisor = validateFacultyAdvisor()
    MobilePhoneNumber = input("Enter MobilePhoneNumber: ")

    mycursor.execute("UPDATE Student SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ? WHERE StudentID = ?", (Major, FacultyAdvisor, MobilePhoneNumber, StudentID,))
    print("Update complete.")
    conn.commit()

def deleteStudent():
    StudentID = validateStudentID("delete")

    mycursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentID = ?",
                     (1, StudentID,))
    print("Delete complete.")
    conn.commit()

# display students by specific attributes
def displayStudentsByAttributes():
    print("Type 1 for Major")
    print("Type 2 for GPA")
    print("Type 3 for City")
    print("Type 4 for State")
    print("Type 5 for FacultyAdvisor")
    selection = ""

    # check to see if selection is valid
    while 5:
        selection = input("Select attribute to search by: ")
        try:
            selection = int(selection)
        except:
            print("Cannot convert " + selection + " to int.")
            print("Try again")
            continue
        break

    while 5:
        # Major
        if (selection == 1):
            value = input("Enter the value for Major that you would like to search by: ")
            query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND Major = ?", (value,))
            handleQuery(query)
        # GPA
        elif (selection == 2):
            value = validateGPA()
            query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND GPA = ?", (value,))
            handleQuery(query)
        # City
        elif (selection == 3):
            value = input("Enter the value for City that you would like to search by: ")
            query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND City = ?", (value,))
            handleQuery(query)
        # State
        elif (selection == 4):
            value = input("Enter the value for State that you would like to search by: ")
            query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND State = ?", (value,))
            handleQuery(query)
        # FacultyAdvisor
        elif (selection == 5):
            value = validateFacultyAdvisor()
            query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND FacultyAdvisor = ?", (value,))
            if (value == "Null" or value == "None" or value == "null" or value == "none" or value == "<null>"):
                query = mycursor.execute("SELECT * FROM Student WHERE isDeleted = 0 AND FacultyAdvisor IS NULL")
            handleQuery(query)
        # invalid
        else:
            print("Invalid option.")
            print("Try again")
            continue
        break

# controls flow of user operations
def controlFlow():
    while 5:
        print("")
        print("Type 1 to display all students")
        print("Type 2 to add a new student")
        print("Type 3 to update a student")
        print("Type 4 to delete a student")
        print("Type 5 for search students by Major, GPA, City, State, Advisor")
        print("Type 6 to exit application")
        print("")

        selection = ""

        # check to see if selection is valid
        while 5:
            selection = input("Select option: ")
            try:
                selection = int(selection)
            except:
                print("Cannot convert " + selection + " to int.")
                print("Try again")
                continue
            break

        if (selection == 1):
            displayStudents()
        elif (selection == 2):
            addNewStudent()
        elif (selection == 3):
            updateStudent()
        elif (selection == 4):
            deleteStudent()
        elif (selection == 5):
            displayStudentsByAttributes()
        elif (selection == 6):
            print("Exiting application. Bye!")
            mycursor.close()
            return
        else:
            print("Invalid option.")
            print("Try again")
            continue
    return

# start off by putting data into table
importDataIntoTable("./students.csv")

# controlFlow() function will run the program
controlFlow()

