#coding:utf-8
import rarfile, zipfile, os, shutil
from tkinter import *                
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import tkinter.messagebox
import tkinter.filedialog
from interval import Interval


def selectPath():
    path_ = askdirectory()
    path.set(path_)

def selectFilePath():
    filepath_ = filedialog.askopenfilename()
    filepath.set(filepath_)

def selectFile():
    filename_ = filedialog.askopenfilename()
    filename.set(filename_)

def outputFlie():
    outputfile_ = askdirectory()
    outputfile.set(outputfile_)

def removeprefix(self: str, prefix: str, /) -> str:
    '''
    https://www.python.org/dev/peps/pep-0616/
    function: remove prefix
    input: file_path, prefix
    '''
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

def removesuffix(self: str, suffix: str, /) -> str:
    '''
    function: remove suffix
    input: file_path, suffix
    suffix='' should not call self[:-0].
    '''
    if suffix and self.endswith(suffix):
        return self[:-len(suffix)]
    else:
        return self[:]

def zip_file(file_path, save_path, compression, compresslevel):
    '''
    file_path: 
        file path you want zip.
    save_path: 
        path you want save.
    allowZip64: 
        If allowZip64 is True (the default) zipfile will create ZIP files that use the ZIP64 extensions when the zipfile is larger than 4 GiB. If it is false zipfile will raise an exception when the ZIP file would require ZIP64 extensions.
    compression:
        ZIP_STORED, 
        ZIP_LZMA, 
        ZIP_DEFLATED,
        ZIP_BZIP2
    compresslevel:
        ZIP_STORED: invalid
        ZIP_LZMA: invalid
        ZIP_DEFLATED: 0~9
        ZIP_BZIP2: 1~9
    '''
    abs_path = os.path.abspath(file_path)
    # print(abs_path)
    print('zip RUN !')

    if os.path.isdir(file_path):
        compress_file = zipfile.ZipFile('{}.zip'.format(abs_path), 'w', compression, compresslevel)
        for root, dirs, files in os.walk(abs_path):
            for file in files:
                compress_file.write(os.path.join(str(root), file), './' + root.replace(abs_path, '') + '/' + file)
        compress_file.close()

    elif os.path.isfile(file_path):
        file_suffix = '.' + abs_path.split('.')[-1]
        file_name = removesuffix(abs_path, file_suffix)
        print(file_name)
        compress_file = zipfile.ZipFile('{}.zip'.format(file_name), 'w', compression, compresslevel)
        print(abs_path)
        print(str('./' + abs_path.split('\\')[-1]))
        compress_file.write(abs_path, str('./' + abs_path.split('\\')[-1]))
        compress_file.close()

    else:
        # print("error! it's a special file.")
        pass

def zip_file_call():
    zip_level_set = 0
    zip_level_set = zip_level.get()
    zip_level_range = Interval(0, 9)
    try:
        if zip_level_set in zip_level_range:
            pass
        else:
            zip_level_set = 0
    except:
        zip_file_call_level_error()
        
    # print(zip_level_set)
    if os.path.isdir(path.get()) or os.path.isfile(filepath.get()):
        try:
            if zip_mode.get() == 'ZIP_DEFLATED':
                # print('mode: ZIP_DEFLATED')
                zip_file(path.get(), './', zipfile.ZIP_DEFLATED, zip_level_set)
                zip_file(filepath.get(), './', zipfile.ZIP_DEFLATED, zip_level_set)
            elif zip_mode.get() == 'ZIP_BZIP2':
                # print('mode: ZIP_BZIP2')
                zip_file(path.get(), './', zipfile.ZIP_BZIP2, zip_level_set)
                zip_file(filepath.get(), './', zipfile.ZIP_BZIP2, zip_level_set)
            elif zip_mode.get() == 'ZIP_STORED':
                # print('mode: ZIP_STORED')
                zip_file(path.get(), './', zipfile.ZIP_STORED, zip_level_set)
                zip_file(filepath.get(), './', zipfile.ZIP_STORED, zip_level_set)
            elif zip_mode.get() == 'ZIP_LZMA':
                # print('mode: ZIP_LZMA')
                zip_file(path.get(), './', zipfile.ZIP_LZMA, zip_level_set)
                zip_file(filepath.get(), './', zipfile.ZIP_LZMA, zip_level_set)
            else:
                pass
        except:
            pass
    else:
        zip_file_call_error()

