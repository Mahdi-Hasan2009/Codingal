for i in range(5):
  print(i)
  """👉 range(5) = 0 থেকে 4
👉 ৫ বার চলবে
  """
# --------------------
i = 0 
while i <5 :
  print(i)
  i +=1
# 👉 শর্ত সত্য থাকলে চলবে
# --------------------

for i in range(5):
  print("*",end = "")

#end="" → new line না
#loop ৫ বার → ৫টা star
# --------------------

# Vertical Star

for i in range(5):
  print("*")
  
# --------------------

# right triangle 

for i in range(1,6):
  print('*' * i)
  
i = 1

while i <=5 :
  print("*" * i)
  i = i+1
  
# --------------------

for i in range(5, 0,-1): # -1 must
    print("*" * i)
    
n = 5
for i in range(n):
  print(" " * (n- i -1) + "*" * (2*i +1) )



# --------------------

# full diamond 

n = 5

# Upper part
for i in range(n):
    print(" " * (n - i - 1) + "*" * (2*i + 1))

# Lower part
for i in range(n-2, -1, -1):
    print(" " * (n - i - 1) + "*" * (2*i + 1))
    
    
for i in range()