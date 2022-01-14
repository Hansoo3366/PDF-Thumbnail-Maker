from pdf2image import convert_from_path
from PIL import Image
import os
import sys
sys.path.append('./system/pdf2image')

file_name = ""

file_dir = os.getcwd()+'/PDF/' #원본 pdf 경로
file_list = os.listdir(file_dir)
file_list = [name for name in file_list if name[0] != "."] #숨김 파일 제외
file_list.sort()



#이미지 저장 모듈
def save_pdf_to_image(pdf_file_path, out_dir, save_name):
    
    poppler_path =os.getcwd()+'/system/poppler/21.12.0/bin/'#맥용 모듈 추가

    images = convert_from_path(pdf_file_path, poppler_path=poppler_path, dpi=72) #해상도 조절하려면 dpi=300 괄호안에 입력해서 조

    images[0].save(out_dir+save_name+'_thumb.png', 'PNG') #저장 될 이미지 이름

def crop_image(before_crop_path,after_crop_path):
    before_crop = before_crop_path
    after_crop = after_crop_path
    img = Image.open(before_crop)
    if img.size[0]*(170/120) > img.size[1]:
        crop_width = img.size[1]*(120/170) #세로를 자름
    else:
        crop_width = img.size[0]

    if img.size[0]*(170/120) > img.size[1]:
        crop_height = img.size[1]
    else:
        crop_height = img.size[0]*(170/120) #가로를 자름

    if img.size[0] > img.size[1]: #가로가 길때
        crop_x1 = (img.size[0] - crop_width)/2
        crop_x2 = img.size[0] - ((img.size[0] - crop_width)/2)
        crop_y1 = 0
        crop_y2 = img.size[1]
    elif img.size[0] < img.size[1]: #세로가 길때
        crop_x1 = 0
        crop_x2 = img.size[0]
        crop_y1 = (img.size[1] - crop_height)/2
        crop_y2 = img.size[1] - ((img.size[1] - crop_height)/2)
    new_image = img.crop((int(crop_x1), int(crop_y1), int(crop_x2), int(crop_y2)))
    new_image.save(after_crop, "PNG", quality=95)

def main():
    save_name = ""
    count = 1
    for i in file_list:
        pdf_file_name = i

        save_name = i.split('.pdf')[0]
        before_crop_path = os.getcwd()+'/pdf_thumb/'+save_name+'_thumb.png'
        after_crop_path = os.getcwd()+'/crop_thumb/'+save_name+'_thumb.png'
        
        pdf_file_path = file_dir + pdf_file_name
        out_dir = os.getcwd()+'/pdf_thumb/' #썸네일 저장 될 경로
        save_pdf_to_image(pdf_file_path, out_dir, save_name)
        crop_image(before_crop_path, after_crop_path)
        print(count,' : '+ pdf_file_name + ' --->  Save Success')
        count = count + 1
    print(count-1 , '개의 PDF 변환 완료')
    
if __name__ == '__main__':
    main()