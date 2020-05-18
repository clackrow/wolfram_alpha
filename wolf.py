import requests
import xml.etree.ElementTree as ET
from PIL import Image
import matplotlib.pyplot as plt
import time



img_files = []


def search():
    search_term = input("Pesquisa: ")
    url = 'http://api.wolframalpha.com/v2/query?input=' + search_term + '&appid=YVQA58-TA2WLJYHK8'
    response = requests.get(url)
    XML_file = ET.fromstring(response.content)
    showText(XML_file)
    loadImgs(XML_file)
    print('----------------------------------------------------------------')
    search()

def showText(_XML: ET.fromstring):
    for n in _XML.findall('pod/subpod/plaintext'):
        if n.text is not None:
            print(n.text)
        else:
            print('')

def loadImgs(_XML: ET.fromstring):
    pods = []
    print('------------------')
    print('Imagens : ')
    loading = True
    while loading:
        print("Carregando imagens...")
        for item in _XML.findall('pod/subpod/img'):
            img_url = str(item.attrib['src'])
            req = requests.get(img_url, stream=True)
            img = Image.open(req.raw)
            img_files.append(img)
        loading = False
    if len(img_files) > 1:
        print("Imagens carregadas com sucesso!")
        print("Imagens disponíveis:")
        for x, item in enumerate(_XML.findall('pod/subpod/img')):
            print(str([x]) + ' ' + str(item.attrib['alt']))
            pods.append(item)
        showImgs()
    else:
        print("Sem imagens disponíveis")


def showImgs():
    index = input("Escolha uma imagem para ser mostrada, para sair escreva 'none': ")
    if str(index) != 'none':
        try:
            index = int(index)
            plt.imshow(img_files[index])
            plt.show()
            showImgs()
        except:
            print("Input inválido!")
            showImgs()
    else:
        img_files.clear()


try:
    search()
except:
    time.sleep(30)


