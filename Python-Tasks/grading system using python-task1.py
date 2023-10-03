#grading system using python.
# Taking names of each person.
while(True):
    def name(names,score):
        if score>=85 and score<=100:
            return "Your garde is A "
        elif score>=75 and score<85:
            return "Your garde is B "
        elif score>=65 and score<75:
            return "Your garde is C "
        elif score>=65 and score<55:
            return "Your garde is D "
        elif score>=35 and score<=55:
            return "Your have passed the test "
        elif score < 35 and score >=0:
            return "You failed in the test "
        else:
            return "Invalid input "
    names=input("Enter name : ")
    score=int(input("enter score : "))
    print(name(names,score))