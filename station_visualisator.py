import tkinter as tk
import numpy as np
import pyproj
import folium
import webview

from tkinter import *
from scipy.optimize import fsolve

root=tk.Tk()

# setting the windows size
root.geometry("600x400")

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

AB_var.set('60.17')
AC_var.set('84.83509356392554')
BC_var.set('46.58641540191733')
AD_var.set('46.78342762132762')
BD_var.set('74.45440822768755')

VEC_AB_var_X.set('0')
VEC_AB_var_Y.set('0')

kanva_width = 1024  # высота
kanva_height = 1024 # ширина

def create_window():
    
    window = tk.Toplevel(root)
    kanva = Canvas(window, width = kanva_width, height = kanva_height)

    A_x_inp = Entry(kanva)
    A_y_inp = Entry(kanva)
    
    kanva.create_text(40, 100, text="A lon :", fill="black", font=("Helvetica 11 bold"))
    kanva.create_text(40, 125, text="A Lat:", fill="black", font=("Helvetica 11 bold"))
    
    kanva.create_window(125,100,window=A_x_inp)
    kanva.create_window(125,125,window=A_y_inp)
    
    A_COORD = kanva.create_text(100, 15, text="Положение точки A", fill="black", font=("Helvetica 11 bold"))
    B_COORD = kanva.create_text(100, 35, text="Положение точки B", fill="black", font=("Helvetica 11 bold"))
    C_COORD = kanva.create_text(100, 55, text="Положение точки C", fill="black", font=("Helvetica 11 bold"))
    D_COORD = kanva.create_text(100, 75, text="Положение точки D", fill="black", font=("Helvetica 11 bold"))
    
    X_A = kanva.create_text(350, 15, text="lon: ", fill="black", font=("Helvetica 11 bold"))
    Y_A = kanva.create_text(550, 15, text="lat: ", fill="black", font=("Helvetica 11 bold"))
    #
    X_B = kanva.create_text(350, 35, text="lon: ", fill="black", font=("Helvetica 11 bold"))
    Y_B = kanva.create_text(550, 35, text="lat: ", fill="black", font=("Helvetica 11 bold"))
    #
    X_C = kanva.create_text(350, 55, text="lon: ", fill="black", font=("Helvetica 11 bold"))
    Y_C = kanva.create_text(550, 55, text="lat: ", fill="black", font=("Helvetica 11 bold"))
    #
    X_D = kanva.create_text(350, 75, text="lon: ", fill="black", font=("Helvetica 11 bold"))
    Y_D = kanva.create_text(550, 75, text="lat: ", fill="black", font=("Helvetica 11 bold"))
    
    # Точка А
    A_point = kanva.create_oval( 0, 0, 3, 3, fill = "#476042" )
    A_label = kanva.create_text(0, 3, text="A", fill="black", font=("Helvetica 11 bold"))
    
    # Точка B 
    B_point = kanva.create_oval( 0, 0, 3, 3, fill = "#476042" )
    B_label = kanva.create_text(0, 3, text="B", fill="black", font=("Helvetica 11 bold"))
    
    # Точка C
    C_point = kanva.create_oval( 0, 0, 3, 3, fill = "#476042" )
    C_label = kanva.create_text(0, 3, text="C", fill="black", font=("Helvetica 11 bold"))
    
    # Точка D
    D_point = kanva.create_oval( 0, 0, 3, 3, fill = "#476042" )
    D_label = kanva.create_text(0, 3, text="D", fill="black", font=("Helvetica 11 bold"))
    
    
    # открытие глобальной карты
    def open_global_map():
        webview.create_window('Глобальная карта', 'point_map.html')
        webview.start() 
        
    # Постановка точки по клику
    def move_A_point(coord): # r — радиус <<точки>>
        A_coord = coord
        kanva.coords(A_point, coord.x-15, coord.y-15, coord.x+15, coord.y+15)
        kanva.coords(A_label, coord.x, coord.y-25)
        
        return coord
    
    # Постановка точки по координатам
    def add_point():
        A_coord = [float(A_x_inp.get()), float(A_y_inp.get())]
        kanva.coords(A_point, A_coord[0]-15, kanva_height-(A_coord[1]-15), A_coord[0]+15, kanva_height-(A_coord[1]+15))
        kanva.coords(A_label, A_coord[0], kanva_height-(A_coord[1]-25))
        print(type(A_coord))
        return A_coord 
    
    # Конвертация в долготы и широты
    def xy_to_lonlat(x, y):
        proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
        proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
        lonlat = pyproj.transform(proj_xy, proj_latlon, x, y)
        print(type(lonlat[0]))
        return lonlat[0], lonlat[1]
    
    # Конвертация в X и Y
    def lonlat_to_xy(lon, lat):
        proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
        proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
        xy = pyproj.transform(proj_latlon, proj_xy, lon, lat)
        return xy[0], xy[1]
    
    # Расчет координат
    def calculate():

        A_coord_word = [kanva.coords(A_point)[0]+15, kanva_height-(kanva.coords(A_point)[1]+15)]
        A_coord = list(lonlat_to_xy(A_coord_word[0], A_coord_word[1]))
        #A_coord = A_coord_word
        AB = np.sqrt(float(AB_var.get())**2 - float(A_height_var.get())**2)
        AC = np.sqrt(float(AC_var.get())**2 - float(A_height_var.get())**2)
        BC = np.sqrt(float(BC_var.get())**2 - float(B_height_var.get())**2)
        AD = np.sqrt(float(AD_var.get())**2 - float(A_height_var.get())**2)
        BD = np.sqrt(float(BD_var.get())**2 - float(B_height_var.get())**2)

        VEC_AB = [float(VEC_AB_var_X.get()), float(VEC_AB_var_Y.get())]
        #VEC_AB = list(lonlat_to_xy(float(VEC_AB_var_X.get()), float(VEC_AB_var_Y.get())))

        # Расчет координаты B
        #calc_B = [VEC_AB[0] + A_coord[0], VEC_AB[1] + A_coord[1]]
        #calc_B_word = xy_to_lonlat(calc_B[0], calc_B[1])
        
        ''' Поиск точки В'''
        size_vector = np.sqrt(VEC_AB[0]*VEC_AB[0] + VEC_AB[1]*VEC_AB[1])
        
        calc_B = [A_coord[0] + AB * VEC_AB[0] / size_vector,
                  A_coord[1] + AB * VEC_AB[1] / size_vector]
        
        calc_B_word = xy_to_lonlat(calc_B[0], calc_B[1])
        print(type(calc_B_word))
        
        # Расчет координаты С
        def equations_C(vars):
            x, y = vars
            eq1 = (x-A_coord[0])**2 + (y - A_coord[1])**2 - AC**2  #x**2 + y**2 - 25
            eq2 = (x-calc_B[0])**2  + (y - calc_B[1] )**2 - BC**2
            return [eq1, eq2]
        
        initial_guess = [1, 1]
        calc_C = np.round(fsolve(equations_C, initial_guess), 2)
        calc_C_word = xy_to_lonlat(calc_C[0], calc_C[1])
        #print("Координаты точки C:", calc_C)
        
        def equations_D(vars):
            x, y = vars
            eq1 = (x-A_coord[0])**2 + (y - A_coord[1])**2 - AD**2
            eq2 = (x-calc_B[0])**2 + (y - calc_B[1])**2 - BD**2
            return [eq1, eq2]
        
        initial_guess = [1, 1]
        calc_D = np.round(fsolve(equations_D, initial_guess), 2)
        calc_D_word = xy_to_lonlat(calc_D[0], calc_D[1])
        #print("Координаты точки D:", calc_D)
        
        print(f'{A_coord_word=}')
        print(f'{calc_B_word=}')
        print(f'{calc_C_word=}')
        print(f'{calc_D_word=}')
        
        print(f'{A_coord=}')
        print(f'{calc_B=}')
        print(f'{calc_C=}')
        print(f'{calc_D=}')

        
        kanva.itemconfigure(X_A, text='lon: ' + str(A_coord_word[0]))
        kanva.itemconfigure(Y_A, text='lat: ' + str(A_coord_word[1]))

        kanva.itemconfigure(X_B, text='lon: ' + str(calc_B_word[0]))
        kanva.itemconfigure(Y_B, text='lat: ' + str(calc_B_word[1]))

        kanva.itemconfigure(X_C, text='lon: ' + str(calc_C_word[0]))
        kanva.itemconfigure(Y_C, text='lat: ' + str(calc_C_word[1]))

        kanva.itemconfigure(X_D, text='lon: ' + str(calc_D_word[0]))
        kanva.itemconfigure(Y_D, text='lat: ' + str(calc_D_word[1]))
        
        kanva.coords(B_point, calc_B[0]-15, kanva_height-(calc_B[1]-15), calc_B[0]+15, kanva_height-(calc_B[1]+15))
        kanva.coords(B_label, calc_B[0], kanva_height-(calc_B[1]-25))
        
        kanva.coords(C_point, calc_C[0]-15, kanva_height-(calc_C[1]-15), calc_C[0]+15, kanva_height-(calc_C[1]+15))
        kanva.coords(C_label, calc_C[0], kanva_height-(calc_C[1]-25))
        
        kanva.coords(D_point, calc_D[0]-15, kanva_height-(calc_D[1]-15), calc_D[0]+15, kanva_height-(calc_D[1]+15))
        kanva.coords(D_label, calc_D[0], kanva_height - (calc_D[1]-25))
        
        map = folium.Map(location=A_coord_word, zoom_start=100)

        folium.Marker(A_coord_word, '3').add_to(map)
        folium.Marker(calc_B_word,  '5').add_to(map)
        folium.Marker(calc_C_word,  '4').add_to(map)
        folium.Marker(calc_D_word,  '6').add_to(map)
        
      
        # basis vector_coord [53.20874, 50.25855]
        real_station_map = [[53.208388, 50.259608],
                            [53.209152, 50.259474],
                            [53.208839, 50.259005],
                            [53.208654, 50.260126]]
        
        for i in range(len(real_station_map)):
            telephone_position = folium.map.FeatureGroup()
            # style the feature group
            telephone_position.add_child(
                folium.features.CircleMarker(
                    [real_station_map[i][0], real_station_map[i][1]], radius = 2,    
                    color = 'red', fill_color = 'Red'
                )
        )
    
            map.add_child(telephone_position)
        map.save("point_map.html")

    culc_coord_points_button = Button(window, text="Найти координаты", command=calculate)
    input_A_point_button = Button(window, text="Поставить точку А", command=add_point)
    open_global_map_button = Button(window, text='Открыть карту', command=open_global_map)
    
    input_A_point_widget = kanva.create_window(275, 100, window=input_A_point_button)
    culc_coord_points_widget = kanva.create_window(275, 125, window=culc_coord_points_button)
    open_global_map_widhet = kanva.create_window(275, 150, window=open_global_map_button)
    
    
    kanva.pack()
    kanva.bind( "<Button-1>", move_A_point) 
    window.mainloop()

