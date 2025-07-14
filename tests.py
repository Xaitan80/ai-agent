#from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
def run_tests():
    print("Result for current directory:")
    print(run_python_file("calculator", "main.py"))

    print("\nResult for 'pkg' directory:")
    print(run_python_file("calculator", "tests.py"))

    print("\nResult for '/bin' directory:")
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    run_tests()
