'''
Created on Nov 21, 2015

@author: nwilliams
'''

from django.shortcuts import render

def index(request):
    return render(request,'client/index.html')
    