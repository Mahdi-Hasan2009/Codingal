char = input("Enter a character: ")

if len(char) == 1 and (('a' <= char <= 'z') or ('A' <= char <= 'Z')):
    print(f"'{char}' is an alphabet.")
else:
    print(f"'{char}' is NOT an alphabet.")