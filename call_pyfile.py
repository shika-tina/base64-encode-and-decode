from base64_decode import convert_base64_to_file as de64
from base64_encode import convert_file_to_base64 as en64
if __name__ == "__main__":
    choice = input('encode -> 1\n' \
    'decode -> 2\n' \
    'encode + decode -> 3\n' 
    'infinite loop -> 4\n')
    choice = int(choice)
    if choice == 1:
        en64()
    elif choice == 2:
        de64()
    elif choice == 3:
        en64()
        de64()
    elif choice == 4:
        while True:
            en64()
            de64()