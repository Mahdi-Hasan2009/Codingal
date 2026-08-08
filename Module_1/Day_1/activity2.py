fullmarks = input("Enter the total marks: ")
mathres = float(input("Enter the marks of Math: "))
englishres = float(input("Enter the marks of English: "))
banglares = float(input("Enter the marks of Bangla: "))
historyres = float(input("Enter the marks of History: "))

print(f"Your total marks : {fullmarks} , Math: {mathres} , English: {englishres} , Bangla: {banglares} , History: {historyres}")

totalmarks = mathres + englishres + banglares + historyres
avr = totalmarks / 4
percentage = (totalmarks / float(fullmarks)) * 100
print(f"Your total marks: {totalmarks} , Average: {avr} , Percentage: {percentage}%")

