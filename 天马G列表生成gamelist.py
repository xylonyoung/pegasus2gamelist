# 将目录下所有的 metadata.pegasus.txt 生成 gamelist.xml。
# created by: xylon
# 注意 ：
#       1.m3u文件需手动更改，例如：PS1中的 露娜（这里我是直接删除m3u文件）。
#       2.naomi文件夹下的naomi,naomi2,naomigd，这3个文件应该不是游戏我直接删除了。
#       3.FBNEO hack文件有些是需要手动整理的。
import os
from xml.etree import ElementTree as ET

metadataName = "metadata.pegasus.txt"
counter = 0
dictList = {"game": "name", "file": "path", "description": "desc"}
mediaList = {"image": "boxFront.jpg",
             "marquee": "logo.png", "video": "video.mp4"}
uselessTag = ["assets.box_front", "assets.logo", "assets.video"]


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


# read all txt files in subfolder
def readTxtFiles(path):
    global counter
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(metadataName):
                counter += 1
                print(root + "/" + file)
                convert(root)


# convert metadata and save to gamelist.xml
def convert(path):
    metadata = os.path.expanduser(path + "/" + metadataName)
    xmlFile = path + "/gamelist.xml"
    gameList = ET.Element("gameList")
    game = None
    fileName = ""
    isMultipleFiles = False
    with open(metadata, 'r', encoding='utf-8') as file:
        for line in file:
            key = ""
            value = ""
            # check if it is a multiple files
            if (isMultipleFiles):
                key = "file"
                value = line.split("/")[0].strip()
                isMultipleFiles = False
            else:
                idx = line.find(":")
                if (idx < 1):
                    continue
                key = line[0:idx].strip()
                value = line[idx+1:].strip()

            # pass useless tag
            if (key in uselessTag):
                continue

            key = dictList.get(key) or key
            if (key == "name"):
                game = ET.SubElement(gameList, "game")
            elif (game is None):
                continue
            elif (key == "files"):
                isMultipleFiles = True
                continue
            elif (key == "path"):
                fileName = getFileName(value)
                value = mergePath(value)
            elif (key == "desc"):
                # add image logo video
                mediaPath = "./media/" + fileName + "/"
                for k, v in mediaList.items():
                    attr = ET.SubElement(game, k)
                    attr.text = mediaPath + getMediaFileName(path, fileName, v)
            elif (mediaList.get(key) is not None):
                value = mergePath(value)

            attr = ET.SubElement(game, key)
            attr.text = value

    indent(gameList)
    tree = ET.ElementTree(gameList)
    tree.write(xmlFile, "UTF-8", xml_declaration=True)


# get file name
def getFileName(name):
    if (name.rfind(".") < 0):
        return name
    else:
        return name[0:name.rfind(".")]


# get media file name
def getMediaFileName(path, folder, fileName):
    global missingCounter
    result = fileName
    aPath = os.path.join(path, "media", folder.split("/")[0])

    if (os.path.exists(aPath)):
        for name in os.listdir(aPath):
            if (fileName[0:2] in name):
                result = name
                continue

    return result


# merge path
def mergePath(path):
    return "./" + path


readTxtFiles("./")
print('已完成，总转换数：' + str(counter))
os.system("pause")
