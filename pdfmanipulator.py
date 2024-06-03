from tkinter.filedialog import askopenfilenames,askopenfilename
from PyPDF2 import PdfReader, PdfWriter,PdfMerger
from tkinter.filedialog import asksaveasfilename
import tkinter as tk


def pdfSplitter(filename:str, pages:list[int]):
    reader = PdfReader(filename)
    writer = PdfWriter()

    try:
        for page_num, page in enumerate(reader.pages,1):
            if page_num in pages:
                writer.add_page(page)

        name = f"{filename.split('.')[0]}_splited.pdf".split('/')[-1]
        out_folder = asksaveasfilename(filetypes=[('pdf files','*.pdf')],initialfile=name)
        writer.write(out_folder)
        writer.close()

        msg = "successfully splitted"

    except:
        msg = "error while splitting"

    finally:
        return msg


def pdfMerger(files:list[str]|tuple[str]):
    merger = PdfMerger()
    for file in files:
        if file != '':
            merger.append(file)

    name = f"{files[0].split('.')[0]}_merged.pdf".split('/')[-1]
    out_folder = asksaveasfilename(filetypes=[('pdf files','*.pdf')],initialfile=name)

    merger.write(out_folder)
    merger.close()

root = tk.Tk()

def open_merge_win():
    master = tk.Toplevel(root)
    master.title("Merger window")

    def add_filename_text():
        files = list(askopenfilenames(filetypes=[('pdf files','*.pdf')]))
        if files is not None:
            opened_fileT.config(state='normal')
            opened_fileT.delete('1.0','end')
            filenames = ""
            for file in files:
                filenames += f'{file}\n'
            
            opened_fileT.insert('1.0',filenames)

    def merge():
        selected_files = opened_fileT.get('1.0','end').strip()

        if len(selected_files) != 0:
            files = selected_files.split("\n")
            print(files)

            try:
                pdfMerger(files)
                msg = "merged successfully"

            except Exception as e:
                msg = "merge was unsuccessfull"

            finally:
                msgT.config(state='normal')
                msgT.delete('1.0','end')
                msgT.insert('1.0',msg)
                msgT.config(state='disabled')

        else:
            msgT.config(state="normal")
            msgT.delete('1.0','end')
            msgT.insert('1.0',"no files selected")
            msgT.config(state='normal')


    open_fileL = tk.Label(master=master, text="Opened files:")
    open_fileL.grid(row=0,column=0,padx=10,pady=10)

    opened_fileT = tk.Text(master=master, state='disabled', height=7)
    opened_fileT.grid(row=1,column=0,padx=10, pady=10)

    open_fileB = tk.Button(master=master, text="Open files", command=add_filename_text)
    open_fileB.grid(row=2,column=0)

    merge_btn = tk.Button(master=master, text="Merge files",command=merge)
    merge_btn.grid(row=3,column=0,padx=10, pady=10)

    msgL = tk.Label(master=master, text="output message: ")
    msgL.grid(row=4, column=0,sticky="W",pady=10)

    msgT = tk.Text(master=master,state='disabled',width=70,height=2)
    msgT.grid(row=5, column=0,sticky="W")

    dummy = tk.Label(master=master)
    dummy.grid(row=6, column=0)


def open_split_win():
    master = tk.Toplevel(root)
    master.title("Splitter window")

    def add_filename_text():
        file = askopenfilename(filetypes=[('pdf files','*.pdf')]).strip()
        
        if len(file) != 0:
            selected_fileT.config(state='normal')
            selected_fileT.delete('1.0','end')
            selected_fileT.insert('1.0',file)
            selected_fileT.config(state='disabled')

    def split():
        filename = selected_fileT.get('1.0','end').strip()
        page_no = page_nosE.get().split(',')
        page_nos = []
        for i in page_no:
            if i.__contains__('-'):
                start, end = i.split('-')
                num_list = range(int(start), int(end)+1)
                page_nos.extend(num_list)
            else:
                page_nos.append(int(i))

        msg = pdfSplitter(filename, page_nos)
        msgT.config(state='normal')
        msgT.delete('1.0','end')
        msgT.insert('1.0', msg)
        msgT.config(state='disabled')


    dummy = tk.Label(master=master)
    dummy.grid(row=0,column=0)

    open_fileL = tk.Label(master=master, text="Opened file:")
    open_fileL.grid(row=1,column=0, sticky="W", padx=10)

    selected_fileT = tk.Text(master=master,height=3,width=70,state='disabled')
    selected_fileT.grid(row=2,column=0, sticky="W", padx=10)

    open_fileB = tk.Button(master=master, text="Open file",command=add_filename_text)
    open_fileB.grid(row=3, column=0, pady=10)

    dummy = tk.Label(master=master)
    dummy.grid(row=4,column=0)

    page_nosL = tk.Label(master=master, text="page no [seperate by comma(,) for range add values within (-) eg:1-10]:")
    page_nosL.grid(row=5)

    page_nosE = tk.Entry(master=master, width=50)
    page_nosE.grid(row=6)

    dummy = tk.Label(master=master)
    dummy.grid(row=7,column=0)

    split_btn = tk.Button(master=master, text="Split",command=split)
    split_btn.grid(row=8)

    dummy = tk.Label(master=master)
    dummy.grid(row=9,column=0)


    dummy = tk.Label(master=master)
    dummy.grid(row=10,column=0)

    msgL = tk.Label(master=master, text="output message: ")
    msgL.grid(row=11, column=0,sticky="W")

    msgT = tk.Text(master=master,state='disabled',width=70,height=1)
    msgT.grid(row=12, column=0,sticky="W")

    dummy = tk.Label(master=master)
    dummy.grid(row=13, column=0)


if __name__ == "__main__":
    
    root.geometry("400x400")
    root.config(background="white")
    root.title('PDF Manipulator')

    main_merge_btn = tk.Button(master=root, text="open Merger", command=open_merge_win)
    main_merge_btn.grid(row=1,column=0,pady=70,padx=0,ipadx=10,ipady=10)

    main_split_btn = tk.Button(master=root, text="open Splitter", command=open_split_win)
    main_split_btn.grid(row=2,column=0,pady=50,padx=125,ipadx=10,ipady=10)

    root.mainloop()


