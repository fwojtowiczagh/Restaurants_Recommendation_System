#!/usr/bin/python
# -*- coding: utf-8 -*-
from projekt import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import numpy as np
import random

all_rest_rec_p = recommendation_system.get_best_restaurants(15)
all_rest_rec = recommendation_system.objects_to_replace(all_rest_rec_p)

root = Tk()
root.title('GUI')
root.geometry('850x440')


notebook = ttk.Notebook(root)
tab_1 = Frame(notebook, background='light goldenrod')
tab_2 = Frame(notebook, background='light goldenrod')

notebook.add(tab_1, text='Rekomendacje')
notebook.add(tab_2, text='Wszystkie warianty')
notebook.pack(fill='both', expand=True)


# Funkcje:
def new_rec(selected, topsis, m_1, m_2, m_3, m_4, m_5, m_6, top_1, top_2, top_3):
    global all_rest_rec
    rest = topsis[int(selected)]
    recommendation_system.add_recommendation(0, rest, m_1.get(), m_2.get(), m_3.get(), m_4.get(), m_5.get(), m_6.get())
    recommendation_system.upload_restaurants_marks()
    recommendation_system.upload_own_recommendations()
    new_all_rest_rec = recommendation_system.get_best_restaurants(15)
    final = recommendation_system.objects_to_replace(new_all_rest_rec)
    all_rest_rec = final
    for record_1 in my_tree.get_children():
        my_tree.delete(record_1)
    count_new = 0
    for record_2 in final:
        my_tree.insert(parent='', index='end', iid=count_new, text='{}'.format(count_new + 1),
                       values=(record_2.get_all_parameters()))
        count_new += 1
    top_1.destroy()
    top_2.destroy()
    top_3.destroy()


def limited_res(option_1, option_2, entry_1, entry_2, all_rec):
    lst = []
    if option_2.get() == '-':
        op_2 = option_2.get()
    elif option_2.get() == 'Tak':
        op_2 = 1
    else:
        op_2 = 0
    if entry_1.get().isnumeric():
        en_1 = int(entry_1.get())
    else:
        en_1 = float('-inf')
    if entry_2.get().isnumeric():
        en_2 = int(entry_2.get())
    else:
        en_2 = float('inf')
    for rest in all_rec:
        if option_1.get() != '-':
            if rest.get_cuisine().find(option_1.get()) == -1:
                continue
        if op_2 != '-':
            if rest.get_delivery() != op_2:
                continue
        if en_1 > rest.get_cost():
            continue
        if en_2 < rest.get_cost():
            continue
        lst.append(rest)
    if len(lst) == 0:
        lst = all_rec
        messagebox.showinfo('Alert', 'Brak pasujących wyników!!!')
    return lst


