# 合并目录下的所有 gamelist.xml 文件，在当前文件夹生成 gamelist.xml 文件。
# created by: xylon
import os
import xml.etree.ElementTree as ET

counter = 0
gameList = ET.Element("gameList")


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


# read all xml files in subfolders
def readXmlFiles(path):
    global counter
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("gamelist.xml"):
                counter += 1
                print(root + "/" + file)
                writeXmlFile(root, file)


# write data to xml file
def writeXmlFile(path, file):
    root = ET.parse(path + "/" + file).getroot()
    hasGame = False
    for newGame in root.findall("game"):
        for game in gameList.findall("game"):
            # if the game name is the same, then skip it
            if (newGame.find("name").text == game.find("name").text):
                hasGame = True
                continue
        if (hasGame):
            hasGame = False
            continue
        modifyGameData(path, newGame)


# modify game data and store it in gameList
def modifyGameData(path, game):
    attrList = ["path", "image", "marquee", "video"]
    for attr in attrList:
        game.find(attr).text = path + game.find(attr).text[1:]
    gameList.append(game)


readXmlFiles("./")
# write a single xml file
indent(gameList)
tree = ET.ElementTree(gameList)
tree.write("gamelist.xml", "UTF-8", xml_declaration=True)
print('已完成，合并数：' + str(counter))
os.system("pause")
