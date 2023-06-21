# 将目录下所有的 metadata.pegasus.txt 生成 gamelist.xml。
# created by: xylon
import os
from xml.etree import ElementTree as ET

counter = 0
dictList = {"game": "name", "file": "path", "sort-by": "sortname", "description": "desc",
            "assets.box_front": "image", "assets.logo": "marquee", "assets.video": "video"}
mediaList = ("image", "marquee", "video")


def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# read all txt files in subfolders
def readTxtFiles(path):
    global counter
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("metadata.pegasus.txt"):
                counter += 1
                print(root + "/" + file)
                convert(root, file)


# conver metadata and save to gamelist.xml
def convert(path, fileName):
    metadata = os.path.expanduser(path + "/" + fileName)
    xmlFile = path + "/gamelist.xml"
    gameList = ET.Element("gameList")
    game = None
    with open(metadata, 'r', encoding='utf-8') as file:
        for line in file:
            if (line[0] == " " and line[1] == " "):
                key = "file"
                value = line[2:].strip()
            else:
                idx = line.find(":")
                if (idx < 1):
                    continue
                key = line[0:idx].strip()
                value = line[idx+1:].strip()

            if (value == ""):
                continue

            key = dictList.get(key) or key
            if (key == "name"):
                game = ET.SubElement(gameList, "game")
            elif (game is None):
                continue
            # add image logo video
            elif (key == "sortname"):
                fileName = os.path.basename(value).split('.')[0]
                mediaPath = "./media/" + fileName + "/"
                attr = ET.SubElement(game, "image")
                attr.text = mediaPath + "boxFront.jpg"
                attr = ET.SubElement(game, "marquee")
                attr.text = mediaPath + "logo.png"
                attr = ET.SubElement(game, "video")
                attr.text = mediaPath + "video.mp4"
            elif (key == "path" or key in mediaList):
                value = "./" + value

            # delete the same tag
            if (key in mediaList):
                for aName in game.findall(key):
                    game.remove(aName)

            attr = ET.SubElement(game, key)
            attr.text = value

    indent(gameList)
    tree = ET.ElementTree(gameList)
    tree.write(xmlFile, "UTF-8", xml_declaration=True)


readTxtFiles("./")
print('已完成，总转换数：' + str(counter))
os.system("pause")
