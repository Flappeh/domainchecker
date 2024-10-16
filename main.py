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
    
for i in domain:
    try:
        info = whois.whois(i)
        print(f"""
Domain : {i}
Registrar : {info["registrar"]}
""")
    except:
        print(f"Error for domain : {i}")
# dm_info =  whois.whois("ictincub.my.id") # 👉️ Get Domain Info

# print(dm_info)