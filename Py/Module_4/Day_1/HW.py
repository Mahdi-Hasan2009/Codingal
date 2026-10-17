"""def square_filter(start, end):
    squares = []
    even_squares = []
    odd_squares = []

    for i in range(start, end+1):
        sq = i ** 2
        squares.append(sq)

        if sq % 2 == 0:
            even_squares.append(sq)
        else:
            odd_squares.append(sq)

    print("All Squares:", squares)
    print("Even Squares:", even_squares)
    print("Odd Squares:", odd_squares)


square_filter(1, 10)"""



def square_converter(start,end):
  squares = []
  even_squares = []
  odd_squares = []
  
  for i in range(start,end+1):
    sq = i**2
    squares.append(sq)
    
    if sq % 2 == 0:
      even_squares.append(sq)
    else:
      odd_squares.append(sq)

  print("Squares:",squares)
  print("Even squares:",even_squares)
  print("Odd squares:",odd_squares)


square_converter(1,10)

