from pdf2image import convert_from_path
from PIL import Image
import os


file_name = ""


folder_dir = os.getcwd() + '/PDF/'
folder_list = os.listdir(folder_dir)
folder_list = [name for name in folder_list if name[0] != "."]
folder_list.sort()




#이미지 저장 모듈
def save_pdf_to_image(pdf_file_path, out_dir, save_name):

    poppler_path =os.getcwd()+'/system/poppler/21.12.0/bin/'#맥용 모듈 추가

    images = convert_from_path(pdf_file_path, poppler_path=poppler_path, dpi=72) #해상도 조절하려면 dpi=300 괄호안에 입력해서 조

    images[0].save(out_dir+save_name+'_thumb.png', 'PNG') #저장 될 이미지 이름

def crop_image(before_crop_path, after_crop_path):
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
        img.show()
        side_margin_y = (img.size[1] - crop_height)/2
        crop_y1 = 0 + side_margin_y
        crop_y2 = crop_height + side_margin_y
        choose = input("Crop 할 위치 지정 (Left: l, Right: r, Center: c) : ") #가로 긴 pdf 크롭 할 위치 고를 수 있게 수정
        if choose == 'c':
            crop_x1 = (img.size[0] - crop_width)/2
            crop_x2 = img.size[0] - ((img.size[0] - crop_width)/2)

        elif choose == 'l':
            crop_x1 = 0
            crop_x2 = crop_width

        elif choose == 'r':
            crop_x1 = img.size[0] - crop_width
            crop_x2 = img.size[0]

    elif img.size[0] < img.size[1]: #세로가 길때
        side_margin_x = (img.size[0]-crop_width)/2
        crop_x1 = 0 + side_margin_x
        crop_x2 = crop_width + side_margin_x
        crop_y1 = (img.size[1] - crop_height)/2
        crop_y2 = img.size[1] - ((img.size[1] - crop_height)/2)
    new_image = img.crop((int(crop_x1), int(crop_y1), int(crop_x2), int(crop_y2)))
    new_image.save(after_crop, "PNG", quality=95)

def main():
    save_name = ""
    for j in folder_list:
        os.mkdir(os.getcwd() + '/PDF_thumb/' + j)
        os.mkdir(os.getcwd() + '/crop_thumb/' + j)
        file_dir = os.getcwd() + '/PDF/' + j + '/' # 원본 pdf 경로
        file_list = os.listdir(file_dir)
        file_list = [name for name in file_list if name[0] != "."]  # 숨김 파일 제외
        file_list.sort()
        for i in file_list:
            pdf_file_name = i
            save_name = i.split('.pdf')[0]
            before_crop_path = os.getcwd()+'/PDF_thumb/'+ j + '/' + save_name+ '_thumb.png' #크롭 전 이미지 경로
            after_crop_path = os.getcwd()+'/crop_thumb/'+ j + '/' + save_name+ '_thumb.png' #크롭 후 저장될 경로

            pdf_file_path = file_dir + pdf_file_name
            out_dir = os.getcwd()+'/PDF_thumb/' + j + '/' #썸네일 저장 될 경로
            save_pdf_to_image(pdf_file_path, out_dir, save_name)
            crop_image(before_crop_path, after_crop_path)
            print(pdf_file_name + ' --->  Save Success')


if __name__ == '__main__':
    main()
