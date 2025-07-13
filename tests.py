#from functions.get_files_info import get_files_info
from functions.write_file import write_file
def run_tests():
    print("Result for current directory:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    print("\nResult for 'pkg' directory:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("\nResult for '/bin' directory:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    run_tests()
