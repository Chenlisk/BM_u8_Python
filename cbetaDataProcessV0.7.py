import os
import re
import sys

#==========================================================

def  readFile(filedir):
    with open(filedir, "r", encoding='utf-8') as f :
        plist = f.readlines()
    return plist

def writeFile(filedir,string):
    path = filedir[0:filedir.rfind("\\")]
    if not os.path.exists(path):
        os.makedirs(path) 
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)
      
def  processFile(filedir):
    #e.g 'H:\\WORKSPACE\\PuncData\\BM_u8-master\\BM_u8-master\\A\\A091\\new.txt'
    folder = re.search(r'BM_u8-master\\[A-Z]{1,2}\\',filedir).group()
    folder=folder[folder.find('\\')+1:folder.rfind('\\')]
    string=''
    plist=readFile(filedir)

    if folder =="B":
        string=B_process(plist) 
    elif folder =="GA":
        string=GA_process(plist) 
    elif folder =="N":
        string=N_process(plist) 
    elif folder =="ZW":
        string=ZW_process(plist) 
    else:
        pass
    
    # B_process(plist) #================

    prefix=''
    if string=='':
        prefix="@"
    #e.g 'H:\\WORKSPACE\\PuncData\\BM_u8-master\\BM_u8-master\\A\\A091\\new.txt'    
    addr = re.sub(r'\\new\.txt','.txt',filedir)
    addr = re.sub(r'BM_u8-master\\[A-Z]{1,2}\\','BM_u8_Result\\\\'+prefix,addr)
    
    writeFile(addr,string)
    print("-------->%s"%(addr))

#==========================================================
def B(plist):
    string = ''
    
    for i in range(0,len(plist)):
        plist[i] = re.sub(r'\n','$$\n',plist[i])  
        plist[i] = re.sub(r"[A-Z]+?\d+.+p.*?\d+[abcd]\d\d_?", "", plist[i]) 
        string+=plist[i]

    string = re.sub(r"##<mj \d\d\d>.*?\$\$", "\n", string) 
    string = re.sub(r"[ABCjJkY]##.+?\$\$", "\n\n", string)   
    string = re.sub(r'##<Q3>.+?\$\$','\n\n',string)   
     
    string = re.sub(r"[IP]##", "\n\n", string)    
    string = re.sub(r'<p(,\d)+?>','\n\n',string)  
    string = re.sub(r"P4#", "\n\n", string)       
    string = re.sub(r"Q\d#", "\n\n", string)       
    string = re.sub(r"##<Q3 m=.+?\$\$", "\n\n", string)    
    string = re.sub(r"Q3=.+?\$\$", "\n\n", string)    
    string = re.sub(r"　", '', string)    
    string = re.sub(r'<□>','❥',string)

    string = re.sub(r'\$\$\n##','',string)    
    string = re.sub(r'[WSs]?##','',string)  
    string = re.sub(r"\$\$", '', string)      

    # string = re.sub(r'\d{1,3}\.','',string)
    # string = re.sub(r'Q\d#','',string)       
    # string = re.sub(r"：\n\n", "：", string)   
    # # string = re.sub(r'△','',string)
    # # string = re.sub(r'●','',string)
    
    # # string = re.sub(r'◇','',string)   
    # string = re.sub(r'<o><p>','\n\n',string )  
    # string = re.sub(r'<u>','\n\n',string )  
    # string = re.sub(r"<I>", '', string)   
  
    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')

    lsp=string.split('\n\n')
    for i in range(0,len(lsp)):
        s=lsp[i]
        
        while re.search(r"\[.{0,4}>.{0,4}\]",s)!=None:#[稀>絺]
            c=re.search(r"\[.{0,4}>.{0,4}\]",s).group()
            a=c[c.find('>')+1:c.find(']')]
            s = s.replace(c,a)

        s = re.sub(r"\[.+[\+\-\*\/（）]?.+\]", "❥", s)       

        s='###' +s+'$$$'
        s=re.sub(r'###\d+?\.','',s) 
        s=re.sub(r'\d+?\$\$\$','',s) 
        s= s.replace('###','')   
        s= s.replace('$$$','')   

        s = re.sub(r"（.+?）", "", s) 
    #     s = re.sub(r"\(.+?\)", "", s)    
        s= s.replace('\n','')    
        s=re.sub(r'<.+?>','',s) 
    
        if len(s)<10:
            s=''               
    #     # if s.find('……')!=-1:
    #     #     s=''
        if s.find('△')!=-1:
            s=''            

        if s.count('的')>1:
            s=''                  
               
        if (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('」') or s.endswith('』'))==False:
            if s.count('。') > 5 and s.count('，') > 5:
                s+='。'    
            else:
                s=''

        if s.count('，') <= len(s)//20:
            s=''            

        lsp[i]=s        
    string='\n\n'.join(lsp)

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')    
    string=string.lstrip('\n').rstrip('\n')
    return string

