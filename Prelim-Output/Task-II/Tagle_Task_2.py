# Tagle, Marc Neil V. - M001

import re

hashMatch = 0
love = []
giftNames = []
giftQuantity = []
giftPrices = []
num = []

with open(r'Prelim-Output\love_letter.txt', 'r', encoding="utf-8") as file:
    inside_gifts_section = False
    
    for line in file:
        line = line.strip()

        date = re.match(r'\d{4}-\d{2}-\d{2}', line)
        if date:
            print(date.group())
        
        if re.search(r'^#', line):
            print(line)
            hashMatch += 1 # Counting matches

        love.extend(re.findall('love', line, re.IGNORECASE))

        num.extend(re.findall('\d+', line))
        
        if re.search(r'# Gifts & Prices', line):
            inside_gifts_section = True
            continue

        if inside_gifts_section and re.search(r'^#', line):
            inside_gifts_section = False
        
        if inside_gifts_section:
            match = re.match(r'^(.*?):\s\$(\d+\.\d+)\s-\s(\d+).*', line)
            if match:
                giftNames.append(match.group(1))
                giftPrices.append(float(match.group(2)))
                giftQuantity.append(int(match.group(3)))

loveCount = len(love) # Counting matches
numAverage = sum(int(x) for x in num) / len(num) # Calculating average
giftDict = {name: (price, qty) for name, price, qty in zip(giftNames, giftPrices, giftQuantity)}

totalPrice = sum(qty * price for qty, price in giftDict.values()) # Total

highPrice = max(giftPrices) # Maximium value
lowPrice = min(giftPrices) # Minimum value
highGift = giftNames[giftPrices.index(highPrice)]
lowGift = giftNames[giftPrices.index(lowPrice)]

print()
print(f"The number of matches that start with a hashtag is {hashMatch}")
print(f"The total love count is {loveCount}")
print(f"The average of all numbers is {numAverage}")
print()
print(giftDict)
print()
print(f"The total gift price is {totalPrice} USD")
print(f"The most expensive gift is {highGift} which costs {highPrice} USD")
print(f"The least expensive gift is {lowGift} which costs {lowPrice:.2f} USD")