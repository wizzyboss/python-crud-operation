#a=[1,2,3]
#b=sum(a)
#print(b)

#a={"milk": 50, "bread": 50, "eggs": 30}
#a["milk"]=40
#a["cheese"]=60
#del a["bread"] 
#print(a)









#first=int(input("Enter the first number: "))
#second=int(input("Enter the second number: "))
#a=[]
#d=(first,second)
#a.append(d)
#b=sum(d)
#print(b)


#first=(input("Enter a commodity"))
#second= int(input("Enter the price"))
#a={}
#d=(first,second)
#a[first]=second
#print(a) 

#item=(input("Enter item: "))
#price= int(input("Enter the price: "))
#a={}
#a[item]=price
#print(a) 
names = []
prices = []

# collect data from 5 users
for i in range(5):
    item = input("Enter item: ")
    price = int(input("Enter the price: "))
    
    names.append(item)
    prices.append(price)

# create dictionary
data = {
    "items": names,
    "prices": prices
}

print(data)