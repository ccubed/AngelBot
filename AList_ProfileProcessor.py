import re

def profile_preprocessor(content):
    # Compile Regular Expressions
    imgtag = re.compile("img[0-9]{0,5}?\((?P<location>.*?)\)", re.IGNORECASE)
    mdimg = re.compile("\[(?P<name>.*?)\]\((?P<location>.*?)\)", re.IGNORECASE)
    atags = re.compile('<a href="(?P<location>.*?)">(?P<title>.*?)</a>', re.IGNORECASE)
    smalltags = re.compile('<small>', re.IGNORECASE)
    fontcolors = re.compile('<font color="(?P<color>.*?)">(?P<content>.*?)</font>', re.IGNORECASE)
    # Create a placeholder that we'll change
    final = content
    # Do inplace modifications for known tags with no information attached
    final = final.replace('~', '')
    final = final.replace('#', '')
    final = final.replace('<p>', '')
    final = final.replace('<hr>', '')
    final = final.replace('__', '***')
    final = final.replace('<br />', '\n')
    final = final.replace('<br>', '\n')
    final = final.replace('<br/>', '\n')
    final = final.replace('~!', '`')
    final = final.replace('!~', '`')
    # Create a list for these next functions
    final = final.split("\n")
    # Create a list from the current lines in final and find any line that starts with - and replace with • (For lists)
    iterable = final
    for num, line in enumerate(iterable):
        if line[0:1] == '-':
            temp = list(line)
            temp[0] = '•'
            final[num] = temp
    # Set iterable equal to the new version of Final and run our regex's against it
    iterable = final
    for num, line in enumerate(iterable):
        temp = line
        imgs = imgtag.findall(line)
        mds = mdimg.findall(line)
        links = atags.findall(line)
        smalls = smalltags.findall(line)
        fonts = fontcolors.findall(line)
        # Check to see if any matched, then replace
        if imgs:
            for matches in imgs:
                temp = temp.replace(matches[0], matches[1])
        if mds:
            for matches in mds:
                temp = temp.replace("[{0}]({1})".format(matches[0], matches[1]), matches[0] + ": " + matches[1])
        if links:
            for matches in links:
                temp = temp.replace('<a href="{0}">{1}</a>'.format(matches[0], matches[1]), matches[0] + ": " + matches[1])
        if smalls:
            for matches in smalls:
                temp = temp.replace("<small>", "*")
                if "</small>" in temp:
                    temp = temp.replace("</small>", "*")
                else:
                    temp += "*"
        if fonts:
            for matches in fonts:
                temp = temp.replace('<font color="{0}">{1}</font>'.format(matches[0], matches[1]), matches[1])
        final[num] = temp
    # We're done, return a string again
    return "\n".join(final)