def zip_file_call_error():
    tkinter.messagebox.askquestion(title='ERROR', message='压缩失败！')

def zip_file_call_level_error():
    tkinter.messagebox.askquestion(title='ERROR', message='压缩等級異常！')

def zip_read(file_path):
    '''
    zip
    '''
    compress_file = zipfile.ZipFile(file_path, 'r')
    print(compress_file.namelist())

def unzip_file(file_path, output_path, pwd):
    if zipfile.is_zipfile(filename.get()):
        compress_file = zipfile.ZipFile(file_path, 'r')
        if os.path.isdir(path.get()):
            compress_file.extractall(output_path)
        else:
            compress_file.extractall(os.path.split(file_path)[0] + '/')
    else:
        pass

def unzip_file_call():
    if zipfile.is_zipfile(filename.get()):
        unzip_file(filename.get(), outputfile.get(), '')
    else:
        unzip_file_call_error()

def unzip_file_call_error():
    tkinter.messagebox.askquestion(title='ERROR', message='解压失败！')

def generate_div_col_1x(row, col):
    div_size = 100
    pad = 5
    align_mode = 'nswe'
    div = tkinter.Frame(root,  width=div_size , height=div_size/10 , bg='orange').grid(column=col, row=row, padx=pad, pady=pad, sticky=align_mode)
    return div

def generate_div_col_2x(row, col):
    div_size = 200
    pad = 5
    align_mode = 'nswe'
    div = tkinter.Frame(root,  width=div_size*2 , height=div_size/10 , bg='blue').grid(column=col, row=row, columnspan=1, padx=pad, pady=pad, sticky=align_mode)
    return div

