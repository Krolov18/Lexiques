# encoding: utf8
from PIL import Image
from PIL import ImageFile


def charger_images(*args):
    import itertools, collections
    dico = collections.defaultdict(set)
    for x, y in itertools.combinations(args, 2):
        if equal(x, y):
            dico[x] &= {y}
    return dico


def equal(img_file1, img_file2):
    # if img_file1 == img_file2:
    #     return True

    fp1 = open(img_file1, 'rb')
    fp2 = open(img_file2, 'rb')

    img1 = Image.open(fp1)
    img2 = Image.open(fp2)

    # ImageFile.LOAD_TRUNCATED_IMAGES = True
    b = img1 == img2

    fp1.close()
    fp2.close()

    return b


def main():
    print(equal("le bon coin 001.jpg", "le bon coin 001.jpg"))

if __name__ == '__main__':
    main()
