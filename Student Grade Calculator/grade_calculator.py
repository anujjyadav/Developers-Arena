

def get_grade(mark):
    if mark >= 90:
        grade = "A"
    elif mark >= 80:
        grade = "B"
    elif mark >= 70:
        grade = "C"
    elif mark >= 60:
        grade = "D"
    else:
        grade = "F"

    return grade


def get_message(grade):
    if grade == "A":
        message = "Excellent work! You are outstanding! Keep it up!"
    elif grade == "B":
        message = "Great job! You are doing really well! Keep pushing!"
    elif grade == "C":
        message = "Good effort! You are on the right track. Keep going!"
    elif grade == "D":
        message = "Don't give up! A little more effort will make a big difference!"
    else:
        message = "Don't be discouraged! Every expert was once a beginner. Try again!"

    return message



def get_valid_mark():
    while True:
        user_input = input("Enter mark (0 to 100): ")

        
        if not user_input.replace(".", "", 1).isdigit():
            print("Invalid! Please enter a number.")
            print()
            continue
        
        mark = float(user_input)

        if mark < 0 or mark > 100:
            print("Invalid! Mark must be between 0 and 100.")
            print()
            continue

        
        return mark


keep_going = True

while keep_going:

    
    name = input("Enter student name: ")
    
    mark = get_valid_mark()
    
    grade = get_grade(mark)

    message = get_message(grade)

    
    print()
    print("------------------------------------")
    print("Result for:", name)
    print("Mark      :", mark)
    print("Grade     :", grade)
    print("Message   :", message)
    print("------------------------------------")
    print()

    again = input("Check another student? (yes or no): ")
    print()

    if again.lower() == "yes" or again.lower() == "y":
        keep_going = True
    else:
        keep_going = False

print("Thank you!")
print("Keep learning and growing!")
