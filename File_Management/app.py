import os
def createFile(filename):
    try:
        with open(filename,mode='x') as file:
            print(f"FileName: {filename} created sucessfully")
    except FileExistsError:
        print(f"{filename} already exists")
    except Exception as e:
        print(f"Error occoured",e)

def view_all_files():
    files=os.listdir()
    if not files:
        print("No files found")
    else:
        print("Files in directory")
        for file in files:
            print(file)

def deleteFile(filename):
    try:
        os.remove(filename)
        print(f"{filename} has been deleted suceessfully")
    except FileNotFoundError:
        print(f"{filename} doesnot exist")
    except Exception as e:
        print("Error occoured while deleting")

def read_file(filename):
    try:
        with open('sample.txt','r') as file:
            content=file.read()
            print(f" Content of filename: {content}")
    except FileNotFoundError:
        print(f"{filename} doesnot exist ")
    except Exception as e:
        print(f"An error occuoured",e)

def edit_file(filename):
    try:
        with open('sample.txt','a') as file:
            content=input("Enter data to add: ")
            file.write(content+"\n")
            print("Content added to filename sucessfully")
    except FileNotFoundError:
        print("File not found while editing")
    except Exception as e:
        print("An error occoured",e)

def main():
    while True:
        print("File Management App")
        print("1: Create a file")
        print("2: View all file")
        print("3. Delete a file")
        print("4. Read a file")
        print("5. Edit a file")
        print("6. Exit")

        choice=input("Enter your choice: ")
        if choice== '1':
            filename=input("Enter a filename to create= ")
            createFile(filename)
        elif choice== '2':
            view_all_files()
        elif choice== '3':
            filename=input("Enter a file to delete: ")
            deleteFile(filename)
        elif choice== '4':
            filename=input("Enter filename to read: ")
            read_file(filename)
        elif choice== '5':
            filename=input("Enter your filename to edit: ")
            edit_file(filename)
        elif choice== '6':
            print("Closing the app")
            break
        else:
            print("Imvalid choice you can only choose between 1 to 6")

if __name__=="__main__":
    main()

    







