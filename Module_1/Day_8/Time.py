time_sec = int(input("Enter a Time in Second: "))
hours = time_sec //3600
minutes =(time_sec%3600)//60
seconds = (time_sec%3600)%60

print(f" Hours: {hours},Minutes: {minutes},seconds: {seconds}")