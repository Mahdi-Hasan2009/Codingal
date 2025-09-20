class reverse:
    def __init__(self, s):
        self.s = s


    def get_reversed(self):
        return self.s[::-1]  


word = input("Enter a word: ")   
obj = reverse(word)              
print("Reversed word:", obj.get_reversed())
