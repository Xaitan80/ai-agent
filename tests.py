#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
def run_tests():
    print("Result for current directory:")
    print(get_file_content("calculator", "main.py"))

    print("\nResult for 'pkg' directory:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\nResult for '/bin' directory:")
    print(get_file_content("calculator", "/bin/cat"))


if __name__ == "__main__":
    run_tests()
