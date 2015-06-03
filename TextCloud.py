# TextCloud.py

from hmc_urllib import getHTML
from visual import *

MAX_WORDS = 30
DEPTH = 2

def main():
    ''' Returns a text cloud from the given URL.
    '''
    
    url = input('Enter a URL:')
    print()
    listVisited = [url]
    listOfWords = getListOfWords(url,DEPTH,listVisited)
    listOfWordsNoPunctuation = removePunctuation(listOfWords)
    listOfWordsNoCommon = removeCommonWords(listOfWordsNoPunctuation)
    stemmedList = stemList(listOfWordsNoCommon)
    dictionary = createDictOfWordCounts(stemmedList)
    sortedList = sorted(dictionary.items(), key = lambda x: x[1],
                        reverse = True)
    print('Here is the dictonary of words on that page:')
    print(sortedList[:MAX_WORDS])
    print()
    windowSetup()
    displayCloud(sortedList[:MAX_WORDS])
    print('Here is the text cloud for your web page:')
    return printResults(sortedList)


def getListOfWords(url,DEPTH,listVisited):
    ''' Returns a list of words from the given url and from all urls on that
        page up to a certain page depth, DEPTH, that also don't appear in the
        list of already visited urls,listVisited.
    '''
    
    siteTuple = getHTML(url)
    listOfWords = siteTuple[0][1:-1].split()
    repeatURL = False
    for urlS in siteTuple[1]:
        if urlS in listVisited:
            repeatURL = True
        if DEPTH <= 0 and repeatURL == False:
            return listOfWords
        if repeatURL == False:
            listVisited = listVisited + [urlS]
            listOfWords += str(getListOfWords(urlS,DEPTH-1,listVisited)).split()
    return listOfWords


def removePunctuation(myList):
    """ Removes puctuation from the words in listOfWords.
    """
    ''' Testing:
        (test 1)
        >>>listOfWords = ['a!', 'b@', 'c#', 'd$', 'e^']
        >>> removePunctuation(listOfWords)
        ['a', 'b', 'c', 'd', 'e']

        (test 2)
        >>>listOfWords = ['a&', 'b*', 'c(', 'd)', 'e.']
        >>>removePunctuation(listOfWords)
        ['a', 'b', 'c', 'd', 'e']
    '''
    newList = []
    for word in myList:
        for punc in ".,`'\"~!@#$%^&*();:<>|\\/?}{][_+=-":
            word = str(word).replace(punc, '')
        if word != "":
            newList += [word]
    return newList



commonWords = 'like who when all now if have were which where then there its but so not their some me'
commonWords += 'my more what they this her for be him had has with was she you the and is that as by or'
commonWords += 'in of are to it to on 123456789 one two three four five six seven eight nine ten '
commonWords += 'these into out in them other from would been on yes no mrs ms do your am any'
def removeCommonWords(myList):
    ''' Removes common words such as 'a', 'the', and 'and' from listOfWords.
    '''
    ''' Testing:
        (test 1)
        >>>listOfWords = ['the', 'dog', 'and', 'cat', 'eat']
        >>>removeCommonWords(listOfWords)
        ['dog', 'cat', 'eat']

        (test 2)
        >>>listOfWords = ['a', 'bird', 'is', 'a', 'good', 'singer']
        >>>removeCommonWords(listOfWords)
        ['bird', 'good', 'singer']
    '''
    newList = []
    for word in myList:
        if word in commonWords:
                word = ''
        if word != '':
            newList += [word]               
    return newList


