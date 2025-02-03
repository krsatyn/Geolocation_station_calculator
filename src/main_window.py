# main_application.py
import tkinter as tk

from point_calc_window import PointCalculator

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        AB_var = tk.StringVar()
        AC_var = tk.StringVar()
        BC_var = tk.StringVar()
        AD_var = tk.StringVar()
        BD_var = tk.StringVar()

        A_height_var = tk.StringVar()
        B_height_var = tk.StringVar()
        C_height_var = tk.StringVar()
        D_height_var = tk.StringVar()

        VEC_AB_var_X = tk.StringVar()
        VEC_AB_var_Y = tk.StringVar()

        # Стартовые параметры для тестовой работы
        AB_var.set('60.17')
        AC_var.set('84.83509356392554')
        BC_var.set('46.58641540191733')
        AD_var.set('46.78342762132762')
        BD_var.set('74.45440822768755')

        VEC_AB_var_X.set('0')
        VEC_AB_var_Y.set('0')
        
        
        AB_label = tk.Label(self.parent, text = 'Растояние AB', font=('calibre',10, 'bold'))
        AB_entry = tk.Entry(self.parent,textvariable = AB_var, font=('calibre',10,'normal'))

        AC_label = tk.Label(self.parent, text = 'Растояние AC', font=('calibre',10, 'bold'))
        AC_entry = tk.Entry(self.parent,textvariable = AC_var, font=('calibre',10,'normal'))

        BC_label = tk.Label(self.parent, text = 'Растояние BC', font=('calibre',10, 'bold'))
        BC_entry = tk.Entry(self.parent,textvariable = BC_var, font=('calibre',10,'normal'))

        AD_label = tk.Label(self.parent, text = 'Растояние AD', font=('calibre',10, 'bold'))
        AD_entry = tk.Entry(self.parent,textvariable = AD_var, font=('calibre',10,'normal'))

        BD_label = tk.Label(self.parent, text = 'Растояние BD', font=('calibre',10, 'bold'))
        BD_entry = tk.Entry(self.parent,textvariable = BD_var, font=('calibre',10,'normal'))

        A_height_label = tk.Label(self.parent, text = 'Высота А', font=('calibre',10, 'bold'))
        A_height_entry = tk.Entry(self.parent,textvariable = A_height_var, font=('calibre',10,'normal'))

        B_height_label = tk.Label(self.parent, text = 'Высота B', font=('calibre',10, 'bold'))
        B_height_entry = tk.Entry(self.parent,textvariable = B_height_var, font=('calibre',10,'normal'))

        C_height_label = tk.Label(self.parent, text = 'Высота С', font=('calibre',10, 'bold'))
        C_height_entry = tk.Entry(self.parent,textvariable = C_height_var, font=('calibre',10,'normal'))

        D_height_label = tk.Label(self.parent, text = 'Высота D', font=('calibre',10, 'bold'))
        D_height_entry = tk.Entry(self.parent,textvariable = D_height_var, font=('calibre',10,'normal'))

        VEC_AB_X_label = tk.Label(self.parent, text = 'Базис вектор lon ', font=('calibre',10, 'bold'))
        VEC_AB_X_entry = tk.Entry(self.parent,textvariable = VEC_AB_var_X, font=('calibre',10,'normal'))

        VEC_AB_Y_label = tk.Label(self.parent, text = 'lat  ', font=('calibre',10, 'bold'))
        VEC_AB_Y_entry = tk.Entry(self.parent,textvariable = VEC_AB_var_Y, font=('calibre',10,'normal'))

        AB_label.grid(row=2, column=0)
        AB_entry.grid(row=2, column=1)

        AC_label.grid(row=3, column=0)
        AC_entry.grid(row=3, column=1)

        BC_label.grid(row=4, column=0)
        BC_entry.grid(row=4, column=1)

        AD_label.grid(row=5, column=0)
        AD_entry.grid(row=5, column=1)

        BD_label.grid(row=6, column=0)
        BD_entry.grid(row=6, column=1)

        A_height_label.grid(row=2, column=2)
        A_height_entry.grid(row=2, column=3)

        B_height_label.grid(row=3, column=2)
        B_height_entry.grid(row=3, column=3)

        C_height_label.grid(row=4, column=2)
        C_height_entry.grid(row=4, column=3)

        D_height_label.grid(row=5, column=2)
        D_height_entry.grid(row=5, column=3)


        VEC_AB_X_label.grid(row=8, column=0)
        VEC_AB_X_entry.grid(row=8, column=1)

        VEC_AB_Y_label.grid(row=8, column=2)
        VEC_AB_Y_entry.grid(row=8, column=3)

        #sub_btn.grid(row=12, column=1)
        
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()