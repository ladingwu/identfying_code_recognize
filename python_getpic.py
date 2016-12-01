import requests

for i in range(0,1000):
    #此处路径自己修改， 
    path='D:\code\python_image_learn\identfying_code_recognize\imgs\\'+str(i)+'.jpg'
    #这个地址下可以下载到普通的验证码
    r=requests.get('http://jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS')
    with open(path,'bw') as f:
        f.write(r.content)
    
