import whois # 👉️ Import whois module


domain = []
taken = []
availabile = []



with open(file='./list.txt',mode='r',encoding='utf8') as f:
    count = 0
    for i in f:
        data = i.rstrip()
        count += 1
        domain.append(data)
        if count > 10:
            break
    
try:
    for i in domain:
        info = whois.whois(i)
        print(info)
except:
    print("Error")
# dm_info =  whois.whois("ictincub.my.id") # 👉️ Get Domain Info

# print(dm_info)