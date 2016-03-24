"""
Created on Nov 22, 2015

@author: nwilliams
"""


def BuildCommaSeparatedList(listOfStrings):
    listOfStrings = [st.strip() for st in listOfStrings]
    if not listOfStrings:
        return []
    if len(listOfStrings) > 1:
        last = listOfStrings.pop()
        returnString = ', '.join(listOfStrings).strip(', ')
        returnString += ' and %s' % last
    else:
        returnString = listOfStrings.pop()
    return returnString
