import pandas as pd

lexique = pd.read_csv("lexique.csv",  encoding='latin-1')
proba = pd.read_csv("lexique.csv",  encoding='latin-1')

MISS = 0
MISPLACED = 1
EXACT = 2

def pattern_to_string(pattern):
    d = {MISS: "⬛", MISPLACED: "🟨", EXACT: "🟩"}
    p = list(pattern)
    for i,a in enumerate(p): 
        p[i]=int(a)
    return "".join(d[x] for x in list(p))

def ugly_generator():
    l= []
    m= []
    o= []
    q= []
    s= []
    for i in [0,1,2]:
        l.append(i)
        l.append(i+10)
        l.append(i+20)
    for i in l:
        m.append(i+100)
        m.append(i+200)
    n = m + l
    for i in n:
        o.append(i+1000)
        o.append(i+2000)
    p= n + o
    for i in p:
        q.append(i+10000)
        q.append(i+20000)
    r = p + q
    for i in r:
        y = str(i)
        while len(y)<5:
            y = "0" + y
        s.append(y)
    
    return s

def filter_from_pattern(tested_word, word, pattern):
    green = []
    yellow = []
    filter_green = False
    filter_yellow = False
    for i in range(0,5):
        if pattern[i] == "2":
            if word[i] == tested_word[i]:
                green.append(True)
            else: 
                green.append(False)
        if pattern[i] == "1":
            if word[i] in tested_word:
                yellow.append(True)
            else: 
                yellow.append(False)
    if not False in green:
        filter_green = True   
    if not False in yellow:
        filter_yellow = True  

    if filter_green and filter_yellow:
        return True
    else:
        return False

def get_proba_from_lexique(word, pattern, lexique):
    lexique["Can be "+pattern] = lexique["Mots"].apply(lambda x: filter_from_pattern(x, word, pattern))
    p = len(lexique[ lexique["Can be "+pattern] == True ])
    lexique.drop(columns=["Can be "+pattern])
    return p 
        
def get_proba(pattern, df):
    print("Pop")
    return df["Mots"].apply(lambda x: get_proba_from_lexique(x, pattern, lexique))
    

# word = input("Votre mot : _ _ _ _ _\n")
# pattern = input("Séquence ? 0=MISS 1=MISPLACED 2=EXACT\n")
# readable_pattern = pattern_to_string(pattern)
# print("Séquence : " + readable_pattern)
list_pattern = ugly_generator()
new_columns = pd.DataFrame({f"{pat}": get_proba(pat, proba) for pat in list_pattern})
df = pd.concat([proba, new_columns], axis=1)
df["sum"] = df.sum(axis=1)
df["average"] = df["sum"].apply(lambda x: (x/(len(lexique)*len(list_pattern)))*100)

df.to_csv("proba_pattern.csv", sep=";")

print(df)
print(df["average"])
print(df[df['average']==df['average'].max()])