AB_label = tk.Label(root, text = 'Растояние AB', font=('calibre',10, 'bold'))
AB_entry = tk.Entry(root,textvariable = AB_var, font=('calibre',10,'normal'))

AC_label = tk.Label(root, text = 'Растояние AC', font=('calibre',10, 'bold'))
AC_entry = tk.Entry(root,textvariable = AC_var, font=('calibre',10,'normal'))

BC_label = tk.Label(root, text = 'Растояние BC', font=('calibre',10, 'bold'))
BC_entry = tk.Entry(root,textvariable = BC_var, font=('calibre',10,'normal'))

AD_label = tk.Label(root, text = 'Растояние AD', font=('calibre',10, 'bold'))
AD_entry = tk.Entry(root,textvariable = AD_var, font=('calibre',10,'normal'))

BD_label = tk.Label(root, text = 'Растояние BD', font=('calibre',10, 'bold'))
BD_entry = tk.Entry(root,textvariable = BD_var, font=('calibre',10,'normal'))

A_height_label = tk.Label(root, text = 'Высота А', font=('calibre',10, 'bold'))
A_height_entry = tk.Entry(root,textvariable = A_height_var, font=('calibre',10,'normal'))

B_height_label = tk.Label(root, text = 'Высота B', font=('calibre',10, 'bold'))
B_height_entry = tk.Entry(root,textvariable = B_height_var, font=('calibre',10,'normal'))

C_height_label = tk.Label(root, text = 'Высота С', font=('calibre',10, 'bold'))
C_height_entry = tk.Entry(root,textvariable = C_height_var, font=('calibre',10,'normal'))

D_height_label = tk.Label(root, text = 'Высота D', font=('calibre',10, 'bold'))
D_height_entry = tk.Entry(root,textvariable = D_height_var, font=('calibre',10,'normal'))

VEC_AB_X_label = tk.Label(root, text = 'Базис вектор lon ', font=('calibre',10, 'bold'))
VEC_AB_X_entry = tk.Entry(root,textvariable = VEC_AB_var_X, font=('calibre',10,'normal'))

VEC_AB_Y_label = tk.Label(root, text = 'lat  ', font=('calibre',10, 'bold'))
VEC_AB_Y_entry = tk.Entry(root,textvariable = VEC_AB_var_Y, font=('calibre',10,'normal'))

sub_btn=tk.Button(root,text = 'Поставить точку', command = create_window)

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

sub_btn.grid(row=12, column=1)
root.mainloop()