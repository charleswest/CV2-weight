def idRule(mm):
    n = -1
    if 1 == 2: pass
    elif mm ==  ['wt', 2, 1, 1]: n = 1  
    elif mm ==  ['wt', 2, 2, 1]: n = 4  
    elif mm ==  ['wt', 2, 2, 2]: n = 0  
    elif mm ==  ['wt', 3, 1, 1]: n = 2 
    return n
if  __name__ == '__main__':
    db =  1
    print idRule(['wt', 3,1,1])

