# importing everything from tkinter
from tkinter import *
# importing ttk for styling widgets from tkinter
from tkinter import ttk
# importing filedialog from tkinter
from tkinter import filedialog as fd
# importing os module
import os

from miner import PDFMiner

class PDFViewer: 
    def __init__(self, master):
        self.path = None # path to pdf file
        self.fileisopen = None # boolean to check if file is open
        self.author = None # author of pdf file
        self.name = None # name of pdf file
        self.current_page = None # current page of pdf file
        self.numPages = None # number of pages in pdf file
        self.master = master # master window
        self.master.title("PDF Viewer") # title of window
        self.master.geometry("580x520+440+180") # dimensions of window
        self.master.resizable(width=0, height=0) # this line disable the resesizing of window
        self.master.iconbitmap("pdf.ico")
        self.menu = Menu(self.master) # creating menu
        self.master.config(menu=self.menu) # adding menu to window
        self.filemenu = Menu(self.menu)   # creating sub menu
        self.menu.add_cascade(label='File', menu=self.filemenu) # adding sub menu to menu
        self.filemenu.add_command(label='Open',command=self.open_file)
        self.filemenu.add_command(label='Exit',command=self.master.destroy)
        self.top_frame = ttk.Frame(self.master, width=580, height=460) # creating top frame
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky=(N, S))
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky=(E, W))
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)
        self.scrolly.config(command=self.output.yview)
        self.scrollx.config(command=self.output.xview)
        # loading the button icons
        self.uparrow_icon = PhotoImage(file='images/uparrow.png')
        self.downarrow_icon = PhotoImage(file='images/downarrow.png')
        # resizing the icons to fit on buttons
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        # creating an up button with an icon
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow , command=self.previous_page)
        # adding the button
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        # creating a down button with an icon
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        # adding the button
        self.downbutton.grid(row=0, column=3, pady=8)
        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        # adding the label
        self.page_label.grid(row=0, column=4, padx=5)

    # function for opening pdf files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the pdf file from the path
            filename = os.path.basename(self.path)
            # passing the path to PDFMiner 
            self.miner = PDFMiner(self.path)
            # getting data and numPages
            data, numPages = self.miner.get_metadata()
            # setting the current page to 0
            self.current_page = 0
            # checking if numPages exists
            if numPages:
                # getting the title
                self.name = data.get('title', filename[:-4])
                # getting the author
                self.author = data.get('author', None)
                self.numPages = numPages
                # setting fileopen to True
                self.fileisopen = True
                # calling the display_page() function
                self.display_page()
                # replacing the window title with the PDF document name
                self.master.title(self.name)

    # the function to display the page  
    def display_page(self):
        # checking if numPages is less than current_page and if current_page is less than
        # or equal to 0
        if 0 <= self.current_page < self.numPages:
            # getting the page using get_page() function from miner
            self.img_file = self.miner.get_page(self.current_page)
            # inserting the page image inside the Canvas
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            # the variable to be stringified
            self.stringified_current_page = self.current_page + 1
            # updating the page label with number of pages 
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.numPages)
            # creating a region for inserting the page inside the Canvas
            region = self.output.bbox(ALL)
            # making the region to be scrollable
            self.output.configure(scrollregion=region)   

    # function for displaying next page
    def next_page(self):
        # checking if file is open
        if self.fileisopen:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page <= self.numPages - 1:
                # updating the page with value 1
                self.current_page += 1
                # displaying the new page
                self.display_page()

    # function for displaying the previous page        
    def previous_page(self):
        # checking if fileisopen
        if self.fileisopen:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                # displaying the previous page
                self.display_page()

root = Tk()
app = PDFViewer(root)
root.mainloop()