def main():
    root.title('EasyCompress')
    div_size = 200
    pad = 5
    align_mode = 'nswe'

    # root.columnconfigure(0, weight=1) 
    # root.columnconfigure(1, weight=1)
    # root.rowconfigure(0, weight=1) 
    # root.rowconfigure(1, weight=1)

    div1_1 = generate_div_col_2x(0,0)
    div1_1 = generate_div_col_1x(0,1)
    div2_1 = generate_div_col_2x(1,0)
    div2_1 = generate_div_col_1x(1,1)
    div3_1 = generate_div_col_2x(2,0)
    div3_1 = generate_div_col_1x(2,1)
    div4_1 = generate_div_col_2x(3,0)
    div4_1 = generate_div_col_1x(3,1)
    div5_1 = generate_div_col_2x(4,0)
    div5_1 = generate_div_col_1x(4,1)
    div6_1 = generate_div_col_2x(5,0)
    div6_1 = generate_div_col_1x(5,1)
    div7_1 = generate_div_col_2x(6,0)
    div7_1 = generate_div_col_1x(6,1)

    Entry(root, width=30, textvariable = path).grid(column=0, row=0, padx=pad, pady=pad, sticky=align_mode)
    Button(root, width=20,  text = "需要压缩的目录路径", command = selectPath).grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)

    Entry(root, width=30, textvariable = filepath).grid(row = 1, column = 0, padx=pad, pady=pad, sticky=align_mode)
    Button(root, width=20,  text = "需要压缩的文件路径", command = selectFilePath).grid(row = 1, column = 1, padx=pad, pady=pad, sticky=align_mode)

    Entry(root, width=30, textvariable = filename).grid(row = 2, column = 0, padx=pad, pady=pad, sticky=align_mode)
    Button(root, width=20, text = "需要解压的文件路径", command = selectFile).grid(row = 2, column = 1, padx=pad, pady=pad, sticky=align_mode)

    Entry(root, width=30, textvariable = outputfile).grid(row = 3, column = 0, padx=pad, pady=pad, sticky=align_mode)
    Button(root, width=20, text = "解压至", command = outputFlie).grid(row = 3, column = 1, padx=pad, pady=pad, sticky=align_mode)

    Label(root, width=20, text = "").grid(row = 4, column = 0, padx=pad, pady=pad, sticky=align_mode)
    Label(root, width=20, text = "").grid(row = 4, column = 1, padx=pad, pady=pad, sticky=align_mode)

    Label(root, width=20, text = "开启kid64").grid(row = 5, column = 0, sticky=align_mode)
    Button(root, width=20, text="压缩",command=zip_file_call).grid(row=5, column=1, padx=pad, pady=pad, sticky=align_mode)

    Label(root, width=20, text = "").grid(row = 6, column = 0, padx=pad, pady=pad, sticky=align_mode)
    Button(root, width=20, text="解压",command=unzip_file_call).grid(row=6, column=1, padx=pad, pady=pad, sticky=align_mode)

    div_menu_break = tkinter.Frame(root,  width=10 , height=div_size/10).grid(column=2, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_1 = tkinter.Frame(root,  width=50 , height=div_size/10, bg='blue').grid(column=3, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_2 = tkinter.Frame(root,  width=50 , height=div_size/10, bg='blue').grid(column=3, row=1, padx=pad, pady=pad, sticky=align_mode)
    div_menu_3 = tkinter.Frame(root,  width=50 , height=div_size/10, bg='blue').grid(column=3, row=2, padx=pad, pady=pad, sticky=align_mode)

    div_menu_stack_0 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=4, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_stack_1 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=5, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_stack_2 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=6, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_stack_3 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=7, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_stack_4 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=8, row=0, padx=pad, pady=pad, sticky=align_mode)
    div_menu_stack_5 = tkinter.Frame(root,  width=20 , height=div_size/10).grid(column=9, row=0, padx=pad, pady=pad, sticky=align_mode)


    div_menu_break = tkinter.Frame(root,  width=10 , height=div_size/10, bg='blue').grid(column=100, row=0, padx=pad, pady=pad, sticky=align_mode)

    zip_option = Radiobutton(root, text=".zip", variable= compress_mode, value='zip_mode', state=NORMAL).grid(column=3, row=0, padx=pad, pady=pad, sticky=align_mode)
    rar_option = Radiobutton(root, text=".rar", variable= compress_mode, value='rar_mode', state=NORMAL).grid(column=3, row=1, padx=pad, pady=pad, sticky=align_mode)
    sevz_option = Radiobutton(root, text=".7z", variable= compress_mode, value='sevenz_mode', state=NORMAL).grid(column=3, row=2, padx=pad, pady=pad, sticky=align_mode)



    # .zip choose
    Radiobutton(root, text="DEFLATED", variable= zip_mode, value='ZIP_DEFLATED', state=NORMAL).grid(column=4, row=0, padx=pad, pady=pad, sticky=align_mode)
    Radiobutton(root, text="BZIP2", variable= zip_mode, value='ZIP_BZIP2', state=NORMAL).grid(column=5, row=0, padx=pad, pady=pad, sticky=align_mode)
    Radiobutton(root, text="STORED", variable= zip_mode, value='ZIP_STORED', state=NORMAL).grid(column=6, row=0, padx=pad, pady=pad, sticky=align_mode)
    Radiobutton(root, text="LZMA", variable= zip_mode, value='ZIP_LZMA', state=NORMAL).grid(column=7, row=0, padx=pad*2, pady=pad, sticky=align_mode)
    Label(root, width=12, text = "压缩等级(0~9):").grid(column=8, row=0, pady=pad, sticky=align_mode)
    Entry(root, width=3, textvariable = zip_level).grid(column=9, row=0, pady=pad, sticky=align_mode)

    root.mainloop()

if __name__ == '__main__':
    '''
    pyinstaller -F -w main.py
    已实现功能:
        文件夹的zip压缩
        单个文件的zip压缩
        zip文件解压
        tk gui 界面
    '''
    print()

    root = Tk()              # 初始化
    path = StringVar()       # 显示路径名
    filepath = StringVar()
    filename = StringVar()   # 显示文件路径名
    outputfile = StringVar() # 显示解压后的文件路径名

    compress_mode =  StringVar()
    compress_mode.set('zip_mode')

    zip_mode = StringVar()
    zip_mode.set('ZIP_DEFLATED')

    zip_level = IntVar()
    zip_level.set(0)

    main()
    