#==========================================================
def N(plist):
    string = ''
    
    for i in range(0,len(plist)):
        pstr=plist[i]
        pstr=pstr.replace('\n','$$\n')        
        pstr = re.sub(r"[A-Z]+\d+.+p.*?\d+[a|b|c]\d\d_?", "", pstr) ###_#1        
 
        pstr = re.sub(r"##<mj \d\d\d>.*\$\$", "\n", pstr)         
        pstr = re.sub(r"##<p>.+<p,\d,\d>", "\n", pstr)
        pstr = re.sub(r"##<Q3 m=.+?><p>.+?<p,2,2>", "\n", pstr) 
        if re.search( r'##(<p(,\d)?>.{1,20})?<T,0,\d>.+(<T,0,5>.+)?\$\$', pstr, re.M|re.I)!=None:
            pstr = re.sub(r"##(<p(,\d)?>.{1,20})?<T,0,\d>", "\n", pstr)
            pstr = re.sub(r"<T,0,\d>", "，", pstr)
            pstr = re.sub(r"，\$\$\n?", "，", pstr)
            pstr = re.sub(r"\$\$\n?", "。", pstr)        
        pstr = re.sub(r"Q\d#.+<Q\d>.+<p.+>", "\n", pstr) 
        pstr = re.sub(r"Q\d#.{1,7}\$\$", "\n", pstr) 
        pstr = re.sub(r"Q\d{1,2}#.{1,10}<p,(0,)?2>", "\n", pstr) 
        pstr = re.sub(r"##<Q\d{1,2}>.+<p,(0,)?2>", "\n", pstr) 
        pstr = re.sub(r"##<Q\d{1,2}>.+<p,0,2>", "\n", pstr) 
        pstr = re.sub(r"##<Q\d{1,2} m=.+<p.+>", "\n", pstr)        
        pstr = re.sub(r"##<Q\d{1,2} m=.+\$\$", "\n", pstr)         
        pstr = re.sub(r"\[\d{1,3}\]", "", pstr) 
        pstr = re.sub(r"\[\>\]", "", pstr) 
        pstr = re.sub(r"<PTS\..+\.\d{1,3}(\.\d{1,5})?>", "", pstr) 
        pstr = re.sub(r".*<p,0,1><trans-mark.+>", "\n", pstr)            
        pstr = re.sub(r"##<p,22>——.+?——.+\$\$", "\n\n", pstr) 
        pstr = re.sub(r"##<p,22>——.+──.+\$\$", "\n\n", pstr) 
        pstr = re.sub(r"##<p,0,2>——.+?。", "\n", pstr) 
        pstr = re.sub(r"##<p,22>.+\$\$", "\n\n", pstr) 
        pstr = re.sub(r"<p,22>.{3,5}\$\$", "\n\n", pstr) 
        pstr = re.sub(r"##<p,2>", "\n", pstr)
        pstr = re.sub(r"##<p,\d(,-?\d)?>", "\n", pstr)       
        pstr = re.sub(r"##<p>.+<T,\d(,-\d)?>", "\n", pstr)
        pstr = re.sub(r" ##<p>.+<p,2,2>", "\n", pstr)  #P三〇<p,0,2>   
        pstr = re.sub(r"P##.{1,4}<p,0,2>", "\n", pstr)  #
        pstr = re.sub(r"##<p>.+\$\$", "\n", pstr)  
        pstr = re.sub(r"##<p.+>", "\n", pstr)
        pstr = re.sub(r"。</T>.*", "。\n", pstr) 
        pstr = re.sub(r"</T>。?", "。\n", pstr) 

        pstr = re.sub(r"Q\d#.+\$\$", "", pstr) 
        pstr = re.sub(r"</Q\d>.*\$\$", "", pstr)         
        pstr = re.sub(r"<Q\d>.+<Q\d>.+\$\$", "", pstr)  

        pstr = re.sub(r"##<T,0,3>", "\n", pstr) 
        pstr = re.sub(r".+<T,0,3>",'，',pstr) 
        pstr = re.sub(r".+<T,0,\d>",'',pstr) 
        string+=pstr
    string = re.sub(r"——\$\$\n+", "——", string)     
    string=string.replace('$$\n##','')
    string=string.replace('$$','')
    string=string.replace('##','')
    string=string.replace('　','')
    string=string.replace('<□>','❥')
    string = re.sub(r"<p,22>。", "\n\n", string)    
    string = re.sub(r"：\n\n", "：", string) 

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')


    lsp=string.split('\n\n')
    for i in range(0,len(lsp)):
        s= lsp[i] 

        while re.search(r"\[.{0,4}>.{0,4}\]",s)!=None:#[稀>絺]
            c=re.search(r"\[.{0,4}>.{0,4}\]",s).group()
            a=c[c.find('>')+1:c.find(']')]
            s = s.replace(c,a)

        s = re.sub(r"\[.+[\+\-\*\/（）]?.+\]", "❥", s)            

        s= re.sub(r"（.+?）", "", s)    
        s = re.sub(r"〔.+?〕", "", s)    
        s = re.sub(r"〈.+?〉", "", s)    
        s = re.sub(r"\(.+?\)", "", s)    
        s= s.replace('\n','')    

        if len(s)<5:
            s=''               
        if s.find('……')!=-1:
            s=''

        if (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('」') or s.endswith('』'))==False:
            s=''      
        
    string='\n\n'.join(lsp)

    nsp=string.split('」')
    for i in range(0,len(nsp)):
        if nsp[i].find('「')==-1:
            nsp[i]+='@@'
        else:
            p=nsp[i].find('「')
            new=nsp[i][p:]
            new=new.replace('\n\n','')
            nsp[i]=nsp[i][0:p]+new
    string='」'.join(nsp)            
    string = re.sub(r'@@」?', '', string) 

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')    
    string=string.lstrip('\n').rstrip('\n')
    return string

