from tkinter import *
from tkinter import messagebox  
import random  
import copy  

class SudokuGame:
    def __init__(self, root):
        self.root=root  
        self.setup_ui()  #создаем интерфейс
        self.new_game(40)  
    
    #транспонирование матрицы
    def transposing(self):
        self.table=[list(row) for row in zip(*self.table)]
    
    #обмен двух строк внутри одного блока
    def swap_rows(self):
        area=random.randint(0, 2)
        line1=random.randint(0, 2)
        line2=random.randint(0, 2)
        while line1==line2:
            line2=random.randint(0, 2) 
        line1=area*3+line1
        line2=area*3+line2
        self.table[line1],self.table[line2]=self.table[line2],self.table[line1]
    
    #обмен двух столбцов внутри одного блока 
    def swap_col(self):
        self.transposing()  
        self.swap_rows()  
        self.transposing()  
    
    #обмен двух блоков строк
    def swap_area_rows(self):
        area1=random.randint(0, 2) 
        area2=random.randint(0, 2)  
        while area1==area2:  
            area2=random.randint(0, 2) 
        for i in range(3): 
            N1=area1*3+i  
            N2=area2*3+i 
            self.table[N1],self.table[N2]=self.table[N2],self.table[N1]
    
    #обмен двух блоков столбцов 
    def swap_area_col(self):
        self.transposing()  
        self.swap_area_rows()  
        self.transposing() 
    
    #метод перемешивания: выполняет случайные преобразования
    def mixy(self, a=20):
        mix_func=[self.transposing, self.swap_rows, self.swap_col, self.swap_area_rows, self.swap_area_col] #список функций перемешивания
        for i in range(a):
            id_func=random.randint(0, len(mix_func)-1)  #выбор случайной функции
            mix_func[id_func]()   
    #создание графического интерфейса
    def setup_ui(self):
        self.root.title("SuDoKu")  
        self.root.geometry("550x600")  
        self.base_table=[
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
            ]
        
        #список для хранения ссылок на поля ввода
        self.cells=[[None for _ in range(9)] for _ in range(9)]
        
        #создаем контейнер для сетки судоку
        grid_frame=Frame(self.root)
        grid_frame.pack(pady=20)
        
        #создаем поля ввода
        for i in range(9):
            for j in range(9):
                entry=Entry(grid_frame, width=2, font=('Arial', 18),
                             justify='center', bg='white') 
                entry.grid(row=i, column=j, ipadx=10, ipady=10)
                if j in [2, 5]:
                    entry.grid(padx=(0, 5))
                if i in [2, 5]:
                    entry.grid(pady=(0, 5))
                
                #обработка ввода
                entry.bind('<KeyRelease>', lambda e, row=i, col=j: self.enter(row, col))
                self.cells[i][j]=entry
        
        #панель управления
        control_frame=Frame(self.root)
        control_frame.pack(pady=10)
        
        #кнопки сложности
        Button(control_frame, text="Легкая", command=lambda: self.new_game(30)).pack(side=LEFT, padx=5)
        Button(control_frame, text="Средняя", command=lambda: self.new_game(40)).pack(side=LEFT, padx=5)
        Button(control_frame, text="Сложная", command=lambda: self.new_game(50)).pack(side=LEFT, padx=5)
        
        #кнопки действий
        action_frame = Frame(self.root)
        action_frame.pack(pady=10)
        Button(action_frame, text="Проверить", command=self.check_solution).pack(side=LEFT, padx=5)
        Button(action_frame, text="Новая игра", command=lambda: self.new_game(40)).pack(side=LEFT, padx=5)
    
    #начало новой игры
    def new_game(self, level):
        self.clear_all_cells()
        self.table=copy.deepcopy(self.base_table) #копируем базовое поле 
        self.mixy(20) #перемешиваем для создания нового решения
        self.solved_table=copy.deepcopy(self.table) #сохраняем правильное решение
        self.game_table=copy.deepcopy(self.table) #создаем игровое поле (удаляем некоторые цифры)
        self.initial_positions=set() #запоминаем какие ячейки были изначально
        
        removed=0
        while removed<level:
            n=random.randint(0,8)
            m=random.randint(0,8)
            if self.game_table[n][m]!=0:
                self.game_table[n][m]=0
                removed+=1    
        #запоминаем начальные цифры
        for i in range(9):
            for j in range(9):
                if self.game_table[i][j]!=0:
                    self.initial_positions.add((i,j))
        self.update_display() #показываем новое поле

    #очистка поля  
    def clear_all_cells(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell:  # если ячейка существует
                    cell.delete(0, END)  # удаляем весь текст
                    cell.config(bg='white', state='normal', fg='black')  # сбрасываем настройки
                
    #обновление отображения поля
    def update_display(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                value = self.game_table[i][j]
                
                # Очищаем ячейку
                cell.delete(0, END)
                cell.config(bg='white', state='normal')
                
                # Если есть цифра - показываем её
                if value != 0:
                    cell.insert(0, str(value))
                    # Если это начальная цифра - делаем недоступной для изменения
                    if (i, j) in self.initial_positions:
                        cell.config(state='readonly')
    
    #обработка ввода в ячейку
    def enter(self,row,col,event=None):
        #нельзя менять начальные цифры
        if (row,col) in self.initial_positions:
            return
        
        cell=self.cells[row][col]
        value=cell.get()
        
        #если ячейка пустая
        if not value:
            self.game_table[row][col] = 0
            cell.config(bg='white')
            return

        #сохраняем цифру
        num=int(value)
        self.game_table[row][col]=num
        
        #проверяем на ошибки
        if not self.cell_true(row,col,num):
            cell.config(bg='#ffcccc')  
        else:
            cell.config(bg='white')
        
        #проверяем, заполнено ли все поле
        if self.complete():
            self.check_solution()
    
    #проверка, можно ли поставить цифру в ячейку
    def cell_true(self,row,col,num):
        #gроверка строки
        for j in range(9):
            if j!=col and self.game_table[row][j]==num:
                return False

        #проверка столбца
        for i in range(9):
            if i!=row and self.game_table[i][col]==num:
                return False
        
        #проверка квадрата
        start_row=3*(row//3)
        start_col=3*(col//3)
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if (i!=row or j!=col) and self.game_table[i][j]==num:
                    return False
        
        return True
    
    #проверка, все ли ячейки заполнены
    def complete(self):
        for i in range(9):
            for j in range(9):
                if self.game_table[i][j]==0:
                    return False
        return True
    
    #проверка решения
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.game_table[i][j]!=self.solved_table[i][j]:
                    messagebox.showerror("Ошибка")
                    return
        messagebox.showinfo("Все верно")

#запуск программы
def main():
    root=Tk()
    game=SudokuGame(root)
    root.mainloop()

if __name__=="__main__":
    main()
