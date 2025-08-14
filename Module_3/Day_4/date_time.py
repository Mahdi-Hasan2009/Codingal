#import datetime
import calendar

yy = 2025
mm1 =1
mm2 =2
mm3 =3
mm4 =4
mm5 =5
mm6 =6
mm7 =7
mm8 =8
mm9 =9
mm10 =10
mm11 =11
mm12 =12


print(calendar.month(yy,mm1))
print(calendar.month(yy,mm2))
print(calendar.month(yy,mm3))
print(calendar.month(yy,mm4))
print(calendar.month(yy,mm5))
print(calendar.month(yy,mm6))
print(calendar.month(yy,mm7))
print(calendar.month(yy,mm8))
print(calendar.month(yy,mm9))
print(calendar.month(yy,mm10))
print(calendar.month(yy,mm11))
print(calendar.month(yy,mm12))


from datetime import date,time,datetime

today = date.today()
now = datetime.now()
print("Today's date is",today)
print("\nCurrent Date and time is",now)

print("\nDate components",today.year,today.month,today.day)






