
from display_setting import DisplaySettings
from plot_settings_ui import PlotSettings
from PyQt5.QtWidgets import QApplication
import sys

class PlostSettingController(PlotSettings):
    def __init__(self, setup_file_path = "F:\\utils\\dummy_setup_file.psa")-> None:
        PlotSettings.__init__(self)
        self.display_setting = DisplaySettings(setup_file_path=setup_file_path)
        self.plot_titles = self.display_setting.get_plot_names()
        self.determine_plot_buttons(self.display_setting.plot_values, self.plot_titles)
        self.determine_plot_stack_widgets(len(self.display_setting.plot_values), self.plot_titles)
        self.add_label_to_widgets()
        self.add_title(self.plot_titles)
        self.add_global_page()
        self.button_click_action()
        self.cell_positions = [self.get_cell_position(len(sensor_list)) for sensor_list in self.display_setting.plot_values]
        self.sensor_tables = [self.define_table(len(num_row), position, page, layout) for num_row, position, page, layout in\
             zip(self.display_setting.plot_values, self.cell_positions, self.pages, self.page_layouts)]
        self.global_sensor_list = self.get_global_sensor_names()
        self.global_sensor_cell_position = self.get_cell_position(len(self.global_sensor_list))
        self.global_sensor_table = self.define_global_sensor_table(len(self.global_sensor_list), self.global_sensor_cell_position, self.global_page, self.global_page_layout)
        self.set_global_sensor_name_to_gui(self.global_sensor_table, self.display_setting.universal_parameter)
        self.global_assign_buttons( self.global_sensor_table, len(self.global_sensor_list))
        [button.clicked.connect(lambda:self.assign_button_click_action(self.global_sensor_table)) for button in self.assign_buttons]
        self.set_plot_button_text()
       
        self.set_plot_values()
        self.ok_button.clicked.connect(self.get_values_from_gui)
        self.exec_()

    def get_values_from_gui(self):
       
        val_from_gui =  self.get_sensor_name_frame_from_gui(self.sensor_tables)
        self.display_setting.new_set_plot_values(val_from_gui)
       
    def set_plot_values(self):
        [self.set_plot_value_to_gui(table, val) for  table, val in zip(self.sensor_tables, self.display_setting.plot_values)]

       
    def set_plot_button_text(self):
        [plot_button.setText(title) for plot_button, title in zip(self.plot_buttons, self.plot_titles)]

    def remove_duplicate_sensor_name(self):
        unique_sensor_name_lists = list()
        for sensor_list in self.sensor_name_list:
            for sensor in sensor_list:
                unique_sensor_name_lists.append(sensor)
            
        return set(unique_sensor_name_lists)

    def get_global_sensor_names(self):
        global_sensor_list = list()
        for k in self.display_setting.plot_values:
            for j in k:
                global_sensor_list.append(k[j]['sensor_name'])
        return set(global_sensor_list)

    def assign_button_click_action(self, table):
        row_col = self.sender().objectName().split('_')
        sensor_name = table.item(int(row_col[0]), 0).text()
        minimum_value = table.item(int(row_col[0]), 1).text()
        maximum_value = table.item(int(row_col[0]), 2).text()
        major_ticks_value  = table.item(int(row_col[0]), 3).text()
        minor_ticks_value = table.item(int(row_col[0]), 4).text()
       
        self.change_min_max_val(sensor_name, minimum_value, maximum_value, major_ticks_value, minor_ticks_value)

    def change_min_max_val(self, sensor_name, minimum_value, maximum_value, major_ticks_value, minor_ticks_value):
      
        for k in self.display_setting.plot_values:
            for j in k:
                
                if k[j]['sensor_name'] == sensor_name:
                    pass
                    if len(minimum_value) != 0:
                        k[j]['minimum'] = minimum_value
                    if len(maximum_value) != 0:
                        k[j]['maximum'] = maximum_value
                    if len(major_ticks_value) != 0:
                        k[j]['major'] = major_ticks_value
                    if len(minor_ticks_value) != 0:
                        k[j]['minor'] = minor_ticks_value
        self.set_plot_values()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlostSettingController()   
   #window.show()
    #sys.exit(app.exec_())