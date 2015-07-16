import requests

for i in range(0,1000):
    #此处路径自己调整，range中数字表示下载验证码的个数，如果改了那么另一个文件中的数字也需要整改
    
    path='D:/Python34/Tools/'+str(i)+".jpg"
    r=requests.get('http://jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS')
    with open(path,'bw') as f:
        f.write(r.content)
    
