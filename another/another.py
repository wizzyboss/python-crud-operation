import matplotlib.pyplot as plt

a = 'c:/Users/USER/OneDrive/DESKTOP/note.txt'   
values = []

with open(a, 'r') as file:
    for line in file:
        for x in line.split():
            num = int(x)

            if num == 8:
                break

            if num % 2 == 0:
                values.append(num)

x = list(range(len(values)))

plt.bar(x, values)
plt.title("Even Numbers")
plt.xlabel("Index")
plt.ylabel("Values")
plt.show()

