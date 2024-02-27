    # -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:31:16 2023

@author: sebas
"""

from PyPDF2 import PdfMerger
import glob

path = r'C:\Users\sebas\Documents\Scripts\PDF_Resources'

#Create an instance of PdfFileMerger() class
merger = PdfMerger()

#Create a list with the file paths
pdf_files = glob.glob(path + '/Files/Julio2**/*.pdf')

#Iterate over the list of the file paths
for pdf_file in pdf_files:
    #Append PDF files
    merger.append(pdf_file)

#Write out the merged PDF file
indice = len(glob.glob(path + '/Results**/*.pdf'))

merger.write(path + f'/Results/Merge_{indice}.pdf')
merger.close()