from tkinter import *
from PIL import Image, ImageTk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
import datetime as dt
from yfinance import *
import pandas as pd
from pandas_datareader import data as pdr

saved_tickers = [];
saved_tickers_cnt = dict();
saved_tickers_prices = dict();
choices = ['A-Z','Z-A','Last added','Best value'];
i = int();
counter = 1;
pdr_override();

def fja():
    bc.config(text='0/1', font=("Arial", 10, 'bold'));
    loading.config(text='Loading: ', font=("Arial", 10, 'bold'));
    return

def reset_tabstop(event):
    event.widget.configure(tabs=(event.width-8, "right"))
def add_ticker_f(e=None):
    global saved_tickers;
    global saved_tickers_cnt;
    global saved_tickers_prices;
    global counter;
    answer = simpledialog.askstring("Add a stock", "Ticker symbol:", parent=root);
    fja();
    if (answer != None):
        answer = answer.upper();
        try:
            stock = Ticker(answer);
            sector = stock.info['sector'];
        except:
            messagebox.showerror("Error", "This stock does not exist");
            bc.config(text='', font=("Arial", 10, 'bold'));
            loading.config(text='', font=("Arial", 10, 'bold'));
            return
        start = dt.datetime(2021,3,25)
        now = dt.datetime.now();
        df = pdr.get_data_yahoo(answer, start, now);
        currentClose = round(df["Adj Close"][-1], 2);
        currentClose2 = round(df["Open"][-1], 2);
        if (answer not in saved_tickers and answer != None):
            saved_tickers.append(answer);
            saved_tickers_cnt.update({answer: counter});
            counter+=1;
            tickers.config(state = NORMAL);
            tickers.insert(END, answer);
            saved_tickers_prices.update({answer: currentClose});
            if (currentClose - currentClose2) >= 0:
                tickers.insert('end', '\t' + str(currentClose) + '\n', 'green');
            else:
                tickers.insert('end', '\t' + str(currentClose) + '\n', 'red');
            tickers.config(state = DISABLED, fg = 'white');
        elif (answer in saved_tickers):
            messagebox.showerror("Error", "This ticker is already in the list");
        bc.config(text='', font=("Arial", 10, 'bold'));
        loading.config(text='', font=("Arial", 10, 'bold'));
def remove_ticker_f(e=None):
    global saved_tickers;
    answer = simpledialog.askstring("Remove a stock", "Ticker symbol:", parent=root);
    if (answer != None):
        answer = answer.upper();
        if (answer in saved_tickers):
            saved_tickers.remove(answer);
        elif (answer not in saved_tickers):
            messagebox.showerror("Error", "This ticker doesn't exist in the list");
def load_f(e=None):
    badOnes = [];
    f = filedialog.askopenfile(title='Open', mode='r', filetypes=[("Text Document","*.txt")])
    if f is None:
        return;
    txt = f.read();
    global saved_tickers
    global saved_tickers_cnt
    global saved_tickers_price
    global counter;
    counter = 1;
    saved_tickers = [];
    saved_tickers_cnt = dict();
    saved_tickers_cnt = dict();
    saved_tickers = txt.split('\n');
    if saved_tickers[-1] == '':
        saved_tickers = saved_tickers[:-1];
    f.close();
    saved_tickers = list(dict.fromkeys(saved_tickers));
    tickers.config(state = NORMAL);
    tickers.delete('1.0', END);
    tickers.config(state = DISABLED, fg = 'white');
    messagebox.showinfo(title = 'Info', message = 'The program is loading your list. Be patient.')
    for c in saved_tickers:
        z = 0;
        try:
            stock = Ticker(c);
            sector = stock.info['sector'];
        except:
            badOnes.append(c);
            z = 1;
        if z == 0:
            start = dt.datetime(2021,3,25)
            now = dt.datetime.now();
            df = pdr.get_data_yahoo(c, start, now);
            currentClose = round(df["Adj Close"][-1], 2);
            currentClose2 = round(df["Open"][-1], 2);
            saved_tickers_cnt.update({c: counter});
            counter+=1;
            tickers.config(state = NORMAL);
            tickers.insert(END, c);
            saved_tickers_prices.update({c: currentClose});
            if (currentClose - currentClose2) >= 0:
                tickers.insert('end', '\t' + str(currentClose) + '\n', 'green');
            else:
                tickers.insert('end', '\t' + str(currentClose) + '\n', 'red');
            tickers.config(state = DISABLED, fg = 'white');

    
def save_f(e=None):
    global saved_tickers
    text2save = '';
    for c in saved_tickers:
        text2save = text2save + c + '\n';
    files = [('Text Document', '*.txt'),
             ('All Files', '*.*')];
    f = filedialog.asksaveasfile(title='Save as', mode='w', filetypes = files, defaultextension = files)
    if f is None:
        return
    f.write(text2save)
    f.close()
    
def add_ticker_text_f1(e=None):
    c.itemconfig("add_ticker", fill="white");
    c.itemconfig("add_ticker_text", fill="black");
def add_ticker_text_f2(e=None):
    c.itemconfig("add_ticker", fill="#242121");
    c.itemconfig("add_ticker_text", fill="white");
def remove_ticker_text_f1(e=None):
    c.itemconfig("remove_ticker", fill="white");
    c.itemconfig("remove_ticker_text", fill="black");
def remove_ticker_text_f2(e=None):
    c.itemconfig("remove_ticker", fill="#242121");
    c.itemconfig("remove_ticker_text", fill="white");
