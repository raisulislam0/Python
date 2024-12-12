class Person:
	def __init__(self, firstName, lastName, idNumber):
		self.firstName = firstName
		self.lastName = lastName
		self.idNumber = idNumber
	def printPerson(self):
		print("Name:", self.lastName + ",", self.firstName)
		print("ID:", self.idNumber)
        

class Student(Person):
    def __init__(self, firstName, lastName, idNumber, scores):
        super().__init__(firstName, lastName, idNumber)
        
        self.scores = scores
        
        
    def calculate(self):
        student_num = sum(self.scores)/len(self.scores)
        
        if student_num >= 90:
            return 'O'
        elif student_num >= 80 and student_num < 90:
            return 'E'
        elif student_num >= 70 and student_num < 80:
            return 'A'
        elif student_num >= 55 and student_num < 70:
            return 'P'
        elif student_num >= 40 and student_num < 55:
            return 'D'
        else: 
            return 'T'            
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    # Write your constructor here
    

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    # Write your function here

line = input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(input()) # not needed for Python
scores = list( map(int, input().split()) )
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())
