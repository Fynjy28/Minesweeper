import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    0: '#f0f0f0',
    1: '#0000ff',
    2: '#00ff00',
    3: '#ff0000',
    4: '#8000ff',
    5: '#964b00',
    6: '#30d5c8',
    7: '#000000',
    8: '#9aa3b3'
}


class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 10
    MINES = 10
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True
    timer_seconds = 0

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

        self.timer_label = tk.Label(self.window, text='00:00', font='Calibri 14 bold')
        self.timer_label.grid(row=0, column=MineSweeper.COLUMNS - 1, columnspan=2, sticky='e', padx=(0, 5))

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
            self.check_win()
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return
        if MineSweeper.IS_FIRST_CLICK:
            MineSweeper.IS_FIRST_CLICK = False
            self.update_timer()
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()


        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True

            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.width_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)
        self.check_win()

    def width_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and next_btn['text'] != '🚩' and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Введено неправильно значение!')
            return
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def reload(self):
        for row in self.buttons:
            for button in row:
                button.destroy()

        self.buttons.clear()
        self.timer_label.config(text='00:00')
        self.timer_seconds = 0
        MineSweeper.IS_GAME_OVER = False
        MineSweeper.IS_FIRST_CLICK = True

        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
        self.timer_label.grid(row=0, column=MineSweeper.COLUMNS - 1, columnspan=2, sticky='e', padx=(0, 10))
        self.create_widgets()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть/Перезапуск', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='файл', menu=settings_menu)

        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for i in range(1, MineSweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

        # Add a dummy column to align the timer
        tk.Grid.columnconfigure(self.window, MineSweeper.COLUMNS, weight=0)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')
                else:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def check_win(self):
        btn_count_flag_true = 0
        btn_count_flag_false = 0
        btn_is_mine_but_not_flagged = 0
        btn_isnt_mine = 0
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if (btn.is_mine and btn['state'] == 'disabled' and btn['text'] == '🚩'):
                    btn_count_flag_true = btn_count_flag_true + 1
                if (not btn.is_mine and btn['state'] == 'disabled' and btn['text'] == '🚩'):
                    btn_count_flag_false = btn_count_flag_false + 1
                if (btn.is_mine and btn['state'] == 'normal' and btn['text'] == ''):
                    btn_is_mine_but_not_flagged = btn_is_mine_but_not_flagged + 1
                if (btn.count_bomb and not btn.is_open):
                    btn_isnt_mine = btn_isnt_mine + 1
        if (btn_isnt_mine > 0) or (btn_count_flag_false > 0):
            return
        if btn_count_flag_true + btn_is_mine_but_not_flagged == MineSweeper.MINES:
            self.open_all_buttons()
            showinfo('Win!', 'Вы выиграли!')
        else:
            return

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()

    def update_timer(self):
        if MineSweeper.IS_GAME_OVER:
            return
        if not MineSweeper.IS_GAME_OVER and not MineSweeper.IS_FIRST_CLICK:
            self.timer_seconds += 1
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f'{mins:02}:{secs:02}')
            if MineSweeper.IS_GAME_OVER:
                return
            else:
                self.window.after(999, self.update_timer)

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbor = self.buttons[i + row_dx][j + col_dx]
                            if neighbor.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        print(f'Исключаем кнопку №{exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
