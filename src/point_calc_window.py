# point_calc_window.py

import tkinter as tk    
import webview
import pyproj
import numpy as np
import folium

from scipy.optimize import fsolve


class PointCalculator(tk.Frame):
    
    def __init__(self, parent, 
                 AB_var, 
                 AC_var, 
                 BC_var, 
                 AD_var, 
                 BD_var, 
                 A_height_var, 
                 B_height_var, 
                 *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.AB_var = AB_var
        self.AC_var = AC_var
        self.BC_var = BC_var
        self.AD_var = AD_var
        self.BD_var = BD_var
        self.A_height_var = A_height_var
        self.B_height_var = B_height_var
        
        

    def main(self,):
        
        parent = self.parent
        
        kanva_width = 1024  # высота
        kanva_height = 1024 # ширина

        window = tk.Toplevel(parent)
        kanva = tk.Canvas(window, width = kanva_width, height = kanva_height)  

        A_x_inp = tk.Entry(kanva)
        A_y_inp = tk.Entry(kanva)

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

        def open_global_map(self,) -> None:
            '''Открывает вебкарту в отдельном оке'''
            
            webview.create_window('Глобальная карта', 'point_map.html')
            webview.start() 
        
        def move_A_point(self, coord) -> tk.Event:
            ''' Передвигает точку А по полю после нажатия'''
            A_coord = coord
            kanva.coords(A_point, coord.x-15, coord.y-15, coord.x+15, coord.y+15)
            kanva.coords(A_label, coord.x, coord.y-25)
            
            return coord
        
        def add_point(self,) -> list:
            '''Ввод координаты точки А вручную'''\
                
            A_coord = [float(A_x_inp.get()), float(A_y_inp.get())]
            kanva.coords(A_point, A_coord[0]-15, kanva_height-(A_coord[1]-15), A_coord[0]+15, kanva_height-(A_coord[1]+15))
            kanva.coords(A_label, A_coord[0], kanva_height-(A_coord[1]-25))
            
            return A_coord 
        
        def xy_to_lonlat(self, x, y) -> float:
            '''Конвертация из декартовой системы координат в долготы и широты'''
            
            proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
            proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
            lonlat = pyproj.transform(proj_xy, proj_latlon, x, y)
            
            return lonlat[0], lonlat[1]
        
        def lonlat_to_xy(self, lon, lat) -> float:
            '''Конвертация из долготы и широты  в декартовой системы координат'''
            proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
            proj_xy = pyproj.Proj(proj="utm", zone=33, datum='WGS84')
            xy = pyproj.transform(proj_latlon, proj_xy, lon, lat)
            
            return xy[0], xy[1]
    
        def equations(self, vars, X1,Y1, X2,Y2, DIST_1, DIST_2) -> list:
            '''Решение системы уравнений 
            X1, Y1: декартова координаты Х и У первой точки,
            DIST1: Растояние до искомой точки от первой точки,
            
            X2, Y2: декартова координаты Х и У второй точки,
            DIST2: Растояние до искомой точки от второй точки,'''
            
            x, y = vars
            eq1 = (x-X1)**2 + (y - Y1)**2 - DIST_1**2  
            eq2 = (x-X2)**2  + (y - Y2)**2 - DIST_2**2
            return [eq1, eq2]

        def building_system_equations(self, X1, Y1, X2, Y2, DIST_1, DIST_2,initial_guess=[1,1]) -> list:
            ''' Решение системы уравнений с заданными параметрами '''
            
            new_equations = equations(X1=X1, Y1=Y1, DIST_1=DIST_1,
                                      X2=X2, Y2=Y2, DIST_2=DIST_2)   

            answer = np.round(fsolve(new_equations, initial_guess), 2)
            
            return answer
            
        def calculate_B_point(self, VEC_AB, A_coord, AB) -> float:
            ''' Поиск точки В по базис вектору
            задаётся направление вектора B, и происходит смещение вдоль этого вектора,
            значением является растояние станции от А до B'''
            
            size_vector = np.sqrt(VEC_AB[0]*VEC_AB[0] + VEC_AB[1]*VEC_AB[1])

            calc_B = [A_coord[0] + AB * VEC_AB[0] / size_vector,
                      A_coord[1] + AB * VEC_AB[1] / size_vector]

            return(calc_B)

        # Расчет координат
        def calculate(self,):

            A_coord_word = [kanva.coords(A_point)[0]+15, kanva_height-(kanva.coords(A_point)[1]+15)]
            A_coord = list(lonlat_to_xy(A_coord_word[0], A_coord_word[1]))
            #A_coord = A_coord_word
            AB = np.sqrt(float(self.AB_var.get())**2 - float(self.A_height_var.get())**2)
            AC = np.sqrt(float(self.AC_var.get())**2 - float(self.A_height_var.get())**2)
            BC = np.sqrt(float(self.BC_var.get())**2 - float(self.B_height_var.get())**2)
            AD = np.sqrt(float(self.AD_var.get())**2 - float(self.A_height_var.get())**2)
            BD = np.sqrt(float(self.BD_var.get())**2 - float(self.B_height_var.get())**2)

            VEC_AB = [float(self.VEC_AB_var_X.get()), float(self.VEC_AB_var_Y.get())]
            
            '''Расчет координаты точки B'''
            calc_B = calculate_B_point(VEC_AB=VEC_AB,
                                       A_coord=A_coord, 
                                       AB=AB)
            calc_B_word = xy_to_lonlat(calc_B[0], calc_B[1])
            
            '''Расчет координаты С'''
            calc_C = building_system_equations(X1=A_coord[0], Y1=A_coord[1], DIST_1=AC,
                                               X2=calc_B[0], Y2=calc_B[1], DIST_2=BC)
            calc_C_word = xy_to_lonlat(calc_C[0], calc_C[1])
            #print("Координаты точки C:", calc_C)

            '''Расчет координаты D'''
            calc_D = building_system_equations(X1=A_coord[0], Y1=A_coord[1], DIST_1=AD,
                                               X2=calc_B[0], Y2=calc_B[1], DIST_2=BD)
            calc_D_word = xy_to_lonlat(calc_C[0], calc_C[1])

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