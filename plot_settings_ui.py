from PyQt5.QtWidgets import QFrame, QVBoxLayout, QDialog, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QStackedWidget, QWidget
from PyQt5 import QtCore


MINIMUM_COLUMN_POSITION = 1
MAXIMUM_COLUMN_POSITION = 2
MAJOR_TICKS_COLUMN_POSITION = 3
MINOR_TICKS_COLUMN_POSITION = 4
SENSOR_NAME_COLUMN_POSITION = 0

GLOBAL_SENSOR_COLUMN_POSITION = 0
TABLE_COLUMN_NUMBER = 5

class PlotSettings(QDialog):
    def __init__(self):
        super().__init__()
        
        self.resize(700, 700)
        self.vbox_layout_1_display = QVBoxLayout(self)
        self.first_frame_display = QFrame(self)
        self.hbox_layout_1_plot = QHBoxLayout(self.first_frame_display)
        self.frame_plot_button = QFrame(self.first_frame_display)
        self.hbox_layout_1_plot.addWidget(self.frame_plot_button)
        self.frame_plot_stack = QFrame(self.first_frame_display)
        self.hbox_layout_1_plot.addWidget(self.frame_plot_stack)
        self.vbox_layout_1_display.addWidget(self.first_frame_display)
        self.controll_button_frame = QFrame(self)
        self.vbox_layout_1_display.addWidget(self.controll_button_frame)
        self.ok_button = QPushButton(self.controll_button_frame)
        self.ok_button.setText('OK')
        self.cancle_button = QPushButton(self.controll_button_frame)
        self.cancle_button.setText('Cancle')
        self.hbox_layout_2_plot = QHBoxLayout(self.controll_button_frame)
        self.hbox_layout_2_plot.addWidget(self.ok_button)
        self.hbox_layout_2_plot.addWidget(self.cancle_button)
        #plot button 
        self.plot_button_v_layout = QVBoxLayout()
        self.frame_plot_button_v_layout = QVBoxLayout(self.frame_plot_button)
        self.frame_plot_button_v_layout.addLayout(self.plot_button_v_layout)

        self.global_button = QPushButton(self.frame_plot_button)
        self.global_button.setText('global button')
        self.global_button.setObjectName('global page')
        self.plot_button_v_layout.addWidget(self.global_button)

        #statcked widgets 
        self.frame_plot_stack_vlayout = QVBoxLayout(self.frame_plot_stack)
        
        
    def determine_plot_buttons(self, number_of_plots, titles):
        self.plot_buttons = [QPushButton(self.frame_plot_button) for _ in range(len(number_of_plots))]
        [button.setObjectName(title) for button, title in zip(self.plot_buttons, titles)]
        [self.plot_button_v_layout.addWidget(plot_button) for plot_button in self.plot_buttons]
    
    def determine_plot_stack_widgets(self, number_of_plots, titles):
        self.plot_stack_widget = QStackedWidget(self.frame_plot_stack)
        self.pages = [ QWidget() for _ in range(number_of_plots)]
        [page.setObjectName(title) for page, title in zip(self.pages, titles)]
        [self.plot_stack_widget.addWidget(page) for page in self.pages]
        self.frame_plot_stack_vlayout.addWidget(self.plot_stack_widget)
        self.page_layouts = [QVBoxLayout(page) for page in self.pages]

    def add_global_page(self):
        self.global_page = QWidget()
        self.plot_stack_widget.addWidget(self.global_page)
        self.global_page.setObjectName('global page')
        self.global_page_layout = QVBoxLayout(self.global_page)
        
    def add_label_to_widgets(self):
        self.labes = [QLabel(page) for page in self.pages]
        [layout.addWidget(lable, 0, QtCore.Qt.AlignHCenter)for layout, lable in zip(self.page_layouts, self.labes)]

    def add_title(self, titles:list):
        [label.setText(title+'_plot') for label, title in zip(self.labes, titles)]
    
    def button_click_action(self):
        button_acitons = [button.clicked.connect(self.change_page) for button in self.plot_buttons]
        self.global_button.clicked.connect(self.global_page_change)

    def change_page(self):
        for i in self.pages:
            if self.sender().objectName() == i.objectName():
                self.plot_stack_widget.setCurrentWidget(i)
    
    def global_page_change(self):
        self.plot_stack_widget.setCurrentWidget(self.global_page)

    def define_table(self, num_row, position, page, page_layout):
        tabel_widget_diplay = QTableWidget(page)
        tabel_widget_diplay.resize(500,500)
        tabel_widget_diplay.setRowCount(num_row)
        tabel_widget_diplay.setColumnCount(TABLE_COLUMN_NUMBER)
        table_column_name =['sensor name', 'MinVal', 'MaxVal', 'MajTics', 'MinTics']
        tabel_widget_diplay.setHorizontalHeaderLabels(table_column_name)
        [tabel_widget_diplay.setItem(row, col,  QTableWidgetItem()) for row, col in position]
        page_layout.addWidget(tabel_widget_diplay)
        return tabel_widget_diplay

    def define_global_sensor_table(self, num_row, position, page, page_layout):
        tabel_widget_diplay = QTableWidget(page)
        tabel_widget_diplay.resize(500,500)
        tabel_widget_diplay.setRowCount(num_row)
        tabel_widget_diplay.setColumnCount(TABLE_COLUMN_NUMBER+1)
        table_column_name =['sensor name', 'MinVal', 'MaxVal', 'MajTics', 'MinTics']
        tabel_widget_diplay.setHorizontalHeaderLabels(table_column_name)
        [tabel_widget_diplay.setItem(row, col,  QTableWidgetItem()) for row, col in position]
        page_layout.addWidget(tabel_widget_diplay)
        return tabel_widget_diplay


    def get_cell_position(self, num_sensor):
        position= list()
        k = 0
        for _ in range(num_sensor): 
            for j in range(5):
                position.append((k, j))
            k +=1
        return position

    def set_plot_value_to_gui(self, tabel_widget_diplay, plot_val):
        row =0
        while row <len(plot_val):
            for k in plot_val:
                for key in plot_val[k]:
                    
                    if key == 'minimum':
                        tabel_widget_diplay.item(row, MINIMUM_COLUMN_POSITION).setText(str(plot_val[k][key])) 
                        
                    elif key == 'maximum':
                        tabel_widget_diplay.item(row, MAXIMUM_COLUMN_POSITION).setText(str(plot_val[k][key]))
                        
                    elif key == 'major':
                        tabel_widget_diplay.item(row, MAJOR_TICKS_COLUMN_POSITION).setText(str(plot_val[k][key]))
                        
                    elif key == 'minor':
                        tabel_widget_diplay.item(row, MINOR_TICKS_COLUMN_POSITION).setText(str(plot_val[k][key]))
                        
                    elif key == 'sensor_name':
                        tabel_widget_diplay.item(row, SENSOR_NAME_COLUMN_POSITION).setText(str(plot_val[k][key]))
                row +=1

 

    def set_global_sensor_name_to_gui(self, tabel_widget_diplay, sensor_name):
        for key, row in zip(sensor_name, range(len(sensor_name))):
            tabel_widget_diplay.item(row, SENSOR_NAME_COLUMN_POSITION).setText(str(key))
            for k in sensor_name[key]:
               
                if k == 'minimum':
                    tabel_widget_diplay.item(row, MINIMUM_COLUMN_POSITION).setText(str(sensor_name[key][k])) 
                                
                elif k == 'maximum':
                    tabel_widget_diplay.item(row, MAXIMUM_COLUMN_POSITION).setText(str(sensor_name[key][k]))
                    
                elif k == 'majot_ticks':
                    tabel_widget_diplay.item(row, MAJOR_TICKS_COLUMN_POSITION).setText(str(sensor_name[key][k]))
                    
                elif k == 'minor_ticks':
                    tabel_widget_diplay.item(row, MINOR_TICKS_COLUMN_POSITION).setText(str(sensor_name[key][k]))
             

    def global_assign_buttons(self,tabel, num_row):
        self.assign_buttons = [QPushButton() for _ in range(num_row)]
        [button.setText('set value') for button in self.assign_buttons]
        [button.setObjectName(str(row)+'_'+str(5)) for button, row in zip(self.assign_buttons, range(num_row))]
        [tabel.setCellWidget(row, 5, button) for button, row in zip(self.assign_buttons, range(num_row))]
       
    def get_sensor_name_frame_from_gui(self, tabel_widget):
        gui_values = [dict() for d in range(len(tabel_widget))]
        for tabel, parent_dict in zip(tabel_widget, gui_values):
            table_dict = {}
            for row in range(tabel.rowCount()):
                sensor_name = tabel.item(row, SENSOR_NAME_COLUMN_POSITION).text()
                minor_val  = tabel.item(row, MINOR_TICKS_COLUMN_POSITION).text()
                major_val = tabel.item(row, MAJOR_TICKS_COLUMN_POSITION).text()
                maximum_val = tabel.item(row, MAXIMUM_COLUMN_POSITION).text()
                minimum_val = tabel.item(row, MINIMUM_COLUMN_POSITION).text()
                parent_dict['sensor_'+str(row)] = {'sensor_name' :sensor_name, 'minor':minor_val, 'major':major_val, 'maximum':maximum_val, 'minimum':minimum_val}
            
        return gui_values
        

    def get_minimum_value_from_gui(self, tabel_widget_diplay, col, sensor_name):
        return [tabel_widget_diplay.item(row, col).text() for row  in range(len(sensor_name)) ]
    
    def get_value_from_gui(self, tabel_widget_diplay, col, sensor_name):
        return [tabel_widget_diplay.item(row, col).text() for row  in range(len(sensor_name)) ]


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = PlotSettings()   
#     window.show()
    
#     sys.exit(app.exec_())