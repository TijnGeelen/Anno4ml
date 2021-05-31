import os
import random

def process_data():
    """This function accesses the files in the directory and processes them to a seperate line for each file."""
    # Create a list of all paths
    paths = ['./adju-1-2', './adju-3-4', './adju-5-6','./adju-7-8']

    dataset = []
    for path in paths:
        for root in os.walk(path):
            taglist = []
            # If its not the directory itself
            if root[1] == []:
                for file in root[2]:
                    # Get the annotation files
                    if file.endswith(".ann"):
                        # Create a new variable line which contains the final line for the output in list format
                        line = []
                        fname = root[0]+ '\\' + file
                        # Read annotation files
                        with open(fname, 'r', encoding="utf8") as f:
                            content = f.readlines()
                            # Get the txt file of the current .ann file
                            fname = root[0] + '\\' + "{}.txt".format(file.split('.')[0])
                            # Read in the text of the whole tweet
                            with open(fname, 'r', encoding='utf8') as f2:
                                text = f2.readlines()
                                # Remove any newlines
                                stripped_text = []
                                for item in text:
                                    stripped_text.append(item.strip())
                            # If there is no main tag, give it a 'None' tag
                            if len(content) == 0:
                                line.append('None')
                                line.append('None')
                                line.append(fname)
                                line.append(" ".join(stripped_text))
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
                                        line.append(" ".join(stripped_text))
                                        break
                                    elif "Main" not in content[index]:
                                        count += 1
                                # If no main tag exists take first line
                                if len(content) == count:
                                    first_line = content[0].split()
                                    line.append(first_line[1])
                                    line.append('Main')
                                    line.append(fname)
                                    line.append(" ".join(stripped_text))
                        taglist.append(line)
            dataset.append(taglist)
    return dataset

def randomize_lines(dataset):
    """This function randomized the lines."""
    linelist = []
    for grp in dataset:
        for file in grp:
            linelist.append(" ".join(file) + "\n")
    random.shuffle(linelist)
    return(linelist)

def write_to_file(linelist):
    """This function writes the lines to an output file."""
    f = open('testfile.txt', 'w', encoding="utf-8")
    for line in linelist:
        f.write(line)
    f.close()

def main():
    dataset = process_data()
    randomized_linelist = randomize_lines(dataset)
    write_to_file(randomized_linelist)

if __name__ == "__main__":
    main()