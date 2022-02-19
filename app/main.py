import pandas as pd

lexique = pd.read_csv("lexique.csv",  encoding='latin-1')
proba = pd.read_csv("proba_pattern.csv",  encoding='latin-1', sep=";")

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
    grey = []
    filter_green = False
    filter_yellow = False
    filter_grey = False
    for i in range(0,5):
        if pattern[i] == "2":
            if word[i] == tested_word[i]:
                green.append(True)
            else: 
                green.append(False)
        if pattern[i] == "1":
            if word[i] == tested_word[i]:
                yellow.append(False)
            elif word[i] in tested_word: 
                yellow.append(True)
            else: 
                yellow.append(False)
        if pattern[i] == "0":
            if word[i] == tested_word[i]:
                grey.append(False)
            elif word[i] in tested_word:
                grey.append(False)
            else:
                grey.append(True)
    if not False in green:
        filter_green = True   
    if not False in yellow:
        filter_yellow = True  
    if not False in grey:
        filter_grey = True  

    if filter_green and filter_yellow and filter_grey:
        return True
    else:
        return False

def get_proba_from_lexique(word, pattern, lexique):
    col= "with" + word + " Can be "+pattern
    lexique[col] = lexique["Mots"].apply(lambda x: filter_from_pattern(x, word, pattern))
    p = len(lexique[ lexique[col] == True ])
    d = lexique[ lexique[col] == True ]
    lexique.drop(columns=[col])
    return p, d
        
def get_proba(pattern, df):
    return df["Mots"].apply(lambda x: get_proba_from_lexique(x, pattern, lexique))
    
def generate_table_proba(lexique):
    list_pattern = ugly_generator()
    new_columns = pd.DataFrame({f"{pat}": get_proba(pat, lexique) for pat in list_pattern})
    df = pd.concat([lexique, new_columns], axis=1)
    df["sum"] = df.sum(axis=1)
    df["average"] = df["sum"].apply(lambda x: (x/(len(lexique)*len(list_pattern)))*100)

    df.to_csv("proba_pattern.csv", sep=";")
    return df

proba["sum"] = proba.sum(axis=1)
proba["average"] = proba["sum"].apply(lambda x: (int(x)/(len(lexique)*243))*100)
lexique["average"] = proba["average"]

win=False
secret="foire"
df = lexique
while win==False:
    word = input("Votre mot : _ _ _ _ _\n")
    pattern = input("Séquence ? 0=MISS 1=MISPLACED 2=EXACT\n")
    readable_pattern = pattern_to_string(pattern)
    print("Séquence : " + readable_pattern)
    lenght, df = get_proba_from_lexique(word, pattern, df)
    df = df.drop(df[df["Mots"]==word].index)
    best = df[df['average']==df['average'].min()]
    print(df)
    print(best)
    if word == secret:
        win=True
        print("GG")