def load_text_f1(e=None):
    c.itemconfig("load", fill="white");
    c.itemconfig("load_text", fill="black");
def load_text_f2(e=None):
    c.itemconfig("load", fill="#242121");
    c.itemconfig("load_text", fill="white");
def save_text_f1(e=None):
    c.itemconfig("save", fill="white");
    c.itemconfig("save_text", fill="black");
def save_text_f2(e=None):
    c.itemconfig("save", fill="#242121");
    c.itemconfig("save_text", fill="white");

root = Tk();
root.title('Stonxinator™ v1.0');
root.resizable(False, False);
photo = PhotoImage(file = "bin\\bg.png");
c = Canvas(root, height=480, width=1280);
c.create_image(1280/2+2, 480/2+1, image=photo);

tickers = Text(root,
                width=15,
                font=("Arial", 14, 'bold'),
                fg='white',
                background='#242121',
                relief=RIDGE,
                cursor="arrow");
add_ticker = c.create_rectangle(700, 20, 815, 60,
                           fill="#242121",
                           tags='add_ticker',
                           outline='white');
add_ticker_text = c.create_text(756, 40,
                      text='Add',
                      tags='add_ticker_text',
                      font=("Arial", 14, 'bold'),
                      fill='white');
remove_ticker = c.create_rectangle(700, 80, 815, 120,
                           fill="#242121",
                           tags='remove_ticker',
                           outline='white');
remove_ticker_text = c.create_text(758, 100,
                      text='Remove',
                      tags='remove_ticker_text',
                      font=("Arial", 14, 'bold'),
                      fill='white');
load = c.create_rectangle(700, 417, 815, 457,
                           fill="#242121",
                           tags='load',
                           outline='white');
load_text = c.create_text(757, 438,
                      text='Load',
                      tags='load_text',
                      font=("Arial", 14, 'bold'),
                      fill='white');
save = c.create_rectangle(700, 357, 815, 397,
                           fill="#242121",
                           tags='save',
                           outline='white');
save_text = c.create_text(757, 377,
                      text='Save',
                      tags='save_text',
                      font=("Arial", 14, 'bold'),
                      fill='white');
sort_text = c.create_text(723, 303,
                      text='Sort by:',
                      tags='sort_text',
                      font=("Arial", 10, 'bold'),
                      fill='white');
loading = Label(c);
loading.place(x=443, y=460);
loading.config(background = 'black', foreground = 'white');
bc = Label(c);
bc.place(x=520, y=460);
bc.config(background = 'black', foreground = 'white');
bc.config(text='', font=("Arial", 10, 'bold'));
loading.config(text='', font=("Arial", 10, 'bold'));


tickers_window = c.create_window(446, 20, width = 225, height = 440, anchor='nw', window=tickers);
tickers.config(state=DISABLED)
gr1 = c.create_rectangle(420, 0, 426, 480, fill="white");
gr2 = c.create_rectangle(843, 0, 849, 480, fill="white");
tickers.tag_config("green", foreground="lawn green")
tickers.tag_config("red", foreground="red")

c.tag_bind(add_ticker, '<Button-1>', add_ticker_f);
c.tag_bind(add_ticker_text, '<Button-1>', add_ticker_f);
c.tag_bind(add_ticker, '<Enter>', add_ticker_text_f1);
c.tag_bind(add_ticker, '<Leave>', add_ticker_text_f2);
c.tag_bind(add_ticker_text, '<Enter>', add_ticker_text_f1);
c.tag_bind(add_ticker_text, '<Leave>', add_ticker_text_f2);
c.tag_bind(remove_ticker, '<Button-1>', remove_ticker_f);
c.tag_bind(remove_ticker_text, '<Button-1>', remove_ticker_f);
c.tag_bind(remove_ticker, '<Enter>', remove_ticker_text_f1);
c.tag_bind(remove_ticker, '<Leave>', remove_ticker_text_f2);
c.tag_bind(remove_ticker_text, '<Enter>', remove_ticker_text_f1);
c.tag_bind(remove_ticker_text, '<Leave>', remove_ticker_text_f2);
c.tag_bind(load, '<Button-1>', load_f);
c.tag_bind(load_text, '<Button-1>', load_f);
c.tag_bind(load, '<Enter>', load_text_f1);
c.tag_bind(load, '<Leave>', load_text_f2);
c.tag_bind(load_text, '<Enter>', load_text_f1);
c.tag_bind(load_text, '<Leave>', load_text_f2);
c.tag_bind(save, '<Button-1>', save_f);
c.tag_bind(save_text, '<Button-1>', save_f);
c.tag_bind(save, '<Enter>', save_text_f1);
c.tag_bind(save, '<Leave>', save_text_f2);
c.tag_bind(save_text, '<Enter>', save_text_f1);
c.tag_bind(save_text, '<Leave>', save_text_f2);
tickers.bind("<Configure>", reset_tabstop)

combostyle = Style();
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#242121',
                                       'fieldbackground': '#242121',
                                       'background': 'white',
                                       'foregroundcolor': 'white'
                                       }}})
combostyle.theme_use('combostyle')
varsa = StringVar(root);
w = Combobox(root, values = choices, textvariable = varsa);
w['state'] = 'readonly';
win = c.create_window(758, 328, width = 119, window=w);

c.pack();
root.withdraw()
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.deiconify()
root.mainloop();
