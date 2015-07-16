from PIL import Image


#竖直模板库
#前四个为数字的特征向量，最后为该数字
list0 = [7,4,4,4,0]
list1 = [1,4,13,2,1]
list2 = [5,6,6,7,2]
list3 = [4,6,6,10,3]
list4 = [2,6,5,13,4]
list5 = [9,6,6,8,5]
list6 = [6,7,6,8,6]
list7 = [2,6,5,5,7]
list8 = [3,11,6,11,8]
list9 = [4,8,6,7,9]
list10 = [4,5,13,2,1]

list11 = [1,8,6,6,9]
list12 = [1,9,7,7,8]
list13 = [1,0,4,13,1]
list14 = [1,6,6,7,2]

#此函数用于设置像素值的转换，
def set_table(a):
    table=[]
    for i in range(256):
        if i<a:
            table.append(0)
        else:
            table.append(1)
    return table
def recognize_picture(p,r):
    img=Image.open(p)
    pix=img.load()
    img1=img.convert("L")
    img2=img1.point(set_table(140),'1')
    pix2=img2.load()
    (width,heigh)=img2.size
    x0=[]
    y0=[]

#x表示行，y表示列
#x0中存储列的位置，y0存储列每个列中像素为0（黑点）的个数
    for x in range(0,width):      
        jd=0
        for y in  range(1,heigh):           
            if pix2[x,y]==0:
                
                jd+=1
        y0.append(jd)
        if jd>0:     
            x0.append(x)
    #print(y0)
    #print(x0)
    count=[]
    for i in range(0,len(x0)-1):
        if (i-1)!=-1:
            if x0[i]-x0[i-1]>1 and x0[i+1]-x0[i]>1:
                count.append(i)    #只是保存位置值，而不立即移除，是因为考虑循环可能溢出
    for i in range(len(count)-1,-1,-1):  #逆向删除，是考虑到移除数据时，后面的数据会向前移动
        x0.remove(x0[count[i]])
    if x0[1]-x0[0]>1:   #之前的循环没有检查x0[0]
        x0.remove(x0[0])
    if x0[-1]-x0[-2]>1:  #和x0[-1]
        x0.remove(x0[-1]) 
    z=[]
    z.append(x0[0])
    #k=0
    for j in range(0,len(x0)-1):
        
        if(x0[j+1]-x0[j])>1:
            
            z.append(x0[j])
            z.append(x0[j+1])
    z.append(x0[-1])
    #print(z)
    sta1=z[0]
    end1=z[1]
    sta2=z[2]
    end2=z[3]
    sta3=z[4]
    end3=z[5]
    sta4=z[6]
    end4=z[7]
    box=[(sta1,0,end1,heigh),(sta2,0,end2,heigh),(sta3,0,end3,heigh),(sta4,0,end4,heigh)]
    result=''
    for j in range(0,4):   #四个验证码
        img3=img2.crop(box[j])
        #img3.show()
        (w3,h3)=img3.size
        pix3=img3.load()
        #print(w3,'--',h3)

        yn=[]
        xn=[]
        for x3 in range(0,4):
            jd2 = 0
            for y3 in range(1,h3):
            
                if pix3[int(x3*2),y3] == 0:
                
                    jd2+=1
            yn.append(jd2)
        #print(yn)
        
        for k in [list0,list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14]:
            t=0
            for m in range(0,4):
                t=t+(yn[m]-k[m])*(yn[m]-k[m])  #消除正负抵消的误差

            if t<2:    #消除有些数字像素点缺漏的问题
                result=result+str(k[4])
                break
    global q
    if len(result)==4:
        q+=1
    else:
        result="unknow"+result
        print('第'+str(r)+'张')
    #此处需要整改
    path='D:/Python34/Tools/hh/'+str(result)+".jpg"
    img.save(path)

q=0
for i in range(1000):
    try:
        #此处路径需要整改
        p="D:/python34/Tools/pic/"+str(i)+".jpg"
        recognize_picture(p,i)
    except:
        print('something wrong')
print("识别了"+str(q)+"张验证码",'正确率为'+str(q/1000))
