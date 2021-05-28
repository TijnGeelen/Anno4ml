import os
import random
paths = ['./adju-1-2','./adju-3-4','./adju-5-6','./adju-7-8']


dataset = []

# for every annotation pair in adju 1-2
for root in os.walk(paths[0]):
    taglist = []
    # If its not the directory itsself
    if root[1] == []:
        for file in root[2]:
            if file.endswith(".ann"):
                line = []
                #filenames.append(root[0]+ '\\' + file)
                fname = root[0]+ '\\' + file
                with open(fname, 'r', encoding="utf8") as f:
                    content = f.readlines()
                    if len(content) == 0:
                        line.append('None')
                        line.append('None')
                        line.append(fname)
                        line.append('None')
                    else:
                        count = 0
                        # Check if main tag exists and if so add it to right list
                        for index in range(len(content)):
                            if "Main" in content[index]:
                                prev_line = content[index - 1].split()
                                if prev_line[1] in ["Anger", "Anticipation", "Caring", "Disgust", "Fear", "Joy", "Sadness", "Surprise", "Trust", "Other", ""]:
                                    line.append(prev_line[1])
                                else:
                                    prev_line = content[index -2].split()
                                    line.append(prev_line[1])
                                line.append('Main')
                                line.append(fname)
                                text = []
                                for li in prev_line[3:]:
                                    if li.replace(";",'0').isdecimal():
                                        pass
                                    else:
                                        text.append(li)
                                tagspan = " ".join(text)
                                line.append(tagspan)

                                break
                            elif "Main" not in content[index]:
                                count += 1
                        # If no main tag exists take first line
                        if len(content) == count:

                            first_line = content[0].split()
                            line.append(first_line[1])
                            line.append('Main')
                            line.append(fname)
                            text = []
                            for li in prev_line[3:]:
                                if li.replace(";", '0').isdecimal():
                                    pass
                                else:
                                    text.append(li)
                            tagspan = " ".join(text)
                            line.append(tagspan)
                taglist.append(line)

    #print(len(taglist))
    dataset.append(taglist)

# delete first empty list
dataset.pop(0)

# randomize group order to make sure data is not skewed
random.shuffle(dataset)

f = open('testfile.txt', 'w', encoding="utf-8")
for grp in dataset:
    for file in grp:
        f.write(" ".join(file) + "\n")
f.close




