# This project was not done from the Codingal.



# Taking the total amount as input from the user
Amount = int(input("Please Enter the Amount for Withdraw :"))

#Calculating the number of notes of different denominations
note_1 = Amount//100
note_2 = (Amount%100)//50
note_3 = ((Amount%100)%50)//10
note_4 = (((Amount%100)%50)%10)//1
print( "Notes of 100 Taka" , note_1)
print( "Notes of 50 Taka" , note_2)
print( "Notes of 10 Taka" , note_3)
print( "Notes of 1 Taka" , note_4)