def add_mark(tree, topsis, top_1, top_2):
    if len(tree.selection()) != 0:
        top = Toplevel()
        top.title('Dodawanie oceny')
        # top.geometry('500x500')

        selected = tree.selection()[0]

        frame_0 = Frame(top)
        frame_0.pack(expand=True)
        label_main = Label(frame_0, text='Oceń restauracje', font=('Comic Sans MS', 12), fg='Green')
        label_main.pack(expand=True)

        entry_frame_1 = Frame(top)
        name_lb_1 = Label(entry_frame_1, text='Styl')
        name_lb_1.grid(row=0, column=0)
        choose_mark_1 = StringVar()
        choose_mark_1.set('5')
        mark_1 = OptionMenu(entry_frame_1, choose_mark_1, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_1.config(width=15)
        mark_1.grid(row=1, column=0)

        name_lb_2 = Label(entry_frame_1, text='Stosunek ceny do jakości')
        name_lb_2.grid(row=0, column=1)
        choose_mark_2 = StringVar()
        choose_mark_2.set('5')
        mark_2 = OptionMenu(entry_frame_1, choose_mark_2, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_2.config(width=15)
        mark_2.grid(row=1, column=1)

        name_lb_3 = Label(entry_frame_1, text='Czas oczekiwania')
        name_lb_3.grid(row=0, column=2)
        choose_mark_3 = StringVar()
        choose_mark_3.set('5')
        mark_3 = OptionMenu(entry_frame_1, choose_mark_3, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_3.config(width=15)
        mark_3.grid(row=1, column=2)

        name_lb_4 = Label(entry_frame_1, text='Atmosfera')
        name_lb_4.grid(row=0, column=3)
        choose_mark_4 = StringVar()
        choose_mark_4.set('5')
        mark_4 = OptionMenu(entry_frame_1, choose_mark_4, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_4.config(width=15)
        mark_4.grid(row=1, column=3)

        name_lb_5 = Label(entry_frame_1, text='Okoliczność')
        name_lb_5.grid(row=0, column=4)
        choose_mark_5 = StringVar()
        choose_mark_5.set('5')
        mark_5 = OptionMenu(entry_frame_1, choose_mark_5, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_5.config(width=15)
        mark_5.grid(row=1, column=4)

        name_lb_6 = Label(entry_frame_1, text='Ocena ogólna')
        name_lb_6.grid(row=0, column=5)
        choose_mark_6 = StringVar()
        choose_mark_6.set('5')
        mark_6 = OptionMenu(entry_frame_1, choose_mark_6, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        mark_6.config(width=15)
        mark_6.grid(row=1, column=5)

        entry_frame_1.pack(pady=5, expand=True)
        button_frame = Frame(top)
        add_button = Button(button_frame, text="Wyślij ocenę", command=lambda: new_rec(selected, topsis, choose_mark_1,
                                                                                       choose_mark_2, choose_mark_3,
                                                                                       choose_mark_4, choose_mark_5,
                                                                                       choose_mark_6, top_1, top_2, top))
        add_button.grid(row=0, column=0, padx=20, pady=5)

        close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
        close.grid(row=0, column=1, padx=20, pady=5)
        button_frame.pack(pady=5, expand=True)
    else:
        messagebox.showinfo('Alert', 'Wybierz restaurację!!!')


def choose_preferences_1():
    top = Toplevel()
    top.title('Rekomendacje')
    #top.geometry('500x500')

    frame_p = Frame(top)
    frame_p.pack(expand=True)
    label_main = Label(frame_p, text='Podaj interesujące kryteria', font=('Comic Sans MS', 12), fg='Green')
    label_main.pack(expand=True)

    entry_frame_p = Frame(top)
    name_lb_1 = Label(entry_frame_p, text='Rodzaj kuchni')
    name_lb_1.grid(row=0, column=0)
    choose_option_1 = StringVar()
    choose_option_1.set('-')
    option_1 = OptionMenu(entry_frame_p, choose_option_1, '-', 'włoska', 'polska', 'chińska', 'indyjska', 'meksykańska',
                          'wegetariańska', 'fast food', 'pizza', 'makarony', 'burgery', 'sałatki', 'sushi', 'desery')
    option_1.grid(row=1, column=0)

    name_lb_2 = Label(entry_frame_p, text='Możliwość dostawy')
    name_lb_2.grid(row=0, column=1)
    choose_option_2 = StringVar()
    choose_option_2.set('-')
    option_2 = OptionMenu(entry_frame_p, choose_option_2, '-', 'Tak', 'Nie')
    option_2.grid(row=1, column=1)

    name_lb_3 = Label(entry_frame_p, text='Minimalna cena')
    name_lb_3.grid(row=0, column=2)
    entry_11 = Entry(entry_frame_p, width=10)
    entry_11['font'] = font.Font(size=11)
    entry_11.grid(row=1, column=2)
    # entry_11.insert(0, parameters[2])

    name_lb_5 = Label(entry_frame_p, text='Maksymalna cena')
    name_lb_5.grid(row=0, column=3)
    entry_21 = Entry(entry_frame_p, width=10)
    entry_21['font'] = font.Font(size=11)
    entry_21.grid(row=1, column=3)
    # entry_21.insert(0, parameters[2])

    entry_frame_p.pack(pady=5, expand=True)

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    label_main = Label(frame_0, text='Określ wagę kryteriów', font=('Comic Sans MS', 12), fg='Green')
    label_main.pack(expand=True)

    entry_frame_1 = Frame(top)
    name_lb_1 = Label(entry_frame_1, text='Styl')
    name_lb_1.grid(row=0, column=0)
    choose_mark_1 = StringVar()
    choose_mark_1.set('5')
    mark_1 = OptionMenu(entry_frame_1, choose_mark_1, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_1.config(width=15)
    mark_1.grid(row=1, column=0)

    name_lb_2 = Label(entry_frame_1, text='Stosunek ceny do jakości')
    name_lb_2.grid(row=0, column=1)
    choose_mark_2 = StringVar()
    choose_mark_2.set('5')
    mark_2 = OptionMenu(entry_frame_1, choose_mark_2, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_2.config(width=15)
    mark_2.grid(row=1, column=1)

    name_lb_3 = Label(entry_frame_1, text='Czas oczekiwania')
    name_lb_3.grid(row=0, column=2)
    choose_mark_3 = StringVar()
    choose_mark_3.set('5')
    mark_3 = OptionMenu(entry_frame_1, choose_mark_3, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_3.config(width=15)
    mark_3.grid(row=1, column=2)

    name_lb_4 = Label(entry_frame_1, text='Atmosfera')
    name_lb_4.grid(row=0, column=3)
    choose_mark_4 = StringVar()
    choose_mark_4.set('5')
    mark_4 = OptionMenu(entry_frame_1, choose_mark_4, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_4.config(width=15)
    mark_4.grid(row=1, column=3)

    name_lb_5 = Label(entry_frame_1, text='Okoliczność')
    name_lb_5.grid(row=0, column=4)
    choose_mark_5 = StringVar()
    choose_mark_5.set('5')
    mark_5 = OptionMenu(entry_frame_1, choose_mark_5, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_5.config(width=15)
    mark_5.grid(row=1, column=4)

    name_lb_6 = Label(entry_frame_1, text='Ocena ogólna')
    name_lb_6.grid(row=0, column=5)
    choose_mark_6 = StringVar()
    choose_mark_6.set('5')
    mark_6 = OptionMenu(entry_frame_1, choose_mark_6, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_6.config(width=15)
    mark_6.grid(row=1, column=5)

    name_lb_7 = Label(entry_frame_1, text='Ważność okoliczności')
    name_lb_7.grid(row=0, column=6)
    choose_mark_7 = StringVar()
    choose_mark_7.set('Wysoka')
    mark_7 = OptionMenu(entry_frame_1, choose_mark_7, 'Wysoka', 'Niska')
    mark_7.config(width=15)
    mark_7.grid(row=1, column=6)

    entry_frame_1.pack(pady=5, expand=True)
    button_frame = Frame(top)
    add_button = Button(button_frame, text="Wyszukaj (Topsis)", command=lambda: choose_the_best_1(choose_mark_1, choose_mark_2,
                                                                                         choose_mark_3, choose_mark_4,
                                                                                         choose_mark_5, choose_mark_6,
                                                                                         choose_mark_7, choose_option_1,
                                                                                         choose_option_2, entry_11,
                                                                                         entry_21, top))
    add_button.grid(row=0, column=0, padx=20, pady=5)

    rsm_button = Button(button_frame, text="Wyszukaj (RSM)", command=lambda: choose_the_best_1_RSM(choose_mark_1, choose_mark_2,
                                                                                         choose_mark_3, choose_mark_4,
                                                                                         choose_mark_5, choose_mark_6,
                                                                                         choose_mark_7, choose_option_1,
                                                                                         choose_option_2, entry_11,
                                                                                         entry_21, top))
    rsm_button.grid(row=0, column=1, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=2, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


def choose_preferences_2():
    top = Toplevel()
    top.title('Rekomendacje')
    #top.geometry('500x500')

    frame_p = Frame(top)
    frame_p.pack(expand=True)
    label_main = Label(frame_p, text='Podaj interesujące kryteria', font=('Comic Sans MS', 12), fg='Green')
    label_main.pack(expand=True)

    entry_frame_p = Frame(top)
    name_lb_1 = Label(entry_frame_p, text='Rodzaj kuchni')
    name_lb_1.grid(row=0, column=0)
    choose_option_1 = StringVar()
    choose_option_1.set('-')
    option_1 = OptionMenu(entry_frame_p, choose_option_1,'-', 'włoska', 'polska', 'chińska', 'indyjska', 'meksykańska',
                          'wegetariańska', 'fast food', 'pizza', 'makarony', 'burgery', 'sałatki', 'sushi', 'desery')
    option_1.grid(row=1, column=0)

    name_lb_2 = Label(entry_frame_p, text='Możliwość dostawy')
    name_lb_2.grid(row=0, column=1)
    choose_option_2 = StringVar()
    choose_option_2.set('-')
    option_2 = OptionMenu(entry_frame_p, choose_option_2, '-', 'Tak', 'Nie')
    option_2.grid(row=1, column=1)

    name_lb_3 = Label(entry_frame_p, text='Minimalna cena')
    name_lb_3.grid(row=0, column=2)
    entry_11 = Entry(entry_frame_p, width=10)
    entry_11['font'] = font.Font(size=11)
    entry_11.grid(row=1, column=2)
    # entry_11.insert(0, parameters[2])

    name_lb_5 = Label(entry_frame_p, text='Maksymalna cena')
    name_lb_5.grid(row=0, column=3)
    entry_21 = Entry(entry_frame_p, width=10)
    entry_21['font'] = font.Font(size=11)
    entry_21.grid(row=1, column=3)
    # entry_21.insert(0, parameters[2])

    entry_frame_p.pack(pady=5, expand=True)

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    label_main = Label(frame_0, text='Określ wagę kryteriów', font=('Comic Sans MS', 12), fg='Green')
    label_main.pack(expand=True)

    entry_frame_1 = Frame(top)
    name_lb_1 = Label(entry_frame_1, text='Styl')
    name_lb_1.grid(row=0, column=0)
    choose_mark_1 = StringVar()
    choose_mark_1.set('5')
    mark_1 = OptionMenu(entry_frame_1, choose_mark_1, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_1.config(width=15)
    mark_1.grid(row=1, column=0)

    name_lb_2 = Label(entry_frame_1, text='Stosunek ceny do jakości')
    name_lb_2.grid(row=0, column=1)
    choose_mark_2 = StringVar()
    choose_mark_2.set('5')
    mark_2 = OptionMenu(entry_frame_1, choose_mark_2, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_2.config(width=15)
    mark_2.grid(row=1, column=1)

    name_lb_3 = Label(entry_frame_1, text='Czas oczekiwania')
    name_lb_3.grid(row=0, column=2)
    choose_mark_3 = StringVar()
    choose_mark_3.set('5')
    mark_3 = OptionMenu(entry_frame_1, choose_mark_3, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_3.config(width=15)
    mark_3.grid(row=1, column=2)

    name_lb_4 = Label(entry_frame_1, text='Atmosfera')
    name_lb_4.grid(row=0, column=3)
    choose_mark_4 = StringVar()
    choose_mark_4.set('5')
    mark_4 = OptionMenu(entry_frame_1, choose_mark_4, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_4.config(width=15)
    mark_4.grid(row=1, column=3)

    name_lb_5 = Label(entry_frame_1, text='Okoliczność')
    name_lb_5.grid(row=0, column=4)
    choose_mark_5 = StringVar()
    choose_mark_5.set('5')
    mark_5 = OptionMenu(entry_frame_1, choose_mark_5, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_5.config(width=15)
    mark_5.grid(row=1, column=4)

    name_lb_6 = Label(entry_frame_1, text='Ocena ogólna')
    name_lb_6.grid(row=0, column=5)
    choose_mark_6 = StringVar()
    choose_mark_6.set('5')
    mark_6 = OptionMenu(entry_frame_1, choose_mark_6, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    mark_6.config(width=15)
    mark_6.grid(row=1, column=5)

    name_lb_7 = Label(entry_frame_1, text='Ważność okoliczności')
    name_lb_7.grid(row=0, column=6)
    choose_mark_7 = StringVar()
    choose_mark_7.set('Wysoka')
    mark_7 = OptionMenu(entry_frame_1, choose_mark_7, 'Wysoka', 'Niska')
    mark_7.config(width=15)
    mark_7.grid(row=1, column=6)

    entry_frame_1.pack(pady=5, expand=True)
    button_frame = Frame(top)
    add_button = Button(button_frame, text="Wyszukaj (Topsis)", command=lambda: choose_the_best_2(choose_mark_1, choose_mark_2,
                                                                                         choose_mark_3, choose_mark_4,
                                                                                         choose_mark_5, choose_mark_6,
                                                                                         choose_mark_7, choose_option_1,
                                                                                         choose_option_2, entry_11,
                                                                                         entry_21, top))
    add_button.grid(row=0, column=0, padx=20, pady=5)

    rsm_button = Button(button_frame, text="Wyszukaj (RSM)", command=lambda: choose_the_best_2_RSM(choose_mark_1, choose_mark_2,
                                                                                         choose_mark_3, choose_mark_4,
                                                                                         choose_mark_5, choose_mark_6,
                                                                                         choose_mark_7, choose_option_1,
                                                                                         choose_option_2, entry_11,
                                                                                         entry_21, top))
    rsm_button.grid(row=0, column=1, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=2, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


def get_target_points(status_quo, style, price_ratio, max_time, atmosphere, occasion, mark, criteria):
    parameters = [int(style.get()), int(price_ratio.get()), int(max_time.get()), int(atmosphere.get()),
                  int(occasion.get()), int(mark.get())]
    size = status_quo.shape
    lst = []
    for ver in range(size[0]):
        target = []
        for hor in range(size[1]):
            if hor == 4:
                if criteria == 1:
                    rand = random.randint(parameters[hor], 10)
                else:
                    rand = random.randint(1, parameters[hor])
            else:
                rand = random.randint(parameters[hor], 10)
            target.append(rand)
        lst.append(target)
    final = np.array(lst, dtype='float')
    return final


def choose_the_best_1(style, price_ratio, max_time, atmosphere, occasion, mark, criteria, option_1, option_2, entry_1,
                      entry_2, top_1):
    weights = np.array(list(map(float, (style.get(), price_ratio.get(), max_time.get(), atmosphere.get(),
                                        occasion.get(), mark.get()))), dtype='float')
    top = Toplevel()
    top.title('Rekomendacje')
    top.geometry('900x400')

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    ddd = Label(frame_0, text='Wybierz ostatecznie jedną restauracje oraz oceń ją', font=('Comic Sans MS', 12), fg='Green')
    ddd.pack(expand=True)
    tree_frame = Frame(top)
    tree_scroll_y = Scrollbar(tree_frame)
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x = Scrollbar(tree_frame, orient='horizontal')
    tree_scroll_x.pack(side=BOTTOM, fill=X)
    tree_frame.pack(padx=10)

    words = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
             'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
    my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
    my_tree['columns'] = words
    my_tree.column('#0', width=150)
    my_tree.heading('#0', text='Nr restauracji w rankingu')
    for i in range(len(words)):
        my_tree.column(words[i], width=150)
        my_tree.heading(words[i], text=words[i])
    count_s = 0

    names = limited_res(option_1, option_2, entry_1, entry_2, all_rest_rec)
    to_topsis = recommendation_system.objects_to_matrix(names)

    if criteria.get() == 'Wysoka':
        crit = 1
    else:
        crit = 0

    topsis = recommendation_system.topsis(to_topsis[0], weights, to_topsis[1], crit)

    for record in topsis:
        my_tree.insert(parent='', index='end', iid=count_s, text='{}'.format(count_s + 1),
                       values=(record.get_all_parameters()))
        count_s += 1
    my_tree.pack()
    tree_scroll_y.config(command=my_tree.yview)
    tree_scroll_x.config(command=my_tree.xview)
    button_frame = Frame(top)

    add_button = Button(button_frame, text="Dodaj ocenę", command=lambda: add_mark(my_tree, topsis, top_1, top),
                        bg='gold2', padx=30)
    add_button.grid(row=0, column=0, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=1, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


def choose_the_best_1_RSM(style, price_ratio, max_time, atmosphere, occasion, mark, criteria, option_1, option_2,
                          entry_1, entry_2, top_1):
    weights = np.array(list(map(float, (style.get(), price_ratio.get(), max_time.get(), atmosphere.get(),
                                        occasion.get(), mark.get()))), dtype='float')
    top = Toplevel()
    top.title('Rekomendacje')
    top.geometry('900x400')

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    ddd = Label(frame_0, text='Wybierz ostatecznie jedną restauracje oraz oceń ją', font=('Comic Sans MS', 12), fg='Green')
    ddd.pack(expand=True)
    tree_frame = Frame(top)
    tree_scroll_y = Scrollbar(tree_frame)
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x = Scrollbar(tree_frame, orient='horizontal')
    tree_scroll_x.pack(side=BOTTOM, fill=X)
    tree_frame.pack(padx=10)

    words = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
             'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
    my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
    my_tree['columns'] = words
    my_tree.column('#0', width=150)
    my_tree.heading('#0', text='Nr restauracji w rankingu')
    for i in range(len(words)):
        my_tree.column(words[i], width=150)
        my_tree.heading(words[i], text=words[i])
    count_s = 0

    names = limited_res(option_1, option_2, entry_1, entry_2, all_rest_rec)
    to_rsm = recommendation_system.objects_to_matrix(names)

    if criteria.get() == 'Wysoka':
        crit = 1
    else:
        crit = 0

    status_quo = recommendation_system.get_own_rates()
    target_points = get_target_points(status_quo, style, price_ratio, max_time, atmosphere, occasion, mark, crit)

    RSM = recommendation_system.RSM(to_rsm[0], weights, to_rsm[1], target_points, status_quo)

    for record in RSM:
        my_tree.insert(parent='', index='end', iid=count_s, text='{}'.format(count_s + 1),
                       values=(record.get_all_parameters()))
        count_s += 1
    my_tree.pack()
    tree_scroll_y.config(command=my_tree.yview)
    tree_scroll_x.config(command=my_tree.xview)
    button_frame = Frame(top)

    add_button = Button(button_frame, text="Dodaj ocenę", command=lambda: add_mark(my_tree, RSM, top_1, top),
                        bg='gold2', padx=30)
    add_button.grid(row=0, column=0, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=1, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


def choose_the_best_2(style, price_ratio, max_time, atmosphere, occasion, mark, criteria, option_1, option_2, entry_1,
                      entry_2, top_1):
    weights = np.array(list(map(float, (style.get(), price_ratio.get(), max_time.get(), atmosphere.get(),
                                        occasion.get(), mark.get()))), dtype='float')
    top = Toplevel()
    top.title('Rekomendacje')
    top.geometry('900x400')

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    ddd = Label(frame_0, text='Wybierz ostatecznie jedną restauracje oraz oceń ją', font=('Comic Sans MS', 12), fg='Green')
    ddd.pack(expand=True)
    tree_frame = Frame(top)
    tree_scroll_y = Scrollbar(tree_frame)
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x = Scrollbar(tree_frame, orient='horizontal')
    tree_scroll_x.pack(side=BOTTOM, fill=X)
    tree_frame.pack(padx=10)

    words = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
             'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
    my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
    my_tree['columns'] = words
    my_tree.column('#0', width=150)
    my_tree.heading('#0', text='Nr restauracji w rankingu')
    for i in range(len(words)):
        my_tree.column(words[i], width=150)
        my_tree.heading(words[i], text=words[i])
    count_s = 0

    own_rest = recommendation_system.get_own_recommendations()
    all_rest = recommendation_system.get_restaurants()
    final = list(set(all_rest) - set(own_rest))
    names = limited_res(option_1, option_2, entry_1, entry_2, final)
    to_topsis = recommendation_system.objects_to_matrix(names)

    if criteria.get() == 'Wysoka':
        crit = 1
    else:
        crit = 0

    topsis = recommendation_system.topsis(to_topsis[0], weights, to_topsis[1], crit)

    for record in topsis:
        my_tree.insert(parent='', index='end', iid=count_s, text='{}'.format(count_s + 1),
                       values=(record.get_all_parameters()))
        count_s += 1
    my_tree.pack()
    tree_scroll_y.config(command=my_tree.yview)
    tree_scroll_x.config(command=my_tree.xview)
    button_frame = Frame(top)

    add_button = Button(button_frame, text="Dodaj ocenę", command=lambda: add_mark(my_tree, topsis, top_1, top),
                        bg='gold2', padx=30)
    add_button.grid(row=0, column=0, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=1, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


def choose_the_best_2_RSM(style, price_ratio, max_time, atmosphere, occasion, mark, criteria, option_1, option_2,
                          entry_1, entry_2, top_1):
    weights = np.array(list(map(float, (style.get(), price_ratio.get(), max_time.get(), atmosphere.get(),
                                        occasion.get(), mark.get()))), dtype='float')
    top = Toplevel()
    top.title('Rekomendacje')
    top.geometry('900x400')

    frame_0 = Frame(top)
    frame_0.pack(expand=True)
    ddd = Label(frame_0, text='Wybierz ostatecznie jedną restauracje oraz oceń ją', font=('Comic Sans MS', 12), fg='Green')
    ddd.pack(expand=True)
    tree_frame = Frame(top)
    tree_scroll_y = Scrollbar(tree_frame)
    tree_scroll_y.pack(side=RIGHT, fill=Y)
    tree_scroll_x = Scrollbar(tree_frame, orient='horizontal')
    tree_scroll_x.pack(side=BOTTOM, fill=X)
    tree_frame.pack(padx=10)

    words = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
             'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
    my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
    my_tree['columns'] = words
    my_tree.column('#0', width=150)
    my_tree.heading('#0', text='Nr restauracji w rankingu')
    for i in range(len(words)):
        my_tree.column(words[i], width=150)
        my_tree.heading(words[i], text=words[i])
    count_s = 0

    own_rest = recommendation_system.get_own_recommendations()
    all_rest = recommendation_system.get_restaurants()
    final = list(set(all_rest) - set(own_rest))
    names = limited_res(option_1, option_2, entry_1, entry_2, final)
    to_rsm = recommendation_system.objects_to_matrix(names)

    if criteria.get() == 'Wysoka':
        crit = 1
    else:
        crit = 0

    status_quo = recommendation_system.get_own_rates()
    target_points = get_target_points(status_quo, style, price_ratio, max_time, atmosphere, occasion, mark, crit)

    RSM = recommendation_system.RSM(to_rsm[0], weights, to_rsm[1], target_points, status_quo)

    for record in RSM:
        my_tree.insert(parent='', index='end', iid=count_s, text='{}'.format(count_s + 1),
                       values=(record.get_all_parameters()))
        count_s += 1
    my_tree.pack()
    tree_scroll_y.config(command=my_tree.yview)
    tree_scroll_x.config(command=my_tree.xview)
    button_frame = Frame(top)

    add_button = Button(button_frame, text="Dodaj ocenę", command=lambda: add_mark(my_tree, RSM, top_1, top),
                        bg='gold2', padx=30)
    add_button.grid(row=0, column=0, padx=20, pady=5)

    close = Button(button_frame, text="Zamknij okno", command=lambda: top.destroy())
    close.grid(row=0, column=1, padx=20, pady=5)
    button_frame.pack(pady=5, expand=True)


frame_0 = Frame(tab_1)
frame_0.pack(expand=True)
ddd = Label(frame_0, text='Rekomender restauracji', font=('Comic Sans MS', 19), fg='Green', background='light goldenrod')
ddd.pack(expand=True)

tree_frame = Frame(tab_1)
tree_scroll_y = Scrollbar(tree_frame)
tree_scroll_y.pack(side=RIGHT, fill=Y)
tree_scroll_x = Scrollbar(tree_frame, orient='horizontal')
tree_scroll_x.pack(side=BOTTOM, fill=X)
tree_frame.pack(padx=10)

words = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
         'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
my_tree = ttk.Treeview(tree_frame, xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
my_tree['columns'] = words
my_tree.column('#0', width=150)
my_tree.heading('#0', text='Numer restauracji')
for i in range(len(words)):
    my_tree.column(words[i], width=150)
    my_tree.heading(words[i], text=words[i])
count_1 = 0

for record in all_rest_rec:
    my_tree.insert(parent='', index='end', iid=count_1, text='{}'.format(count_1 + 1),
                   values=(record.get_all_parameters()))
    count_1 += 1
my_tree.pack()
tree_scroll_y.config(command=my_tree.yview)
tree_scroll_x.config(command=my_tree.xview)

frame_2 = Frame(tab_1, background='light goldenrod')
frame_2.pack(expand=True)

run_project = Button(frame_2, text="Pokaż rekomendacje", command=choose_preferences_1, bg='gold2', padx=30)
run_project.grid(row=0, column=0, padx=30)
run_project['font'] = font.Font(size=12)
close = Button(frame_2, text="Zamknij", command=lambda: root.destroy(), bg='orange red', padx=30)
close.grid(row=0, column=1, padx=30)
close['font'] = font.Font(size=12)

frame_02 = Frame(tab_2)
frame_02.pack(expand=True)
label_2 = Label(frame_02, text='Rekomender restauracji', font=('Comic Sans MS', 19), fg='Green', background='light goldenrod')
label_2.pack(expand=True)

tree_frame_2 = Frame(tab_2)
tree_scroll_y_2 = Scrollbar(tree_frame_2)
tree_scroll_y_2.pack(side=RIGHT, fill=Y)
tree_scroll_x_2 = Scrollbar(tree_frame_2, orient='horizontal')
tree_scroll_x_2.pack(side=BOTTOM, fill=X)
tree_frame_2.pack(padx=10)

words_2 = ['Nazwa', 'Rodzaj kuchni', 'Możliwość dostawy', 'Średnia cena', 'Styl', 'Stosunek ceny do jakości',
         'Maks. czas oczekiwania', 'Atmosfera', 'Okoliczność', 'Ogólna ocena']
my_tree_2 = ttk.Treeview(tree_frame_2, xscrollcommand=tree_scroll_x_2.set, yscrollcommand=tree_scroll_y_2.set)
my_tree_2['columns'] = words_2
my_tree_2.column('#0', width=150)
my_tree_2.heading('#0', text='Numer restauracji')
for i in range(len(words)):
    my_tree_2.column(words_2[i], width=150)
    my_tree_2.heading(words_2[i], text=words_2[i])
count_2 = 0

for record in restaurants:
    my_tree_2.insert(parent='', index='end', iid=count_2, text='{}'.format(count_2 + 1),
                     values=(record.get_all_parameters()))
    count_2 += 1
my_tree_2.pack()
tree_scroll_y_2.config(command=my_tree_2.yview)
tree_scroll_x_2.config(command=my_tree_2.xview)

frame_2_2 = Frame(tab_2, background='light goldenrod')
frame_2_2.pack(expand=True)

run_project_2 = Button(frame_2_2, text="Pokaż rekomendacje", command=choose_preferences_2, bg='gold2', padx=30)
run_project_2.grid(row=0, column=0, padx=30)
run_project_2['font'] = font.Font(size=12)
close_2 = Button(frame_2_2, text="Zamknij", command=lambda: root.destroy(), bg='orange red', padx=30)
close_2.grid(row=0, column=1, padx=30)
close_2['font'] = font.Font(size=12)

root.mainloop()
