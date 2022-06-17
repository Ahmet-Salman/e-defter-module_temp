import tkinter as tk
import tkinter.font as tkFont
# from lxml import etree as ET
import xml.etree.ElementTree as ET
import pandas as pd
import win32com.client as win32ComClient
import os
import time
import json
# from xbrl import XBRLParser
from tkinter import *
from pathlib import PurePosixPath, Path
from tkinter import filedialog as fd
from e_defter_clean_xbrl import clean_xbrl

class App:
    def __init__(self, root):
        #setting title
        root.title("E-Defter Module")
        #setting window size
        width=864
        height=569
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # ====================================
        # =========== START OF UI ============
        # P.S You should not need to change
        # These parts, so you can skip them
        # =========== START OF UI =============
        # =====================================

        # This is for the Lines =======================
        canvas=Canvas(root, width=864, height=569)
    
        # This is for Covered Date
        canvas.create_line(54, 45, 54, 110, fill="black", width=1)
        canvas.create_line(55, 79, 65, 79, fill="black", width=1)
        canvas.create_line(55, 109, 65, 109, fill="black", width=1)

        # This is for Fiscal Year
        canvas.create_line(277, 45, 277, 110, fill="black", width=1)
        canvas.create_line(277, 79, 283, 79, fill="black", width=1)
        canvas.create_line(277, 109, 283, 109, fill="black", width=1)

        # This is for Accountant
        canvas.create_line(470, 45, 470, 110, fill="black", width=1)
        canvas.create_line(470, 79, 476, 79, fill="black", width=1)
        canvas.create_line(470, 109, 476, 109, fill="black", width=1)

        # This is for Entry
        canvas.create_line(672, 45, 672, 110, fill="black", width=1)
        canvas.create_line(672, 79, 680, 79, fill="black", width=1)
        canvas.create_line(672, 109, 680, 109, fill="black", width=1)

        # This is for Line
        canvas.create_line(278, 180, 278, 240, fill="black", width=1)
        canvas.create_line(278, 210, 284, 210, fill="black", width=1)
        canvas.create_line(278, 240, 284, 240, fill="black", width=1)

        # This is for Document
        canvas.create_line(470, 170, 470, 331, fill="black", width=1)
        canvas.create_line(470, 331, 478, 331, fill="black", width=1)
        canvas.create_line(470, 301, 478, 301, fill="black", width=1)
        canvas.create_line(470, 271, 478, 271, fill="black", width=1)
        canvas.create_line(470, 241, 478, 241, fill="black", width=1)
        canvas.create_line(470, 211, 478, 211, fill="black", width=1)
        canvas.pack()

        # This is for Batch
        canvas.create_line(675, 180, 675, 240, fill="black", width=1)
        canvas.create_line(675, 210, 682, 210, fill="black", width=1)
        canvas.create_line(675, 240, 682, 240, fill="black", width=1)

        # END of Lines ====================

        self.coveredDate_var = tk.IntVar()
        self.coveredDate_start_var = tk.IntVar()
        self.coveredDate_end_var = tk.IntVar()
        ft = tkFont.Font(family='Times',size=10)

        listOfAllChildren = []
        listOfAllChildren_var = []

        coveredDateChildren = [self.coveredDate_start_var, self.coveredDate_end_var]
        self.coveredDate=tk.Checkbutton(root, variable=self.coveredDate_var, font=ft, fg="#000000", 
        justify="center", text="Period Covered", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.coveredDate_var, coveredDateChildren, True))
        self.coveredDate.place(x=30,y=40,width=130,height=15)

        self.coveredDate_start=tk.Checkbutton(root, variable=self.coveredDate_start_var, font=ft, fg="#000000", 
        justify="center", text="Period Covered Start", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.coveredDate_var, [self.coveredDate_start_var], False))
        self.coveredDate_start.place(x=60,y=70,width=130,height=20)
        
        self.coveredDate_end=tk.Checkbutton(root, variable=self.coveredDate_end_var, font=ft, fg="#000000", 
        justify="center", text="Period Covered End", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.coveredDate_var, [self.coveredDate_end_var], False))
        self.coveredDate_end.place(x=60,y=100,width=130,height=20)

        self.fiscalYear_var = tk.IntVar()
        self.fiscalYear_start_var = tk.IntVar()
        self.fiscalYear_end_var = tk.IntVar()

        fiscalYearChildren = [self.fiscalYear_start_var, self.fiscalYear_end_var]
        self.fiscalYear=tk.Checkbutton(root, variable=self.fiscalYear_var, font=ft, fg="#000000", 
        justify="center", text="Fiscal Year", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.fiscalYear_var, fiscalYearChildren, True))
        self.fiscalYear.place(x=245,y=40,width=130,height=20)

        self.fiscalYear_start=tk.Checkbutton(root, variable=self.fiscalYear_start_var, font=ft, fg="#000000", 
        justify="center", text="Fiscal Year Start", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.fiscalYear_var, [self.fiscalYear_start_var], False))
        self.fiscalYear_start.place(x=285,y=70,width=120,height=20)
        
        self.fiscalYear_end=tk.Checkbutton(root, variable=self.fiscalYear_end_var, font=ft, fg="#000000", 
        justify="center", text="Fiscal Year End", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.fiscalYear_var, [self.fiscalYear_end_var], False))
        self.fiscalYear_end.place(x=285,y=100,width=120,height=20)

        self.accountant_var = tk.IntVar()
        self.accountant_name_var = tk.IntVar()
        self.accountant_type_desc_var = tk.IntVar()
        accountantChildren = [self.accountant_name_var, self.accountant_type_desc_var]
        self.accountant=tk.Checkbutton(root, variable=self.accountant_var, font=ft, fg="#000000", 
        justify="center", text="Accountant", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.accountant_var, accountantChildren, True))
        self.accountant.place(x=440,y=40,width=130,height=20)

        self.accountant_name=tk.Checkbutton(root, variable=self.accountant_name_var, font=ft, fg="#000000", 
        justify="center", text="Accountant Name", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.accountant_var, [self.accountant_name_var], False))
        self.accountant_name.place(x=480,y=70,width=117,height=20)

        self.accountant_type_desc=tk.Checkbutton(root, variable=self.accountant_type_desc_var, font=ft, fg="#000000", 
        justify="center", text="Accountant Description", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.accountant_var, [self.accountant_type_desc_var], False))
        self.accountant_type_desc.place(x=480,y=100,width=150,height=20)

        self.entry_var = tk.IntVar()
        self.entries_comment_var = tk.IntVar()
        self.entry_number_var = tk.IntVar()
        entryChildren = [self.entries_comment_var, self.entry_number_var]
        self.entry=tk.Checkbutton(root, variable=self.entry_var, font=ft, fg="#000000", 
        justify="center", text="Entries", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.entry_var, entryChildren, True))
        self.entry.place(x=630,y=40,width=130,height=20)
        
        self.entries_comment=tk.Checkbutton(root, variable=self.entries_comment_var, font=ft, fg="#000000", 
        justify="center", text="Entries Comment", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.entry_var, [self.entries_comment_var], False))
        self.entries_comment.place(x=680,y=70,width=117,height=20)

        self.entry_number=tk.Checkbutton(root, variable=self.entry_number_var, font=ft, fg="#000000", 
        justify="center", text="Entry Number", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.entry_var, [self.entry_number_var], False))
        self.entry_number.place(x=680,y=100,width=110,height=20)

        self.organizationIdentifier_var = tk.IntVar()
        self.organizationIdentifier=tk.Checkbutton(root, variable=self.organizationIdentifier_var, font=ft, fg="#000000", 
        justify="center", text="Organization Identifier", offvalue="0", onvalue="1",
        command=lambda: self.checkboxPressed( self.organizationIdentifier_var))
        self.organizationIdentifier.place(x=30,y=170,width=172,height=20)

        self.businessDescription_var = tk.IntVar()
        self.businessDescription=tk.Checkbutton(root, variable=self.businessDescription_var, font=ft, fg="#000000", 
        justify="center", text="Business Description", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed( self.businessDescription_var))
        self.businessDescription.place(x=30,y=210,width=165,height=20)

        self.entryNumberCounter_var = tk.IntVar()
        self.entryNumberCounter=tk.Checkbutton(root, variable=self.entryNumberCounter_var, font=ft, fg="#000000", 
        justify="center", text="Entry Number Counter", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed( self.entryNumberCounter_var))
        self.entryNumberCounter.place(x=30,y=250,width=170,height=20)

        self.uniqueID_var = tk.IntVar()
        self.uniqueID=tk.Checkbutton(root, variable=self.uniqueID_var, font=ft, fg="#000000", 
        justify="center", text="Unique ID", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed(self.uniqueID_var))
        self.uniqueID.place(x=30,y=290,width=105,height=20)        

        self.postingDate_var = tk.IntVar()
        self.postingDate=tk.Checkbutton(root, variable=self.postingDate_var, font=ft, fg="#000000", 
        justify="center", text="Posting Date", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed( self.postingDate_var))
        self.postingDate.place(x=30,y=330,width=120,height=20)

        self.EnteredBy_var = tk.IntVar()
        self.EnteredBy=tk.Checkbutton(root, variable=self.EnteredBy_var, font=ft, fg="#000000", 
        justify="center", text="Entered By", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.EnteredBy_var], False))
        self.EnteredBy.place(x=30,y=370,width=110,height=20)

        self.creationDate_var = tk.IntVar()
        self.creationDate=tk.Checkbutton(root, variable=self.creationDate_var, font=ft, fg="#000000", 
        justify="center", text="Creation Date", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed( self.creationDate_var))
        self.creationDate.place(x=30,y=410,width=123,height=20)

        self.enteredDate_var = tk.IntVar()
        self.enteredDate=tk.Checkbutton(root, variable=self.enteredDate_var, font=ft, fg="#000000", 
        justify="center", text="Entered Date", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed(self.enteredDate_var))
        self.enteredDate.place(x=30,y=450,width=120,height=20)

        self.sourceApplication_var = tk.IntVar()
        self.sourceApplication=tk.Checkbutton(root, variable=self.sourceApplication_var, font=ft, fg="#000000", 
        justify="center", text="Source Application", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed(self.sourceApplication_var))
        self.sourceApplication.place(x=30,y=490,width=152,height=20)

        self.paymentMethod_var = tk.IntVar()
        self.paymentMethod=tk.Checkbutton(root, variable=self.paymentMethod_var, font=ft, fg="#000000", 
        justify="center", text="Payment Method", offvalue="0", onvalue="1", 
        command=lambda: self.checkboxPressed(self.paymentMethod_var))
        self.paymentMethod.place(x=30,y=530,width=140,height=20)

        self.line_var = tk.IntVar()
        self.line_number_var = tk.IntVar()
        self.line_counter_var = tk.IntVar()
        lineChidlren = [self.line_number_var, self.line_counter_var]
        ft = tkFont.Font(family='Times',size=10)
        self.line=tk.Checkbutton(root, variable=self.line_var, font=ft, fg="#000000", 
        justify="center", text="Line", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.line_var, lineChidlren, True))
        self.line.place(x=240,y=170,width=110,height=20)
        
        self.line_number=tk.Checkbutton(root, variable=self.line_number_var, font=ft, fg="#000000", 
        justify="center", text="Line Number", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.line_var, [self.line_number_var], False))
        self.line_number.place(x=285,y=200,width=110,height=20)

        self.line_counter=tk.Checkbutton(root, variable=self.line_counter_var, font=ft, fg="#000000", 
        justify="center", text="Line Counter", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.line_var, [self.line_counter_var], False))
        self.line_counter.place(x=285,y=230,width=117,height=20)

        self.document_var = tk.IntVar()
        self.documentReference_var = tk.IntVar()
        self.documentType_var = tk.IntVar()
        self.documentTypeDescription_var = tk.IntVar()
        self.documentNumber_var = tk.IntVar()
        self.documentDate_var = tk.IntVar()
        documentChildren = [self.documentReference_var, self.documentType_var, self.documentTypeDescription_var, self.documentNumber_var, self.documentDate_var]
        self.document=tk.Checkbutton(root, variable=self.document_var, font=ft, fg="#000000", 
        justify="center", text="Document", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, documentChildren, True))
        self.document.place(x=440,y=170,width=117,height=20)

        self.documentReference_var = tk.IntVar()
        self.documentReference=tk.Checkbutton(root, variable=self.documentReference_var, font=ft, fg="#000000", 
        justify="center", text="Document Reference", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.documentReference_var], False))
        self.documentReference.place(x=485,y=200,width=140,height=20)
        
        self.documentType=tk.Checkbutton(root, variable=self.documentType_var, font=ft, fg="#000000", 
        justify="center", text="Document Type", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.documentType_var], False))
        self.documentType.place(x=485,y=230,width=115,height=20)
        
        self.documentTypeDescription=tk.Checkbutton(root, variable=self.documentTypeDescription_var, font=ft, fg="#000000", 
        justify="center", text="Document Type Description", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.documentTypeDescription_var], False))
        self.documentTypeDescription.place(x=485,y=260,width=182,height=20)
        
        self.documentNumber=tk.Checkbutton(root, variable=self.documentNumber_var, font=ft, fg="#000000", 
        justify="center", text="Document Number", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.documentNumber_var], False))
        self.documentNumber.place(x=485,y=290,width=132,height=20)

        self.documentDate=tk.Checkbutton(root, variable=self.documentDate_var, font=ft, fg="#000000", 
        justify="center", text="Document Date", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.document_var, [self.documentDate_var], False))
        self.documentDate.place(x=485,y=320,width=115,height=20)

        self.batch_var = tk.IntVar()
        self.batch_ID_var = tk.IntVar()
        self.batch_desc_var = tk.IntVar()
        batchChidlren = [self.batch_ID_var, self.batch_desc_var]
        ft = tkFont.Font(family='Times',size=10)
        self.batch=tk.Checkbutton(root, variable=self.batch_var, font=ft, fg="#000000", 
        justify="center", text="Batch", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.batch_var, batchChidlren, True))
        self.batch.place(x=640,y=170,width=110,height=20)
        
        self.batch_ID=tk.Checkbutton(root, variable=self.batch_ID_var, font=ft, fg="#000000", 
        justify="center", text="Batch ID", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.batch_var, [self.batch_ID_var], False))
        self.batch_ID.place(x=685,y=200,width=68,height=20)

        self.batch_desc=tk.Checkbutton(root, variable=self.batch_desc_var, font=ft, fg="#000000", 
        justify="center", text="Batch Description", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.batch_var, [self.batch_desc_var], False))
        self.batch_desc.place(x=685,y=230,width=117,height=20)

        self.text = Text(root, state='disabled', width=40, height=5, wrap=WORD)
        self.text.place(x = 450, y = 390)

        self.selectAll_var = tk.IntVar()
        ft = tkFont.Font(family='Times',size=16)
        self.selectAll=tk.Checkbutton(root, variable=self.selectAll_var, font=ft, fg="#000000", 
        justify="center", text="Select All", offvalue="0", onvalue="1", 
        command=lambda: self.parentPressed(self.selectAll_var, listOfAllChildren_var, True))
        self.selectAll.place(x=260,y=510,width=130,height=20)

        selectFile_button = Button(root, text = "Choose File", command=self.selectFile).place(x = 530, y = 480)
        ok_button = Button(root, text = "OK", command=lambda: self.okButtonCommand(listOfAllChildren)).place(x = 670, y = 480)

        listOfAllChildren.append((self.organizationIdentifier_var, 1, 'organizationIdentifier'))
        listOfAllChildren.append((self.businessDescription_var, 2, 'businessDescription'))
        listOfAllChildren.append((self.fiscalYear_start_var, 3, 'fiscalYearStart'))
        listOfAllChildren.append((self.fiscalYear_end_var, 4, 'fiscalYearEnd'))
        listOfAllChildren.append((self.accountant_name_var, 5, 'accountantName'))
        listOfAllChildren.append((self.accountant_type_desc_var, 6, 'accountantEngagementTypeDescription'))
        listOfAllChildren.append((self.batch_ID_var, 7, 'batchID'))
        listOfAllChildren.append((self.batch_desc_var, 8, 'batchDescription'))
        listOfAllChildren.append((self.uniqueID_var, 9, 'uniqueID'))
        listOfAllChildren.append((self.creationDate_var, 10, 'creationDate'))
        listOfAllChildren.append((self.entries_comment_var, 11, 'entriesComment'))
        listOfAllChildren.append((self.coveredDate_start_var, 12, 'periodCoveredStart')) # The 1 here is column number in the cleaned version of the XML)
        listOfAllChildren.append((self.coveredDate_end_var, 13, 'periodCoveredEnd'))
        listOfAllChildren.append((self.sourceApplication_var, 14, 'sourceApplication'))
        listOfAllChildren.append((self.EnteredBy_var, 15, 'EnteredBy'))
        listOfAllChildren.append((self.enteredDate_var, 16, 'enteredDate'))
        listOfAllChildren.append((self.entry_number_var, 17, 'entryNumber'))
        listOfAllChildren.append((self.documentType_var, 18, 'documentType'))
        listOfAllChildren.append((self.entryNumberCounter_var, 19, 'entryNumberCounter'))
        listOfAllChildren.append((self.line_number_var, 20, 'lineNumber'))
        listOfAllChildren.append((self.line_counter_var, 21, 'lineNumberCounter'))
        listOfAllChildren.append((self.postingDate_var, 22, 'postingDate'))
        listOfAllChildren.append((self.documentReference_var, 23, 'documentReference'))
        listOfAllChildren.append((self.documentTypeDescription_var, 24, 'documentTypeDescription'))
        listOfAllChildren.append((self.documentNumber_var, 25, 'documentNumber'))
        listOfAllChildren.append((self.documentDate_var, 26, 'documentDate'))
        listOfAllChildren.append((self.paymentMethod_var, 27, 'paymentMethod'))

        # ====================================
        # =========== END OF UI ============
        # P.S Check the comments below to 
        # see what variables you are available
        # =========== END OF UI =============
        # =====================================

        ''' 
            There is the list called listOfAllChildren, it contains 21 tuples
            representing the 21 columns, each of the tuple has the format of
            (checkBox varibale, column number, name of column )
            checkBox variable: it is used to read/write the value of the check box
            column number: the order of the column after the XML is cleaned
            name of the column: The EXACT name of the field as it appears in the .XML file
        '''

        ''' 
            The other variable is listOfAllChildren_var, it contains only the 
            check box variables used to access the checkboxes, this is only
            used for the selectAll button above
        '''

        listOfAllChildren_var = [(child[0]) for child in listOfAllChildren]
        
        self.file = None # this will store the file that will be imported
        self.fileCounter = 1
        self.fileList = []

    def parentPressed(self, parentVar, children, isParent):
        if ((parentVar.get() == 1) and (isParent == True)):
            for child in children:
                child.set(1)
        for child in children:
            if child.get() == 0:
                parentVar.set(0)
                self.selectAll_var.set(0)
        
    def checkboxPressed(self, varName):
        if varName.get() == 0:
            self.selectAll_var.set(0)

    def selectFile(self):
        filetypes = (
            ('XML files', '*.xml'),
        )
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='D:\Bilkent Uni\MED_IDEA Internship\e-defter Module\Code\Sample Data',
            filetypes=filetypes
        )
        self.file = filename
        self.fileList.append(filename)
        self.text.configure(state='normal')
        if filename != "":
            self.text.insert('end', str(self.fileCounter) + "- " + PurePosixPath(filename).name + "\n")
            self.fileCounter += 1
        self.text.configure(state='disabled')    

    def okButtonCommand(self, childrenList):
        listOfChosenColumns = [child[2] for child in childrenList if child[0].get() == 1]
        listOfNotChosenIndices = [child[2] for child in childrenList if child[0].get() == 0]
        print(listOfNotChosenIndices)
        # listOfAllColumns = [child[2] for child in childrenList]
        # listOfNotChosenColumns = [x for x in listOfAllColumns if x not in listOfChosenColumns]
        # st = time.time()
        # clean_xbrl('7420300220-202001-Y-000001.xml')
        with open('entries.json', encoding='utf-8') as fh:
            data = json.load(fh)
            df = pd.DataFrame(data)
            # takes a list of columnNames to remove
            # df.drop(df.columns[listOfNotChosenIndices], axis = 1, inplace = True)
            
            df.drop(['uniqueID'], axis = 1, inplace = True)
            print(df)
            
            # df1 = df[~df.index.isin(1, 2)]
            # print(df.iloc[1])
            return
        #     # for element in data:
        #     #     for field in listOfNotChosenColumns:
        #     #         del element[field]

        # #         # print(element)
        # et = time.time()
        # # # get the execution time
        # elapsed_time = et - st
        # print('Time Elapsed', elapsed_time)
        # return
        # # print(data[0])
        # xml = dict2xml(data)
        # print(xml)
        # xmlfile = open("filteredData.xml", "w")
        # xmlfile.write(xml)
        # xmlfile.close()
        # return
        # self.fileList = ['D:/Bilkent Uni/MED_IDEA Internship/e-defter Module/Code/Sample Data/7420300220-202001-Y-000001.xml']
        for filePath in self.fileList:
            st = time.time()
            # clean_xbrl(filePath)
            
            # for i in data:
            #     # do nothing
            #     pass
            
            
            # return
            
            filteredData = self.xmlToDataFrame(filePath, listOfChosenColumns)
            et = time.time()
            # get the execution time
            elapsed_time = et - st
            print('Time Elapsed', elapsed_time)
            # conversion of the DataFrame to a cleaned/filtered XML
            fileName = Path(filePath).stem
            fileName_clean = fileName + 'clean.xml'
            filteredData.to_xml(fileName_clean, index = False)
            filePath_clean = os.getcwd() + '\\' + fileName_clean
            print('Starting Importing')
            self.importXMLToIdea(filePath = filePath_clean, fileName = fileName)
            print('Finished Importing')
            
        root.destroy()

    def xmlToDataFrame (self, filePath, listOfChosenColumns):
        tree = ET.parse(filePath)
        root = tree.getroot()
        limit = 5
        counter = 0
        filteredData = pd.DataFrame()
        isThereNone = True
        dataRow = {column : None for column in listOfChosenColumns}
        print ('Started Parsing')
        st = time.time()
        for child in root.iter():
            if limit == counter:
                break
            filteredChildtag = child.tag.split('}', 1)[1]

            # entryDetail indicates the beginning of a new record
            # isThereNone makes sure that no values in the dictionary are None
            # i.e. ensures all the fields are populated
            if (filteredChildtag == "entryDetail") and not isThereNone:
                # we have the data row here, we need to append it to a DataFrame
                filteredData = filteredData.append(dataRow, ignore_index=True)
                # counter += 1 # this counter is for testing purposes, it limits the number of rows in the DF
            if filteredChildtag in listOfChosenColumns:
                dataRow[filteredChildtag] = child.text
                isThereNone = not all(dataRow.values()) # returns false if not elements are None, returns true if there is 1 or more None values
        print ('Finished Parsing')
        et = time.time()
        # get the execution time
        elapsed_time = et - st
        print('Time Elapsed', elapsed_time)
        return filteredData
    
    # filePath is the path to the XML file that holds the cleaned/filtered data
    # fileName is the name you want to be given to the new .IMD DB
    def importXMLToIdea (self, filePath = None, fileName = None):
        try:
            idea = win32ComClient.Dispatch(dispatch="Idea.IdeaClient")
            task = idea.GetImportTask ("ImportXML")
            task.InputFileName = filePath
            task.OutputFileName = fileName
            projectFolder = idea.WorkingDirectory
            self.deleteIfExists(projectFolder + '\\' + fileName + '.IMD')
            task.PerformTask()

            # delete the temp cleaned XML file
            os.remove(filePath)
        finally:
            task = None
            db = None
            idea = None

    def deleteIfExists (self, path = None):
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

