import os
from xml.etree import ElementTree as ET

files = ["metadata.pegasus.txt"]
romPath = "./"
dictList = {"assets.box_front": "image", "assets.logo": "marquee",
            "assets.video": "video", "file": "path", "sort-by": "sortname", "description": "desc"}
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


def fileList(path):
    for pathDir in os.listdir(path):
        fullpath = os.path.join(path, pathDir)
        if os.path.isdir(fullpath):
            fileList(fullpath)
        elif os.path.isfile(fullpath):
            if fullpath.endswith("metadata.pegasus.txt"):
                fullpath = fullpath.replace("\\", "/")
                files.append(fullpath)
                print("Find out: " + fullpath)
                convert(fullpath)


def convert(metaFile):
    metaFile = os.path.expanduser(metaFile)
    romPath = os.path.dirname(metaFile)
    xmlFile = romPath + "/gamelist.xml"
    gameList = ET.Element("gameList")
    game = None
    name = ""
    with open(metaFile, 'r', encoding='utf-8') as file:
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

            if (key == "game"):
                name = value
                game = ET.SubElement(gameList, "game")
                att = ET.SubElement(game, "name")
                att.text = name
            elif (game is not None):
                key = dictList.get(key) or key
                if (key == "sortname"):
                    # add image logo video
                    fileName = os.path.basename(value).split('.')[0]
                    mediaPath = "./media/" + fileName + "/"
                    att = ET.SubElement(game, "image")
                    att.text = mediaPath + "boxFront.jpg"
                    att = ET.SubElement(game, "marquee")
                    att.text = mediaPath + "logo.png"
                    att = ET.SubElement(game, "video")
                    att.text = mediaPath + "video.mp4"
                if (key == "path" or key in mediaList):
                    value = "./" + value
                if (key in mediaList):
                    # delete the same tag
                    for aName in game.findall(key):
                        game.remove(aName)

                att = ET.SubElement(game, key)
                att.text = value

    indent(gameList)
    tree = ET.ElementTree(gameList)
    tree.write(xmlFile, "UTF-8", xml_declaration=True)


fileList(os.path.expanduser(romPath))
print('已完成，总转换数：' + str(len(files) - 1))
