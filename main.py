while True:
    print("\nMenu:")
    print("1. Open WebCam")
    print("2. Export and Email Attendance Records to Admin")
    print("3. Refresh List of Students in Database")
    print("4. Exit")

    choice = input("Enter your choice (1, 2, or 3):\n ")

    if choice == "1":
        exec(open("FaceRecAndSQL.py").read())
    elif choice == "2":
        exec(open("ExportAndEmail.py").read())
    elif choice == "3":
        exec(open("RefreshStudents.py").read())
    elif choice == "4":
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")

    ans = input("Do you want to run the program again? (y/n): ")
    if ans.lower() != "y":
        print("Exiting the program. Goodbye!")
        break
