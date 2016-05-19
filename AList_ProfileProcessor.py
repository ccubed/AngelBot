import re


def profile_preprocessor(content):
    # Compile Regular Expressions
    imgtag = re.compile("img.*?\((?P<location>.*?)\)", re.IGNORECASE)
    mdimg = re.compile("\[.*?\]\((?P<location>.*?)\)", re.IGNORECASE)
    atags = re.compile('<a.*?>(?P<title>.*?)</a>', re.IGNORECASE)
    smalltags = re.compile('<small>', re.IGNORECASE)
    fontcolors = re.compile('<font.*?>(?P<content>.*?)</font>', re.IGNORECASE)
    breaks = re.compile('<br.*?>', re.IGNORECASE)
    blocks = re.compile('(~!|!~)', re.IGNORECASE)
    removes = re.compile('(~|#|<p>|<hr>)', re.IGNORECASE)
    # Create a placeholder that we'll change
    final = content
    # Do inplace modifications for known tags with no information attached
    final = final.replace('__', '***')
    final = breaks.sub('\n', final)
    final = blocks.sub('\`', final)
    final = removes.sub('', final)
    # Create a list for these next functions
    final = final.split("\n")
    # Create a list from the current lines in final and find any line that starts with - and replace with • (For lists)
    for num, line in enumerate(final):
        temp = line
        if temp[0:1] == '-':
            temp = list(line)
            temp[0] = '•'
            temp = ''.join(temp)
        imgs = imgtag.findall(temp)
        mds = mdimg.findall(temp)
        links = atags.findall(temp)
        smalls = smalltags.findall(temp)
        fonts = fontcolors.findall(temp)
        # Check to see if any matched, then replace
        if imgs:
            for matches in imgs:
                temp = temp.replace(matches[0], '<{0}>'.format(matches[1]))
        if mds:
            for matches in mds:
                temp = temp.replace("[{0}]({1})".format(matches[0], matches[1]), '<{0}>'.format(matches[1]))
        if links:
            for matches in links:
                temp = temp.replace('<a href="{0}">{1}</a>'.format(matches[0], matches[1]), '<{0}>'.format(matches[1]))
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
