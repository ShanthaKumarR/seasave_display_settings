from abc import ABC, abstractmethod
from xml.dom import minidom 


class PlotSettings(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def set_plot_value(self, major_tics_value):
        """to set the major division value from the psa file"""
    @abstractmethod
    def get_plot_value(self):
        """to set the minor division value from the psa file"""
    
    @abstractmethod
    def get_number_of_plots(self):
        """to get the number of plots from the .psa file"""
    
    @abstractmethod
    def get_plot_names(self):
        """to get the name of the plots mentioned on the .psa file"""

class DisplaySettings(PlotSettings):
    def __init__(self, setup_file_path):
        self.setup_file_path = setup_file_path
        self.number_of_display = self.get_number_of_plots()
        self.plot_values, self.universal_parameter = self.get_plot_value()
    
    def get_plot_value(self):
        with open(self.setup_file_path, 'r') as file:
            domObj = minidom.parse(file)
            group = domObj.documentElement
            display_node = group.getElementsByTagName('Display')
            values = [dict() for _ in range(self.get_number_of_plots())]
            unique_parameter= {}
            for  node, my_dict in zip(display_node, values):
                try:
                    xy = node.getElementsByTagName('XYPlotData')[0]
                    ax = xy.getElementsByTagName('Axes')[0]
                    axis = ax.getElementsByTagName('Axis')
                    for i, sub_position in zip(axis, range(len(axis))):
                        temp_dict = dict()
                        try:
                            if i.getElementsByTagName('FullName')[0]:
                                parameter_name = i.getElementsByTagName('FullName')[0].getAttribute('value')
                                mini = i.getElementsByTagName('MinimumValue')[0].getAttribute('value')
                                maxi = i.getElementsByTagName('MaximumValue')[0].getAttribute('value')
                                maj= i.getElementsByTagName('MajorDivisions')[0].getAttribute('value')
                                minr = i.getElementsByTagName('MinorDivisions')[0].getAttribute('value')
                                temp_dict['sensor_name'] = parameter_name
                                temp_dict['minimum'] = mini
                                temp_dict['maximum'] = maxi
                                temp_dict['major'] = maj
                                temp_dict['minor'] = minr
                                if parameter_name not in unique_parameter:
                                    unique_parameter[parameter_name] = {'minimum': mini, 'maximum': maxi, 'majot_ticks': maj, 'minor_ticks':minr}
                            my_dict['sensor_'+str(sub_position)] = temp_dict
                        except IndexError:
                            pass
                except:
                    pass
            return values, unique_parameter


    def set_plot_value(self, plot_vlaues)->None:
            with open(self.setup_file_path, 'r') as file:
                domObj = minidom.parse(file)
                group = domObj.documentElement
                display_node = group.getElementsByTagName('Display')
                axes_nodes = [node.getElementsByTagName('Axes') for node in display_node]
                for index, axes in enumerate(axes_nodes):
                    axis_nodes = axes[0].getElementsByTagName('Axis')
                    try:
                        for element, val in zip(axis_nodes, plot_vlaues[index]):
                            if element.getElementsByTagName('FullName')[0].attributes['value'] == val['sensor_name']:
                                element.getElementsByTagName('MinimumValue')[0].attributes['value'] = val['minimum']
                                element.getElementsByTagName('MaximumValue')[0].attributes['value'] = val['maximum']
                                element.getElementsByTagName('MajorDivisions')[0].attributes['value'] = val['major']
                                element.getElementsByTagName('MinorDivisions')[0].attributes['value'] = val['minor']
                    except:
                        pass
                with open(self.setup_file_path, 'w') as file:
                    domObj.writexml(file)

    def get_number_of_plots(self):
        with open(self.setup_file_path, 'r') as file:
            plot_num =0
            domObj = minidom.parse(file)
            group = domObj.documentElement
            group = group.getElementsByTagName('DisplaySettings')[0].getElementsByTagName('Display')
            for node in group:
                try:
                    xy = node.getElementsByTagName('XYPlotData')[0]
                    plot_num +=1
                except:
                    
                    pass
        return plot_num
           
    def get_plot_names(self)->list:
        plot_titles = list()
        with open(self.setup_file_path, 'r') as file:
            domObj = minidom.parse(file)
            group = domObj.documentElement
            node = group.getElementsByTagName('DisplaySettings')[0].getElementsByTagName('Display')
            for inx, element in enumerate(node):
                try:
                    plot_name = element.getElementsByTagName('XYPlotData')[0].getElementsByTagName('Title')[0].getAttribute('value')
                    if len(plot_name) == 0:
                        plot_titles.append(str(inx))
                    else:
                        plot_titles.append(plot_name)
                except:
                    pass
        return plot_titles
            
    def new_set_plot_values(self, values):
        
        with open(self.setup_file_path, 'r') as file:
            domObj = minidom.parse(file)
            group = domObj.documentElement
            display_node = group.getElementsByTagName('Display')
            for  node, my_dict in zip(display_node, range(len(values))):
                xy = node.getElementsByTagName('XYPlotData')[0]
                ax = xy.getElementsByTagName('Axes')[0]
                axis = ax.getElementsByTagName('Axis')
                for i, inx in zip(axis, range(len(axis))):
                    try:
                        print(i.getElementsByTagName('FullName')[0].getAttribute('value'))
                        if i.getElementsByTagName('FullName')[0].getAttribute('value') ==  values[my_dict]['sensor_'+str(inx)]['sensor_name']:
                            i.getElementsByTagName('MinimumValue')[0].attributes['value'] =values[my_dict]['sensor_'+str(inx)]['minimum']
                            i.getElementsByTagName('MaximumValue')[0].attributes['value'] =values[my_dict]['sensor_'+str(inx)]['maximum']
                            i.getElementsByTagName('MajorDivisions')[0].attributes['value'] =values[my_dict]['sensor_'+str(inx)]['major']
                            i.getElementsByTagName('MinorDivisions')[0].attributes['value'] =values[my_dict]['sensor_'+str(inx)]['minor']
                    except IndexError:
                        pass
            with open(self.setup_file_path, 'w') as file:
                    domObj.writexml(file)