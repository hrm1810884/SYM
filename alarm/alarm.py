str = input()
#str = '<s>5時半にかけて</s>'
minute = 0
for i in range(len(str)):
    if str[i] == '1':
        hour = 10
    if str[i] in ['5','6','7','8','9']:
        hour = int(str[i])
    if str[i] == '3' or str[i] == '半':
        minute = 30


    