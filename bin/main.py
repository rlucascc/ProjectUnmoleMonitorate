import customtkinter as ctk
import psutil
from platform import  platform,architecture,node
import cpuinfo
from tkinter import PhotoImage

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        #MACHINE ATTRIBUTES
        self.__machine_name = node()
        self.__machine_os = platform()
        self.__machine_arq = architecture()[0]

        #CPU ATTRIBUTES
        self.__cpu_processor = cpuinfo.get_cpu_info()["brand_raw"]
        self.__cpu_freq = cpuinfo.get_cpu_info()["hz_actual"][0]/10**9
        self.__cpu_percent = psutil.cpu_percent()
        self.__cpu_physical_core = psutil.cpu_count(logical=False)
        self.__cpu_threads_core = psutil.cpu_count(logical=True)
        self.__cpu_temp = psutil.sensors_temperatures()["k10temp"][0][1]

        #MEMORY ATTRIBUTES
        self.__memory_total = psutil.virtual_memory().total/1024 ** 3
        self.__memory_actual = psutil.virtual_memory().used/1024 ** 3

        #WINDOW ATTRIBUTES
        self.geometry('800x400')
        self.title('Unmole Desktop Monitorator')
        self.resizable(False, False)
        self._set_appearance_mode('dark')
        self.iconphoto(False, PhotoImage(file='../images/Unmole_IMG.png'))

        #MACHINE LABEL
        self.label_mac_name = ctk.CTkLabel(self,text=f'Hostname: {self.__machine_name}', fg_color='#174ba2', bg_color='transparent',corner_radius=8 , font=('roboto', 20), text_color='white').place(x=15, y=10)
        self.label_mac_os = ctk.CTkLabel(self,text=f'OS: {self.__machine_os}', fg_color='#174ba2', bg_color='transparent',corner_radius=8 , font=('roboto', 20), text_color='white').place(x=15, y=50)
        self.label_mac_arq = ctk.CTkLabel(self,text=f'Architecture: {self.__machine_arq}', fg_color='#174ba2', bg_color='transparent',corner_radius=8 , font=('roboto', 20), text_color='white').place(x=600, y=10)

        #CPU LABEL
        self.label_cpu_proc = ctk.CTkLabel(self, text=f'Processor: {self.__cpu_processor}', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20), text_color='white').place(x=15, y=110)
        self.label_cpu_freq = ctk.CTkLabel(self, text=f'CPU frequency: {self.__cpu_freq:.2f} Ghz', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20), text_color='white')
        self.label_cpu_freq.pack()
        self.label_cpu_freq.place(x=15, y=150)
        self.label_cpu_percent = ctk.CTkLabel(self, text=f'CPU percent: {self.__cpu_percent} %', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20), text_color='white')
        self.label_cpu_percent.pack()
        self.label_cpu_percent.place(x=15, y=190)
        self.label_cpu_Pcore = ctk.CTkLabel(self, text=f'Physical cores: {self.__cpu_physical_core}',fg_color='#174ba2', bg_color='transparent', corner_radius=8,font=('roboto', 20), text_color='white').place(x=600, y=150)
        self.label_cpu_Lcore = ctk.CTkLabel(self, text=f'Logical cores: {self.__cpu_threads_core}', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20),text_color='white').place(x=600, y=190)
        self.label_cpu_temp = ctk.CTkLabel(self, text=f'CPU : {int(self.__cpu_temp/2)*"|"}', anchor="w" ,width=770 ,fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 35), text_color='white')
        self.label_cpu_temp.pack()
        self.label_cpu_temp.place(x=15, y=350)

        #MEMORY LABEL
        self.label_memory_total = ctk.CTkLabel(self, text=f'Memory total: {self.__memory_total:.2f} GB', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20), text_color='white').place(x=15, y=250)
        self.label_memory_actual = ctk.CTkLabel(self, text=f'Memory used: {self.__memory_actual:.2f} GB', fg_color='#174ba2',bg_color='transparent', corner_radius=8, font=('roboto', 20), text_color='white')
        self.label_memory_actual.pack()
        self.label_memory_actual.place(x=15, y=290)

    #MONITORETE METHODS
    def monitore_CPU(self):
        #CPU FREQ UPDATE
        self.__cpu_freq = cpuinfo.get_cpu_info()["hz_actual"][0]/10**9
        self.label_cpu_freq.configure(text=f'CPU frequency: {self.__cpu_freq:.2f} Ghz')

        #CPU PERCENT UPDATE
        self.__cpu_percent = psutil.cpu_percent()
        self.label_cpu_percent.configure(text=f'CPU percent: {self.__cpu_percent} %')

        #CPU TEMP UPDATE
        self.__cpu_temp = psutil.sensors_temperatures()["k10temp"][0][1]
        self.label_cpu_temp.configure(text=f'CPU < {self.__cpu_temp:.2f}° > {int(self.__cpu_temp/2)*"|"}')
        self.label_cpu_temp.after(500, self.monitore_CPU)
        pass

    def monitore_MEMORY(self):
        self.__memory_actual = psutil.virtual_memory().used/1024 ** 3
        self.label_memory_actual.configure(text=f'Memory used: {self.__memory_actual:.2f} GB')
        self.label_memory_actual.after(5000, self.monitore_MEMORY)
        pass

if __name__ == "__main__":
    app = MainApp()
    app.monitore_CPU()
    app.monitore_MEMORY()
    app.mainloop()
