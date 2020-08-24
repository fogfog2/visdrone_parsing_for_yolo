
import os

from PIL import Image, ImageDraw


count_v = 0 
all_v = 0

class_counter = [0,0,0,0,0,0,0,0,0,0,0,0]
class_counter2 = [0,0,0,0,0,0,0,0,0,0,0,0]
class_remain = [0,0,0,0,0,0,0,0,0,0,0,0]

def load(textfile,imagefile,new_filename):

    #load text file
    f = open(textfile)
   
    lines = f.readlines()

    #영역 제한 사이즈
    mw = 608
    mh = 608

    #load image file
    im=Image.open(imagefile)
    w, h = im.size # (width,height) tuple
    #dr = ImageDraw.Draw(im)

    #overlap 영역 계산 
    div_w =int(w / mw)
    div_h =int(h / mh)

    cols = div_w + 1 
    rows = div_h + 1

    overlapped_w=0
    overlapped_h=0
    if div_w>0:
        overlapped_w = (mw*cols - w)/div_w
    if div_h>0:
        overlapped_h = (mh*rows - h)/div_h

    #시작점 위치 계산
    s_x = []
    s_y = []
    for col in range(cols):
        s_x.append( col * (mw - overlapped_w) )
    for row in range(rows):
        s_y.append( row * (mh - overlapped_h) )


    #이미지가 608 608 보다 작은경우 크기 제한 
    if mw > w:
        mw = w

    if mh > h:
        mh = h


    #이미지 영역별 크롭 
    cropped_img = []
    area_list = []
    for x in s_x:
        for y in s_y:
            area = (x,y, x+mw, y+mh)
            area_list.append(area)
            cropped_img.append(im.crop(area))

    #크롭 보여주기
    #for c_img  in cropped_img:
    #    c_img.show()

    count_test = 0
    #print(textfile)
    area_count = 0
    for area in area_list:

        ax = area[0]
        ay = area[1]
        aw = area[2]
        ah = area[3]

        # cimg = im.crop(area)
        # dr = ImageDraw.Draw(cimg)

        data = []
        for line in lines:
            global count_v
            global all_v

            split_line = line.split(",")

            if float(split_line[0]) > ax and float(split_line[0]) < ax + aw and \
                float(split_line[1]) > ay and float(split_line[1]) < ay + ah and \
                float(split_line[0]) + float(split_line[2]) > ax and float(split_line[0]) + float(split_line[2]) < ax + aw and \
                float(split_line[1]) + float(split_line[3]) > ay and float(split_line[1]) + float(split_line[3]) < ay + ah:
                
                width = round(float(split_line[2])/aw,6)
                height = round(float(split_line[3])/ah,6)
                cx = round( (float(split_line[0])-ax) / aw + 0.5*float(split_line[2])/aw,6)
                cy =  round( (float(split_line[1])-ay) / ah +  0.5*float(split_line[3])/ah,6)     
                
                # analysis
                class_counter[int(split_line[5])] = class_counter[int(split_line[5])] +1
                all_v = all_v +  1

                #if(width < 0.026 or height <0.019):
                #    class_counter2[int(split_line[5])] = class_counter2[int(split_line[5])] +1
                #    count_v = count_v + 1
                
                #write data
                if(int(split_line[5]) == 1 or int(split_line[5]) == 2):
                    if(float(split_line[2]) > 16 and float(split_line[3]) > 16):
                        data.append("0" +" "+ str(cx) + " " + str(cy) + " " + str(width) + " " + str(height) +"\n")
                        class_counter2[int(split_line[5])] = class_counter2[int(split_line[5])] +1
                        count_v = count_v + 1
                            

                #draw data
                if(int(split_line[5]) == 1 or int(split_line[5]) == 2):
                    if(float(split_line[2]) > 16 and float(split_line[3]) > 16):
                        dr.rectangle(((cx*aw - 0.5*width*aw, cy*ah - 0.5*height*ah ), (cx*aw + 0.5*width*aw, cy*ah + 0.5*height*ah )), outline='#00ff88')
                        
                
        
        
        if len(data)>0:
            file_path = os.path.splitext(new_filename)
            
            ##annotation 저장
            path = file_path[0] + "_"  +  str(area_count) + file_path[-1]            
            nf = open(path,'a')
            for d in data:
                nf.write(d) 
            nf.close()
            
            ##image 저장
            imgpath = file_path[0] + "_" + str(area_count) + ".jpg"
            cropped_img[area_count].save(imgpath)

            
        area_count = area_count + 1
        # if len(data)>0:
        #     cimg.show()
    # del dr
    # if count_test==1:
    #     im.show()
    # elif count_test==2:
    #     im.show()
    #im.close()



    f.close()
    

def search(dirname, images, new_path):
    filenames = os.listdir(dirname)
    for filename in filenames:
        image_name= filename.replace("txt","jpg")
        full_imagename = os.path.join(images, image_name)
        full_filename = os.path.join(dirname, filename)
        new_filename = os.path.join(new_path, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.txt': 
            load(full_filename, full_imagename, new_filename)

#data
choice = 1 
if choice ==1:
    search("/home/sj/data/VisDrone2019-DET-train/VisDrone2019-DET-train/annotations"# path, annotation
    ,"/home/sj/data/VisDrone2019-DET-train/VisDrone2019-DET-train/images" # path, images
    ,"/home/sj/data/VisDrone2019-DET-train/VisDrone2019-DET-train/images_test") # path, 새로운 annotation 놓을 위치
elif choice ==2:
    search("/home/sj/data/VisDrone2019-DET-val/VisDrone2019-DET-val/annotations"# path, annotation
    ,"/home/sj/data/VisDrone2019-DET-val/VisDrone2019-DET-val/images" # path, images
    ,"/home/sj/data/VisDrone2019-DET-val/VisDrone2019-DET-val/images_test") # path, 새로운 annotation 놓을 위치
elif choice ==3:
    search("/home/sj/data/VisDrone2019-DET-test-dev/annotations"# path, annotation
    ,"/home/sj/data/VisDrone2019-DET-test-dev/images" # path, images
    ,"/home/sj/data/VisDrone2019-DET-test-dev/images_test") # path, 새로운 annotation 놓을 위치


per = count_v / all_v
print(class_counter)
print(class_counter2)
i = 0
for a, b in zip(class_counter, class_counter2):
    class_remain[i] = a-b
    i= i+1
print(class_remain)
print(per)