def stemList(myList):
    ''' Stems the words in listOfWords so that words are simplified down to
        their root (i.e. spamming -> spam).
    '''
    '''Testing:
        (test 1)
        >>>listOfWords = ['spamming', 'spammed', 'spammer']
        >>>stemList(listOfWords)
        ['spam', 'spam', 'spam']

        (test 2)
        >>>listOfWords = ['books', 'carries', 'bagged']
        >>>stemList(listOfWords)
        ['book', 'carry', 'bag']
    '''
    newList = []
    for word in myList:
        if word[-3:] == 'ies':
            word = word[:-3] + 'y'
        if word[-3:] == 'ied':
            word = word[:-3] + 'y'
        if word[-3:] == 'ous': 
            word = word[:3]           
        if word[-1] == 's' and word[-2] != 's' and len(word) > 3:
            word = word[:-1]
        if len(word) >= 4:    
            if word[-2:] == 'er' and word[-3] == word[-4]:
                word = word[:-3]
        if word[-2:] == 'ed' and len(word) >= 4:
            if word[-3] == word[-4]:
                word = word[:-3]
            else:
                word = word[:-1]
        if word[-4:] == 'ness':
            word = word[:-4]
        if word[-3:] == 'ize' and len(word) >= 4:
            if word[-4] == 't':
                word = word[:-3] + 'e'
            else:
                word = word[:-3]
        if word[-4:] == 'able':
            word = word[:-4]
        if word[-3:] == 'ion':
            word = word[:-3]+ 'e'
        if word[-3:] == 'ive':
            word = word[:-3]+ 'e'
        if word[-3:] == 'ish':
            word = word[:-3]
        if len(word) >= 5:
            if word[-3:] == 'ing' and word[-4] == word[-5]:
                word = word[:-4]
        if word[-4:] == 'ying':
            word = word[:-4]+ 'ie'
        if word[-4:] == 'ving':
            word = word[:-3]+'e'
        '''if len(word) >= 2:
            if word[-1] == word[-2]:
                word = word[:-1]'''                
        if word[-2:] == 'ly':
            word = word[:-2]
        if word[-4:] =='cing':
            word = word[:-3] + 'e'
            
        newList += [word]
    return newList
    
    
def createDictOfWordCounts(myList):
    """ Creates a sorted list of words containing the number of times each
        word appeared.
    """
    ''' Testing:
        (test 1)
        >>>listOfWords = ['dog', 'cat', 'bird', 'dog', 'dog', 'cat']
        >>>createDictOfWordCounts(listOfWords)
        {'bird': 1, 'dog': 3, 'cat': 2}

        (test 2)
        >>>listOfWords = ['book', 'book', 'book', 'book', 'sad', 'happy']
        >>>createDictOfWordCounts(listOfWords)
        {'happy': 1, 'book': 4, 'sad': 1}
    '''
    wordCounterDict = {}
    for word in myList:
        if word in wordCounterDict:
            wordCounterDict[word] += 1
        else:
            wordCounterDict[word] = 1
    return wordCounterDict


def printResults(sortedList):
    """ Prints each word in sortedList and the number of times it occurred.
        Prints at most MAX words.
    """
    '''Testing:
       (test 1)
       >>>dictionary = {'happy': 1, 'book': 4, 'sad': 1}
       >>>printResults(dictionary)
       book (4)
       sad (1)
       happy (1)

       (test 2)
       >>>dictionary = {'bird': 1, 'dog': 3, 'cat': 2}
       >>>printResults(dictionary)
       dog (3)
       cat (2)
       bird (1)
    '''
    for item in sortedList[:MAX_WORDS]:
        print(item[0], '(%s)' % item[1])
    return


def windowSetup():   
    """" Sets up the VPython window "scene"
         See http://www.vpython.org/webdoc/visual/display.html"""
    
    scene.autoscale = false        # Don't auto rescale
    scene.foreground = color.red
    scene.background = color.white
    scene.height = 1000            # height of graphic window in pixels
    scene.width = 1000             # width of graphic window in pixels
    scene.x = 100                  # x offset of upper left corner in pixels
    scene.y = 100                  # y offset of upper left corner in pixels
    scene.title = 'Text Cloud'


def displayCloud(sortedList):
    """ Displays on a VPython graphics window the text cloud in an 'X' shape
        Input: sortedList - a list of tuples with first item a common word
               and second item the count for that word.  Sorted from high
               to low on counts. """
    
    
    y = 5          # scene coordinates at top is 5
    x = -7
    maxHeight = 100 # max height of letter in pixels
    
    maxCount = sortedList[0][1]

    myLabels = []
    xDirection = False
    yDirection = False
    length = len(sortedList)
    stepSize = 10/length
    for w in range(length):

        # wordHeight is proportional to word's count
        wordHeight = sortedList[w][1]/maxCount * maxHeight

        myLabels += [ label(text = sortedList[w][0], pos = (x, y, 0),
                    color = (0 , 0.5, 0),
                    height = wordHeight, box = 0, border = 0, font = "times") ]

        if xDirection and yDirection:
            y = y + 1.5*(stepSize * (length - w)) 
            xDirection = False
        elif xDirection and not yDirection:
            x = x + 1.5*(stepSize * (length - w))   
            yDirection = True
        elif not xDirection and yDirection:
            x = x - 1.5*(stepSize * (length - w))  
            yDirection = False
        else:
            y = y - 1.5*(stepSize * (length - w)) 
            xDirection = True
