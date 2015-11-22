'''
Created on Nov 22, 2015

@author: nwilliams
'''

def BuildCommaSeperatedList(listOfStrings):
    listOfStrings = [stri.strip() for stri in listOfStrings]
    if len(listOfStrings) > 1:
        last = listOfStrings.pop()
        returnString = ', '.join(listOfStrings).strip(', ')
        returnString += ' and %s' % last
    else:
        returnString = listOfStrings.pop()
    return returnString