import os 

x = input("Do you want to shut your pc down:(yes/no) ").lower()

def shutdown(acception):
  if acception == "yes":
    print("shutting down...")
    os.system("shutdown /s /t 1")
  else:
    print("Ok")
    
shutdown(x)