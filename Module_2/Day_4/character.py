text = input("Enter a text: ") 
key = input("Enter a key: ")
count = 0

for i in range(len(text) - len(key) + 1):
    if text[i:i+len(key)] == key:
        count += 1

if count > 0:
    print(f"The key '{key}' appears {count} times in the string.")
else:
    print(f"The key '{key}' does not appear in the string.")