#==========================================================
def GA(plist):
    string = ''
    
    for i in range(0,len(plist)):
        pstr=plist[i]

        pstr = re.sub(r'\n','$$\n',pstr)        
        pstr = re.sub(r".+\d\dWQ2.+\$\$", "\n", pstr)
        pstr = re.sub(r"[A-Z]+\d+.+p.*?\d+[abcd]\d\dW?_?", "", pstr) 
        pstr = re.sub(r"##<mj \d\d\d>.*\$\$", "\n", pstr) 
        pstr = re.sub(r"##<Q\d{1,2} m=.+><p,(0,)?2>", "\n", pstr)    
        pstr = re.sub(r"##<Q\d{1,2} m=.+?>.+?<T", "\n<T", pstr)      
        pstr = re.sub(r"##<Q\d{1,2} m=.+?>.+?<", "\n<", pstr)  
        pstr = re.sub(r"##<Q[124] m=.+?>.+?\$\$", "\n", pstr)  
        pstr = re.sub(r"Q[12]=.+\$\$", "\n", pstr)    
        pstr = re.sub(r'<Q[23] m=.+?>','',pstr)
        pstr = re.sub(r"Q\d#.+\$\$", "\n", pstr) 
        pstr = re.sub(r".*<[Cc]>.*\$\$", "\n", pstr) 
        pstr = re.sub(r"j##.*\$\$","\n", pstr) 
        pstr = re.sub(r"<I><p,4,-2>", "", pstr) ##
        pstr = re.sub(r"<I><p,4,-4>.*\$\$", "\n", pstr)
        pstr = re.sub(r"<I1><p,\d,-\d>.+\$\$", "\n", pstr)
        pstr = re.sub(r"<I2><p,\d,-\d>", "", pstr)
        pstr = re.sub(r'<I\d><p,\d,-\d>','',pstr)
        pstr = re.sub(r"<p,\d,-\d>", "", pstr)
        pstr = re.sub(r'<L_sp>','\n',pstr)             
        pstr = re.sub(r"J-#.+\$\$", "\n", pstr)
        pstr = re.sub(r"</?reg>", '', pstr)
        pstr = re.sub(r"[ABC]##.+\$\$", "\n", pstr)
        pstr = re.sub(r"(##)?<Q4>.+?<p,0,2>", '\n\n', pstr) ##<Q4>賢良<p,0,2>
        pstr = re.sub(r"WQ2.+\$\$", "\n", pstr)
        pstr = re.sub(r"</Q\d>\$\$", '', pstr)
        pstr = re.sub(r"<Q3>", "\n\n", pstr)         
        pstr = re.sub(r"<z,0,2>", "", pstr)     
        pstr = re.sub(r"【圖】",'',pstr) 
        pstr = re.sub(r"##<I>",'',pstr) 
        pstr = re.sub(r"##<J>",'',pstr) 
        pstr = re.sub(r"</L>",'',pstr)             
        string+=pstr

    if len(string)<=2000:
        string=''
    else:
        if string[0:2000].count('，')+string[0:2000].count('。') < 20:
            string=''

    string = re.sub(r"##<Q4>", "\n", string) ##<Q4>賢
    string = re.sub(r"##<Q[12]>.+\$\$", "\n", string)##<Q2>晉$$
    string = re.sub(r'<Q4>','',string)      
    string = re.sub(r'<p,(0,)?2>','\n\n',string)   
    string = re.sub(r'<p,\d>','',string)
    string = re.sub(r'<T,0,2>','\n\n<T,0,2>',string)
    string = re.sub(r'<Q5>','\n\n<Q5>',string)
    string = re.sub(r"<I[12]>", '', string)    
    string = re.sub(r"<p,8,-2>", '', string)     
    string = re.sub(r'<resp="CBETA.+?">', '', string)     
    string = re.sub(r'\$\$\n##','',string)
    string = re.sub(r'\$\$','',string)
    string = re.sub(r'##','',string)
    string = re.sub(r'△','',string)
    string = re.sub(r'●','',string)
    string = re.sub(r'<□>','❥',string)
    string = re.sub(r'◇','',string)   
    string = re.sub(r'<p>','\n\n',string )  

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')

    lsp=string.split('\n\n')
    for i in range(0,len(lsp)):
        s=lsp[i]

        while re.search(r"\[.{0,4}>.{0,4}\]",s)!=None:#[稀>絺]
            c=re.search(r"\[.{0,4}>.{0,4}\]",s).group()
            a=c[c.find('>')+1:c.find(']')]
            s = s.replace(c,a)

        s = re.sub(r"\[.+[\+\-\*\/（）]?.+\]", "❥", s)    

        s = re.sub(r"（.+?）", "", s)    
        s = re.sub(r"〔.+?〕", "", s)    
        s = re.sub(r"〈.+?〉", "", s)    
        s = re.sub(r"\(.+?\)", "", s)    
        s= s.replace('\n','')    
        s = re.sub(r".*<[ABE]>.*", '', s)     

        if re.search(r"<T,0,[02]>.+?</T>",s)!=None:
            if s.find('<T,0,1>')==-1 and  s.find('　')==-1:
                s=''
            s=re.sub(r'<T,0,[02]>','',s)
            s=re.sub(r'<T,0,1>','。',s)            
            s=re.sub(r'　','，',s)
            s=re.sub(r'</T>','。',s)
            s=re.sub(r'。。','。',s)

        if re.search(r"<T,2>.+?</T>",s)!=None:   
            s=re.sub(r'<T,2>','',s)
            s=re.sub(r'　','，',s)
            s=re.sub(r'</T>','。',s)
            s=re.sub(r'。。','。',s)           

        s=re.sub(r'<.+>','',s) 
    
        if len(s)<10:
            s=''               
        if s.find('……')!=-1:
            s=''
        elif (s.endswith('：'))==True:
            s=''                  
        elif (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('」') or s.endswith('』'))==False:
            if s.count('。') > 5 and s.count('，') > 5:
                s+='。'    
            else:
                s=''
        else:
            pass

        if len(s)>50:
            if s.count('，')+s.count('。') < len(s)//10:
                s=''

        lsp[i]=s        
    string='\n\n'.join(lsp)

    nsp=string.split('」')
    for i in range(0,len(nsp)):
        if nsp[i].find('「')==-1:
            nsp[i]+='@@'
        else:
            p=nsp[i].find('「')
            new=nsp[i][p:]
            new=new.replace('\n\n','')
            nsp[i]=nsp[i][0:p]+new
    string='」'.join(nsp)   
    string = re.sub(r'@@」?', '', string) 

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')    
    string=string.lstrip('\n').rstrip('\n')
    return string

