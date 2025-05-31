buyPrice = float(input("Enter Your Buying Price: "))
sellPrice = float(input("Enter Your Selling Price: "))
profit = sellPrice-buyPrice
loss = buyPrice-sellPrice
profPercent = (profit/buyPrice)*100
lossPercent = (loss/buyPrice)*100

if buyPrice<sellPrice:
  print(f"Your Profit is:{profit}$ & Persentage Profit is:{profPercent}%")
elif buyPrice>sellPrice:
  print(f"Your Loss is:{loss}$ & Persentage Profit is:{lossPercent}%")
else:
  print("No Profit & No Loss")