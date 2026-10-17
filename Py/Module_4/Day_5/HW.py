#list comprehension #dictionary comprehension


"""fruits = ["apple","banana","grapes","lichi"]

capitalizedFruit = [i.capitalize() for i in fruits  ]

print(capitalizedFruit) """

fruitInput = input("Enter fruits name like: (apple,banana,grape): ")
fruits = eval(fruitInput) 
capitalizedInput = [i.capitalize() for i in fruits]

print(capitalizedInput)



