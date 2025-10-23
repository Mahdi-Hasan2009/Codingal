import pygame 

pygame.init()

screen = pygame.display.set_mode((600,400))
pygame.display.set_caption("Basic Pygame Functions")

# image load

image = pygame.image.load("E:\Codingal\practice\practice1\pygamegpt.py\images.jpeg")

# pygame text

font = pygame.font.Font(None,50)  # None = default font
text = font.render("Hello Pygame!",True,("Red"))
"""
text = font.render("Hello Pygame!", True, ("Red"))
এটা pygame.font.Font অবজেক্টের render() মেথড।
এর কাজ হচ্ছে 👉 একটা টেক্সটকে ইমেজ (Surface) আকারে তৈরি করা, যেন আমরা সেটাকে blit() করে স্ক্রিনে দেখাতে পারি।

🧩 এখন একে একে অংশগুলো বোঝো:
1️⃣ "Hello Pygame!"
এটা হচ্ছে টেক্সট — যা তুমি স্ক্রিনে দেখাতে চাও।

2️⃣ True
এইটা মানে antialiasing on করা আছে।

👉 Antialiasing মানে টেক্সটের ধার মসৃণ বা smooth করা, যেন খাঁজখাঁজ না লাগে।

True দিলে টেক্সটটা সুন্দর ও মসৃণ দেখাবে।

False দিলে টেক্সটটা একটু খসখসে বা পিক্সেলেটেড দেখাবে।

🧠 মনে রাখো: এটা শুধু ভিজ্যুয়াল পার্থক্য করে, টেক্সটের মানে না।

3️⃣ ("Red")
এইটা হচ্ছে রঙ, যেটা টেক্সটে প্রয়োগ হবে।
এখানে "Red" ব্যবহার করা হয়েছে, তবে তুমি চাইলে (255, 0, 0) (RGB মান) দিয়েও দিতে পারো।

🔹 সব মিলিয়ে এর মানে:
👉 "Hello Pygame!" টেক্সটটা লাল রঙে, smooth edges সহ,
একটা Surface object হিসেবে তৈরি হবে —
যেটাকে পরে তুমি screen.blit(text, (x, y)) দিয়ে স্ক্রিনে দেখাতে পারবে।
"""

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
      running = False
  screen.fill((0,150,200))
  # .blit() is important for text ,image , sprites and so on  
  screen.blit(image,(200,100)) # (x,y) position
  screen.blit(text, (150, 180))
  pygame.display.update() # ***

pygame.quit()
  