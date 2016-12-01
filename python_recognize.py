from PIL import Image
import traceback
import python_getpic
import os
#竖直模板库
#前四个为数字的特征向量，最后一个数字为该数字
#这些模板都是需要事先拿出十几张验证码试探得出的每个数字的特征向量
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
#漏网之鱼
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
    '''
     这个识别函数的过程是：首先对图像进行灰度处理，然后对验证码中每个数字进行切割，如果有四个数字，就切割成四份
     每一个数字相是由一个像素矩阵组成，然后求取每个数字的像素矩阵的特征值，然后再通过特征向量来匹配验证码。

     我只通过像素矩阵的竖直方向上的几列的特征像素值来判断验证码，正确率达到了97%，
     其实还可以通过横向的几列像素值的特征值，还有对角线的特征值继续判断，提高正确率。
      
    '''
    img=Image.open(p)
    #pix=img.load()
    img1=img.convert("L")
    #convert函数的作用：将图片转化为其他种类的色彩模式，如灰度图（将黑白之间分成若干个等级），
    #二值图（非黑即白），相关的模式有‘1，L,P,RGB.....’，这里用到的模式为L 转化为灰度图，
    #set_table（140）140是一个分界线，大于这个值的像素色值设为1，小于140的设为0，
    img2=img1.point(set_table(140),'1')
    pix2=img2.load()
    #得到这个图片像素的宽高
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
                #分别取0,2,4,6列的像素值作为这个数的特征向量
                if pix3[int(x3*2),y3] == 0:
                
                    jd2+=1
            yn.append(jd2)
        #print(yn)

        #开始识别
        for k in [list0,list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14]:
            t=0
            for m in range(0,4):
                t=t+(yn[m]-k[m])*(yn[m]-k[m])  #消除正负抵消的误差
            if t<2:    # 理论上t==0才符合要求,t<2是为了消除有些数字像素点缺漏的问题
                result=result+str(k[4])
                break
    global q
    if len(result)==4:
        q+=1
    else:
        result="unknow"+result
        print('第'+str(r)+'张未识别')
    
    path=global_path+str(result)+".jpg"
    img.save(path)
global_path=python_getpic.path+r"recognize/"

if __name__=='__main__':
    q=0
    end=python_getpic.num
    if os.path.exists(global_path):  
        pass
    else:
        os.makedirs(global_path)
        
    for i in range(end):
        try:                
            p=python_getpic.path+str(i)+".jpg"
            recognize_picture(p,i)
        except:
            print('something wrong')
            traceback.print_exc()
            break;
    print("识别了"+str(q)+"张验证码",'正确率为'+str((q/end)*100)+"%")