#==========================================================
def ZW(plist):
    string = ''
    
    for i in range(0,len(plist)):
        pstr=plist[i]

        pstr = re.sub(r'\n','$$\n',pstr)
        pstr = re.sub(r"[A-Z]+\d+.+p.*?\d+[abcd]\d\dW?_?", "", pstr) 
        pstr = re.sub(r"##<mj \d\d\d>.*\$\$", "\n", pstr) 

        pstr = re.sub(r"I##(<p,0,2>)?", "##", pstr)    
        pstr = re.sub(r"##<p,0,2>", "\n\n", pstr)    
        pstr = re.sub(r"\[\d{1,3}\]", "", pstr) 

        pstr = re.sub(r"[ABCjJY]##.+\$\$", "\n", pstr)
        pstr = re.sub(r"[QP]\d#.+\$\$", "\n\n", pstr)
        pstr = re.sub(r"##<I\d+>", "\n\n##", pstr)
        if re.search(r"<I\d+>〔[甲乙丙丁戊己庚辛壬癸]〕",pstr)!=None:#[稀>絺]
            pstr = re.sub(r"<I\d+>〔", '', pstr)
            pstr = re.sub(r"〕", '', pstr)            
         
        string+=pstr

    string = re.sub(r"<w><p,0,2>", '\n\n', string) 
    string = re.sub(r"<a><p,0,2>", '', string) 
    string = re.sub(r"<o><p,0,2>", '\n\n', string) 
    string = re.sub(r"<u><p,0,2>", '', string) 
    string = re.sub(r"<p,0,2>", '\n\n', string) 
    string = re.sub(r"<o><p>", '\n\n', string) 
    string = re.sub(r"<u><p,2>", '', string)   
    string = re.sub(r'\$\$\n##','',string)
    string = re.sub(r'\$\$','',string)
    string = re.sub(r'##','',string)
    string = re.sub(r'<Q2 m=.+?>','',string)
    string = re.sub(r'<p=h2>','\n\n',string)

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')
    string=string.lstrip('\n').rstrip('\n')

    string = re.sub(r'：\n{0,2}「','：「',string)
    string = re.sub(r'：\n{0,2}','：',string)

    msp=string.split('<Q1 m=錄文>〔錄文〕')
    for i in range(0,len(msp)):
        if msp[i].find('P〔錄文完〕')==-1:
            msp[i]=''
        else:
            p=msp[i].find('P〔錄文完〕')
            new=msp[i][0:p]
            msp[i]=new
    string='\n\n'.join(msp)  

    nsp=string.split('」')
    for i in range(0,len(nsp)):
        if nsp[i].find('「')==-1:
            nsp[i]+='@@'
        else:
            p=nsp[i].find('「')
            new=nsp[i][p:]
            new=new.replace('\n\n','')
            nsp[i]=nsp[i][0:p]+new
    string='」'.join(nsp)        
    string = re.sub(r'@@」?', '', string) 

    lsp=string.split('\n\n')
    for i in range(0,len(lsp)):
        s=lsp[i]
        
        s = re.sub(r"<T,0,[01234]>", '', s)
        s = re.sub(r"</T>", '', s)

        if s.count('□')<3:
            s= re.sub(r"□", '❥', s)        
        elif s.count('□')>=3:
            s=''   

        while re.search(r"\[.{0,4}>.{0,4}\]",s)!=None:#[稀>絺]
            c=re.search(r"\[.{0,4}>.{0,4}\]",s).group()
            a=c[c.find('>')+1:c.find(']')]
            s = s.replace(c,a)
        s = re.sub(r"\[.+[\+\-\*\/（）]?.+\]", "❥", s)    

        s = re.sub(r"（.+?）", "", s)    
        s = re.sub(r"〔.+?〕", "", s)    
        s = re.sub(r"〈.+?〉", "", s)    
        s = re.sub(r"\(.+?\)", "", s)    
        s= s.replace('\n','')    

        if re.search(r"<T,0,[02]>.+?</T>",s)!=None:
            if s.find('<T,0,1>')==-1 and  s.find('　')==-1:
                s=''
            s=re.sub(r'<T,0,[0123]>','',s)
            s=re.sub(r'</T>','',s)

        s=re.sub(r'<.+?>','',s) 
    
        if len(s)<10:                     
            s=''   
        if s.find('…')!=-1:         
            s=''
        elif (s.endswith('：'))==True:
            s=''                  
        elif (s.endswith('。') or s.endswith('？') or  s.endswith('！') or  s.endswith('」') or s.endswith('』'))==False:
            if s.count('。') > 5 and s.count('，') > 5:
                s+='。'    
            else:
                s=''
        else:
            pass

        lsp[i]=s        
    string='\n\n'.join(lsp)

    string = re.sub(r"P", '', string) 

    while string.find('\n\n\n')!=-1:
        string=string.replace('\n\n\n','\n\n')    
    string=string.lstrip('\n').rstrip('\n')
    return string

#==========================================================
def B_process(plist) :
    string = B(plist)
    return string
        
def GA_process(plist) :
    string =GA(plist)
    return string
    
def N_process(plist) :
    string =N(plist)
    return string
        
def ZW_process(plist) :
    string =ZW(plist)    
    return string

#==========================================================
if __name__ == '__main__':
    if len(sys.argv)>1 :
        path=sys.argv[1]
    else :
        p=''
        # p='\\B08'
        path='H:\\WORKSPACE\\PuncData\\BM_u8-master\\BM_u8-master\\B'+p
        # print ("---$:usage: cbetaDataProcess.py dirname.")        
        # sys.exit(1)
    print ("--------$:building file lists...")
    fileList = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('new.txt'):
                 fileList.append(os.path.join(dirpath, file))
    amax=len(fileList)
    for i in range(0,amax):
        print('\n',str(i+1).rjust(3,'0'),'/',amax,'---$: ',fileList[i])
        processFile(fileList[i])        
        # break#-----------------------------------
    print ("--------$:file lists built.")
#==========================================================
