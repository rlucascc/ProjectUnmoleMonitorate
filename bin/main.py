from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont,QFontDatabase
import pyqtgraph as pg
import psutil
import cpuinfo
import platform

import sys
import threading


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # ===================================== GET MACHINE ATTRIBUTES =============================================

        # GET MACHINE ATTRIBUTES ===========================================================
        try:
            interfaces = list(psutil.net_if_addrs().keys())
            self._machine_net = interfaces[1]
            self._ip_address = psutil.net_if_addrs()[self._machine_net][0][1]
        except:
            self._machine_net = 'N/A'
            self._ip_address = 'N/A'

        try:
            self._machine_name = platform.node()
            self._machine_os = platform.platform()
            self._machine_arq = platform.architecture()[0]
        except:
            self._machine_name = "N/A"
            self._machine_os = "N/A"
            self._machine_arq = "N/A"
            pass

        # GET CPU ATTRIBUTES ===============================================================
        try:
            self._cpu_processor = cpuinfo.get_cpu_info()["brand_raw"]
            self._cpu_freq = cpuinfo.get_cpu_info()["hz_actual"][0] / 10 ** 9
            self._cpu_percent = psutil.cpu_percent()
            self._cpu_physical_core = psutil.cpu_count(logical=False)
            self._cpu_threads_core = psutil.cpu_count(logical=True)
            self._cpu_temp = psutil.sensors_temperatures()["k10temp"][0][1]
        except:
            self._cpu_percent = 0.
            self._cpu_physical_core = "N/A"
            self._cpu_threads_core = "N/A"
            self._cpu_temp = 0.
            self._memory_total = 0.
            self._memory_actual = 0.
            pass

        # MEMORY ATTRIBUTES ===============================================================
        try:
            self._memory_total = psutil.virtual_memory().total / 1024 ** 3
            self._memory_actual = psutil.virtual_memory().used / 1024 ** 3
        except:
            self._memory_total = 0.
            self._memory_actual = 0.
            pass
        # ==========================================================================================================
        # ======================================= WINDOW APP CONFIG ================================================

        # MAIN WINDOWS CONFIG
        self.setWindowTitle("Unmole Desktop Monitorator")
        self.setFixedSize(630, 700)
        self.setStyleSheet("background-color: black;")

        # CREATE LAYOUT
        self.layout = QVBoxLayout()

        # MAIN WIDGET AND CONFIG
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # CREATE FONT
        font_id = QFontDatabase.addApplicationFont("../Resources/Digital7-rg1mL.ttf")
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.font = QFont(family, 19)

        # CREATE A MEMORY LABEL
        self.memory_label = QLabel(f'{20 * "="} MEMORY STATUS {25 * "="}\n\n'
                                   f'>> MEMORIA TOTAL: {self._memory_total:.2f} GB\n'
                                   f'>> MEMORIA UTILIZADA: {self._memory_actual:.2f} GB')
        self.memory_label.setFont(self.font)
        self.memory_label.setStyleSheet('color:green')

        # CREATE A MACHINE LABEL
        self.machine_label = QLabel(f'{20 * "="} MACHINE STATUS {25 * "="}\n\n'
                                    f'>> NOME DO HOST: {self._machine_name}     >> INTERFACE DE REDE: {self._machine_net}\n'
                                    f'>> ARQUITETURA: {self._machine_arq}  {14 * " "}>> ENDERECO IP: {self._ip_address}\n'
                                    f'>> SO: {self._machine_os}')

        self.machine_label.setFont(self.font)
        self.machine_label.setStyleSheet('color:green')

        # CREATE A CPU LABEL
        self.CPU_label = QLabel(f'{20 * "="} CPU STATUS {22 * "="}\n\n'
                                    f'>> PROCESSADOR: {self._cpu_processor}\n'
                                    f'>> NUCLEOS FÍSICOS {self._cpu_physical_core}\n'
                                    f'>> NUCLEOS LOGICOS: {self._cpu_threads_core}\n'
                                    f'>> FREQUENCIA: {self._cpu_freq:.2f} Ghz  {20 * " "}>> PORCENTAGEM: {self._cpu_percent:.2f} %')

        self.CPU_label.setFont(self.font)
        self.CPU_label.setStyleSheet('color:green')

        # CREATE A DISK LABEL

        #PLOTS CPUT TEMP
        self.data = []

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setFixedSize(600, 200)
        self.plot_widget.setTitle(f'Temperatura da CPU: {self._cpu_temp}°')
        self.plot_widget.setLabel('left', 'Temperatura em Celsius')

        # Adiciona widgets ao layout
        self.layout.addWidget(self.machine_label)
        self.layout.addWidget(self.memory_label)
        self.layout.addWidget(self.CPU_label)
        self.layout.addWidget(self.plot_widget)

        # CREATE CURVE
        self.curve = self.plot_widget.plot(self.data, pen='g')

        #CREATE A TIMER TO CALL UPDATE TEMP CPU
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(100) #100ms

    def update_plots(self):
        # Adicionar dados novos
        self.data.append(psutil.sensors_temperatures()["k10temp"][0][1])  # ADD DATA OF CPU TEMP
        self._cpu_temp = self.data[-1]
        self.plot_widget.setTitle(f'Temperatura de CPU: {self._cpu_temp:.2f}°')

        # Atualizar a curva
        self.curve.setData(self.data)

        # Atualiza os demais atributos da máquina
        if (len(self.data) % 25) == 0:
            t1 = threading.Thread(target=self.update_atributes)
            t1.start()

        # Manter o gráfico em uma janela fixa
        if len(self.data) > 50:
            self.data.clear()


    def update_atributes(self):
        # MEMORY UPDATE
        self._memory_actual = self._memory_actual = psutil.virtual_memory().used / 1024 ** 3
        self.memory_label.setText(f'{20 * "="} MEMORY STATUS {25 * "="}\n\n'
                                  f'>> MEMORIA TOTAL: {self._memory_total:.2f} GB\n'
                                  f'>> MEMORIA UTILIZADA: {self._memory_actual:.2f} GB')

        # CPU UPDATE
        self._cpu_freq = cpuinfo.get_cpu_info()["hz_actual"][0] / 10 ** 9
        self._cpu_percent = psutil.cpu_percent()
        self.CPU_label.setText(f'{20 * "="} CPU STATUS {30 * "="}\n\n'
                                    f'>> PROCESSADOR: {self._cpu_processor}\n'
                                    f'>> NUCLEOS FÍSICOS {self._cpu_physical_core}\n'
                                    f'>> NUCLEOS LOGICOS: {self._cpu_threads_core}\n'
                                    f'>> FREQUENCIA: {self._cpu_freq:.2f} Ghz  {20 * " "}>> PORCENTAGEM: {self._cpu_percent:.2f} %')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
''''''
