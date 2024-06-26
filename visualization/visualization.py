from matplotlib import pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

import pandas as pd

class Visualizer():
    def __init__(self, path="plots/", **kwargs):
        # maybe some general settings like style and window size
        # also the path where the plots are saved
        
        #establish a better system!
        self.path = path
        self.figsize = (10,5)
        
        # font settings
        self.font_family = "Arial, sans-serif"
        
        self.margin=dict(l=50, r=50, t=50, b=50)
        if "margin" in kwargs:
            self.margin = kwargs["margin"]
            
        self.axis_title_size = 18
        if "axis_title_size" in kwargs:
            self.axis_title_size = kwargs["axis_title_size"]
            
        self.text_size = 14
        if "text_size" in kwargs:
            self.text_size = kwargs["text_size"]
            
        self.title_size = 30
        if "title_size" in kwargs:
            self.title_size = kwargs["title_size"]
         
        # format settings
        self.plot_height_provided = 1000
        if "plot_height" in kwargs:
            self.plot_height_provided = kwargs["plot_height"]

        self.plot_height = self.plot_height_provided
        
        self.plot_width = None
        if "plot_width" in kwargs:
            self.plot_width = kwargs["plot_width"]
            
        # plotly config
        self.config={
            "responsive": True,
            'scrollZoom': True,
            "displaylogo": False,
            "displayModeBar": True,
            "modeBarButtonsToRemove": 
                ["select", "zoomIn", "zoomOut", "autoScale", "lasso2d"]}


############ CSS ############
    def get_css_class(self):
        
        if self.plot_width is None:
            return "chart-container-responsive"
        else:
            return "chart-container-fixed"
        
         
############ Plotly ############
    ##### Basic Utility Functions #####
    def add_title(self, fig, title):
        
        fig.update_layout(
            title = {
                'text':f"{title}",
                'font':{
                    'size':self.title_size},
                'x':0.5,
                'y':0.95,
                'xanchor':'center'},)
        
        return fig
             
    def apply_general_settings(self, fig):
        
        # general layout settings
        fig.update_layout(
            barmode='group',
            dragmode='pan',
            font=dict(
                family=self.font_family,
                size=self.text_size,),
            margin=self.margin,
            height=self.plot_height,
            hoverlabel=dict(font_size=self.text_size+2))

        if self.plot_width is not None:
            fig.update_layout(width=self.plot_width)
            
        return fig

    def customize_yaxis(self, fig, title, range, row, col):
        
        fig.update_yaxes(
            title={
                "text": title,
                "font": {"size": self.axis_title_size}},
            range=range,
            row=row, col=col)
        
        return fig      
        
    def frequency_yaxis(self, fig, row, col, relative, title):
        if relative:
            if title:
                title_text = "<b> Relative Frequency </b>"
            else:
                title_text = ""
                
            fig = self.customize_yaxis(fig=fig,
                                      title=title_text, 
                                      range=[0,1.1], 
                                      row=row, col=col)
            
        else:
            if title:
                title_text = "<b> Absolute Frequency </b>"
            else:
                title_text = ""
                
            fig = self.customize_yaxis(fig=fig,
                                      title=title_text, 
                                      range=[0, None], 
                                      row=row, col=col)
            
        return fig
    
    def date_xaxis(self, fig, row, col, x, ticktext):
        fig.update_xaxes(
            title={
                "text":"<b> Course Date </b>",
                "font": {"size": self.axis_title_size}},
            automargin=True,
            tickvals=x,
            ticktext=ticktext,
            row=row, col=col)  
        return fig
    
    def customize_hover(self, fig, mode, **kwargs):
        if mode == "multi_bar":
            fig.update_traces(
                hovertemplate="<b>Frequency: %{y}</b><br>" +
                            "%{customdata[13]}: %{customdata[12]}<br>" +
                            #"Course number: %{customdata[0]}<br>" +
                            #"Present: %{customdata[17]} | Registered: %{customdata[14]}<br>" +
                            "Time: %{customdata[1]} %{customdata[8]}-%{customdata[9]}<br>" +
                            "Room: %{customdata[2]}<br>"+
                            #"Room: %{customdata[2]} | Room Capacity:%{customdata[7]} <br>"+
                            #"Irregular: %{customdata[21]}<br>" +
                            "Note: %{customdata[3]}")
            
        elif mode == "single_bar":
            fig.update_traces(
                hovertemplate="Frequency: %{y}<br>" +
                            "Note: %{customdata[3]}<br>"
            )
        
        elif mode == "grouped_bar":
            fig.update_traces(
                hovertemplate="Frequency: %{y}<br>" + kwargs["template"]
            )
            
        elif mode == "late_students":
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                            "Title: %{customdata[8]} [%{customdata[9]}]<br>" +
                            "Y: %{y}<br>" +
                            "Present:%{customdata[19]} | Registered:%{customdata[16]}<br>" +
                            "Start Time: %{customdata[1]} %{customdata[5]}<br>" +
                            "Room: %{customdata[2]}<br>"+
                            "Irregular: %{customdata[27]}<br>" +
                            "First: %{customdata[20]} | Last: %{customdata[21]}<br>"
                            "Note: %{customdata[3]}")
        else:
            raise ValueError("Mode must be one of: multi_bar, late_students")
        return fig
    
    def handle_mode(self, mode):
        if mode == "absolute":
            y_column = "present_students"
            relative = False
            before_after = False
            
        elif mode == "relative_registered":
            y_column = "relative_registered"
            relative = True
            before_after = False
            
        elif mode == "relative_capacity":
            y_column = "relative_capacity"
            relative = True
            before_after = False
            
        elif mode == "before_after":
            y_column = "present_students"
            relative = False
            before_after = True
            
        else:
            raise ValueError("Mode must be one of: absolute, relative_registered, relative_capacity, before_after")

        return y_column, relative, before_after
        
            
    ##### One Course Particpants Bar Chart #####
    def generate_charts_before_after(self, fig, df, x, row, col):
        
            y = df["present_students_b"]
            fig.add_trace(
                go.Bar(
                    x=np.array(x) - 0.35, 
                    y=y, 
                    name="Before",
                    text=y,
                    width=0.2,
                    customdata=df),
                row=row, col=col)
            
            y = df["present_students"]
            fig = self.generate_bar_chart(fig, df, x, y, row=row, col=col)
            
            y = df["present_students_a"]   
            fig.add_trace(
                go.Bar( 
                    x=np.array(x) + 0.35, 
                    y=y,
                    name="After",
                    text=y,
                    width=0.2,
                    customdata=df),
                row=row, col=col)
            
            return fig

    def generate_bar_chart(self, fig, df, x, y, row, col):
        
        custom_data = df.copy()
        fig.add_trace(
            go.Bar(
                x=x, 
                y=y, 
                name="",
                text=y,
                textposition='auto',
                width=0.5,
                customdata=df),
            
            row=row, col=col)
        
        return fig
    
    def make_subplot_beforeafter(self, fig, df, row, col):
        
        x = list(range(len(df)))
        ticktext = df["start_time"].dt.strftime("%d.%m.%Y <br> %H:%M")
        
        fig = self.generate_charts_before_after(fig, df, x, row, col)
        fig = self.frequency_yaxis(fig=fig, row=row, col=col, relative=False, title=True)
        fig = self.date_xaxis(fig=fig, row=row, col=col, x=x, ticktext=ticktext) 
        
        return fig
        
    def make_subplot_chart(self, fig, df, y_col, row, col):
        x = list(range(len(df)))
        y = df[y_col]
        ticktext = df["start_time"].dt.strftime("%d.%m.%Y <br> %H:%M")
        
        if bool(re.search("relative", y_col)):
            relative = True
        else:
            relative = False
        
        fig = self.generate_bar_chart(fig=fig, df=df, x=x, y=y, row=row, col=col)
        fig = self.frequency_yaxis(fig=fig, row=row, col=col, relative=relative, title=True)
        fig = self.date_xaxis(fig=fig, row=row, col=col, x=x, ticktext=ticktext)

        return fig
        
    def plot_course_bar(self, dataframe):
    
        df = dataframe.copy()

        titles = ["Absolute Frequencies",
                  "Frequencies Relative to Registered Students", 
                  "Frequencies Relative to Room Capacity"]
        fig = make_subplots(rows=3, cols=1,
                            vertical_spacing=0.25,
                            subplot_titles=titles)
        
        
         # absolute frequency always on top
        fig = self.make_subplot_chart(fig=fig, df=df, y_col="present_students", row=1, col=1)
        #fig = self.make_subplot_beforeafter(fig=fig, df=df, row=1, col=2)
        fig = self.make_subplot_chart(fig=fig, df=df, y_col="relative_registered", row=2, col=1)
        fig = self.make_subplot_chart(fig=fig, df=df, y_col="relative_capacity", row=3, col=1)
        
        
        fig = self.apply_general_settings(fig)
        fig = self.customize_hover(fig=fig, mode="single_bar")
        fig.update_layout(showlegend=False)
        
        return fig
    
    def plot_empty_course_bar(self):
            
            fig = make_subplots(rows=1, cols=1)
            
            fig = self.add_title(fig, "No Course Selected")
            fig = self.apply_general_settings(fig)
            fig.update_layout(showlegend=False)
            fig.update_layout(margin=dict(t=100))
            
            return fig   
    
    
    ##### Multiple Courses Bar Chart #####
    def course_numbers_xaxis(self, fig, row, col, x, ticktext, n_rows):
        #if row == n_rows:
        #    title_text = "<b> Course Number </b>"
        #else:
        #    title_text = ""

        fig.update_xaxes(
            #title={
            #    "text":title_text,
            #    "font": {"size": self.axis_title_size}},
            automargin=True,
            tickvals=x,
            range=[-0.25, len(ticktext)+0.25],
            tickangle=0,
            ticktext=ticktext,
            row=row, col=col) 
         
        return fig
    
    def plot_multiple_courses_line(self, dataframe, lva_numbers, title):
        df = dataframe.copy()

        rows, cols = 1, 1
        fig=make_subplots(rows=rows, cols=cols)         

        for lva_number in lva_numbers:
            
            # filter by course number
            df_lva = df[df["course_number"] == lva_number]
            
            x = df_lva["start_time"]
            y = df_lva["present_students"]
            
            fig.add_trace(
                go.Scatter(
                    x=x, 
                    y=y, 
                    name=f"{lva_number}",
                    mode="lines"),
                row=1, col=1)
        
        fig = self.add_title(fig, title)
        
        fig = self.apply_general_settings(fig)
        
        fig.show(config=self.config)

    def generate_mulit_bar_plot(self, fig, y_column, df, course_numbers, row, col):
        
        for i,course_number in enumerate(course_numbers):
            
            df_course = df[df["course_number"] == course_number]
            
            n_dates = len(df_course)
            if n_dates < 4:
                offset = n_dates/8
                start = 0.5 - offset
                end = 0.5 + offset
                step_size = (end-start)/n_dates
                x = np.arange(start+(step_size/2), end, step_size) + i
            else:
                step_size = 0.8/n_dates                
                x = np.arange(0.1 + step_size/2, 0.9, step_size) + i
                
            if len(x) != n_dates:
                raise ValueError("Length of x and n_dates do not match", len(x), n_dates)
            
            y = df_course[y_column]
                                            
            fig.add_trace(
                go.Bar(
                    x=x, 
                    y=y,
                    name="",
                    width=step_size, 
                    customdata=df_course,),
                row=row, col=col)
            
        return fig
    
    def get_ticktext(self, course_numbers):
        labels = []
        for x in course_numbers:
            splitter = x.split(", ")
            if len(splitter) > 1:
                labels.append(splitter[0] + ",...")
            else:
                labels.append(x)
        return labels
    
    def customise_x_and_y_title(self, fig, x_title, y_title):
        
        for annotation in fig.layout.annotations:
            if annotation["text"] == x_title:
                annotation["text"] = f"<b>{annotation['text']}</b>"
                annotation["font"] = {"size": self.axis_title_size + 6}
                
            elif annotation["text"] == y_title:
                annotation["text"] = f"<b>{annotation['text']}</b>"
                annotation["font"] = {"size": self.axis_title_size + 6}
                annotation["xanchor"] = "center"
                annotation["yanchor"] = "middle"
                annotation["xshift"] = -80

            else:
                continue
            
        return fig
    
    def handle_mode_y_title(self, mode):
        if mode == "absolute":
            return "Absolute Frequency"
        elif mode == "relative_registered":
            return "Frequency Realtive to Registered Students"
        elif mode == "relative_capacity":
            return "Frequency Relative to Room Capacity"
        else:
            raise ValueError("Mode must be one of: absolute, relative_registered, relative_capacity")
        
    def plot_multiple_courses_bars(self, dataframe, course_numbers, mode):
        
        df = dataframe.copy()
        course_numbers = course_numbers.copy()
        df["start_time"] = df["start_time"].dt.strftime("%d.%m.%Y %H:%M")
        df["end_time"] = df["end_time"].dt.strftime("%H:%M")
        
        n_courses = len(course_numbers)
        n_rows = int(np.ceil(n_courses/8))
        course_indices = np.array_split(np.arange(n_courses), n_rows)
        n_cols = 1
            
        y_column, relative, _ = self.handle_mode(mode)
        
        #x_title = "Course Number"
        #y_title = "Onsite Participants" +  self.handle_mode_y_title(mode)
        #fig = make_subplots(rows=n_rows, cols=n_cols, 
        #                    y_title=y_title,
        #                    x_title=x_title,)
        fig = make_subplots(rows=n_rows, cols=n_cols)
        
        #fig = self.customise_x_and_y_title(fig, x_title, y_title)
        for row, indices in enumerate(course_indices, 1):
            chunk_course_numbers = [course_numbers[i] for i in indices]
            fig = self.generate_mulit_bar_plot(fig=fig, 
                                               y_column=y_column,
                                                df=df, 
                                                course_numbers=chunk_course_numbers, 
                                                row=row, col=1)

            ticktext = self.get_ticktext(chunk_course_numbers)
            fig = self.course_numbers_xaxis(fig, 
                                    row=row, col=n_cols, 
                                    x=np.arange(len(chunk_course_numbers))+0.5, 
                                    ticktext=ticktext,
                                    n_rows=n_rows)  
                          
            #fig = self.frequency_yaxis(fig=fig, row=row, col=n_cols, relative=relative, title=True)
        
        #fig = self.add_title(fig, title)
        if self.plot_height/n_rows > 200:
            self.plot_height = int(200*n_rows)
        else:
            self.plot_height = self.plot_height_provided
            
        fig = self.apply_general_settings(fig)
        fig = self.customize_hover(fig=fig, mode="multi_bar")
        fig.update_layout(showlegend=False)
        
        return fig

    #### Plot Grouped Bar Chart ####
    def calc_relative(self, dataframe, tartget_column, relative_to_column, out_column):
        df = dataframe.copy()
        df[out_column] = (df[tartget_column] / df[relative_to_column]).round(4)
        return df
    
    def handle_relative_mode(self, dataframe, mode, target_column, out_column):
        df = dataframe.copy()
        
        if mode == "relative_registered":
            df = self.calc_relative(df, target_column, "registered_students", out_column)

        elif mode == "relative_capacity":
            df = self.calc_relative(df, target_column, "room_capacity", out_column)
            
        else:
            raise ValueError("Mode must be one of: relative_registered, relative_present")
        
        return df
    
    def make_hover_template(self, df, group_by):
        columns = df.columns
        template = ""
        for x in group_by:
            idx = columns.get_loc(x)
            #"%{customdata[9]}: %{customdata[8]}<br>" +
            template += f"{x}:"+ " %{customdata["+f"{idx}"+"]}<br>"
        return template
            
    def plot_grouped_bar(self, dataframe, group_by, mode):
        df = dataframe.copy()
        
        # duration as a string
        df["duration"] = df["duration"].astype(str)    
        # handle mode
        y_column, relative, _ = self.handle_mode(mode)
        
        if relative:
            df = self.handle_relative_mode(df, mode, "present_students", y_column)
        
        fig = make_subplots(rows=1, cols=1)
        
        if len(group_by) == 1:
            x = df[group_by[0]]        
        else:    
            x = [df[col] for col in group_by]
        y = df[y_column]
        
        # we could add a color scheme
        # color_list = ?
        fig.add_trace(
            go.Bar(
                alignmentgroup=2,
                x=x, 
                y=y, 
                name="",
                text=y,
                textposition='auto',
                width=0.6,
                customdata=df))
        
        fig = self.apply_general_settings(fig)
        fig = self.frequency_yaxis(fig=fig, row=1, col=1, relative=relative, title=True)
        fig.update_xaxes(
            title={
                "text":"<b>"+", ".join(group_by)+"</b>",
                "font": {"size": self.axis_title_size}},
            automargin=True,
            row=1, col=1) 
        
        template = self.make_hover_template(df, group_by)
        fig = self.customize_hover(fig, "grouped_bar", template=template)
        return fig
        
    def plot_empty_grouped_bar(self):
            
            fig = make_subplots(rows=1, cols=1)
            
            fig = self.add_title(fig, "Please select a feature to group by!")
            fig = self.apply_general_settings(fig)
            fig.update_layout(margin=dict(t=100))
            fig.update_layout(showlegend=False)
            
            return fig   


    ##### Charts for Attendance Dynamics #####
    def calc_relative_registered(self, dataframe, column):
        df = dataframe.copy()
        df["relative_registered"] = df[column] / df["registered_students"]
        return df
    
    def calc_relative_capacity(self, dataframe, column):
        df = dataframe.copy()
        df["relative_capacity"] = df[column] / df["room_capacity"]
        return df
    
    def calc_relative_present(self, dataframe, column):
        df = dataframe.copy()
        df["relative_present"] = df[column] / df["present_students"]
        return df
    
    def apply_mode(self, dataframe, mode):
        if mode == "relative_registered":
            return self.calc_relative_registered(dataframe)
        elif mode == "relative_present":
            return self.calc_relative_present(dataframe)
        else:
            raise ValueError("Mode must be one of: relative_registered, relative_present")
               
    def late_students_prepare(self, dataframe, room_id, mode):
        df = dataframe.copy()
        df["time"] = df["start_time"].dt.strftime("%d.%m.%Y %H:%M")
        df = self.filter_by_room(df, room_id).sort_values(by="late_students", ascending=False)
        
        if mode == "absolute":
            df["x"] = df["time"]
            df["y"] = df["late_students"]
            
        elif mode == "relative_present":
            df = self.calc_relative_present(df, "late_students").sort_values(by="relative_present", ascending=False)
            df["x"] = df["time"]
            df["y"] = df["relative_present"]
            
        elif mode == "relative_registered":
            df = self.calc_relative_registered(df, "late_students").sort_values(by="relative_registered", ascending=False)
            df["x"] = df["time"]
            df["y"] = df["relative_registered"]
        
        else:
            raise ValueError("Mode must be one of: absolute, relative_present")

        return df
        
    def plot_late_students(self, dataframe):
        
        fig = make_subplots(rows=1, cols=1)
        
        df = dataframe.copy()
        
        fig.add_trace(
            go.Bar(
                x=df["x"], 
                y=df["y"],
                name="",
                customdata=df),
            row=1, col=1)
        
        #fig = self.add_title(fig, title)
        fig = self.apply_general_settings(fig)
        
        fig = self.customize_hover(fig, mode="late_students")
        fig.show(config=self.config)     


############# Pandas ############
#    def filter_greater_than(self, dataframe, column, value):
#        df = dataframe.copy()
#        return df[df[column] > value]
    

    #def plot_early_leaving_students(self, fig, df_hs18, df_hs19, top_n):
        
    #    df1 = df_hs18.copy()
    #    df1 = self.filter_greater_than(df1[:top_n], "leaving_early_students", 0)
    #    fig.add_trace(
    #        go.Bar(
    #            x=df1["start_time"], 
    #            y=df1["leaving_early_students"],
    #            name="HS 18"),
    #        row=2, col=1)
        
    #    df2 = df_hs19.copy()
    #    df2 = self.filter_greater_than(df2[:top_n], "leaving_early_students", 0)
    #    fig.add_trace(
    #        go.Bar(
    #            x=df2["start_time"], 
    #            y=df2["leaving_early_students"],
    #            name="HS 19"),
    #        row=2, col=2)       
        
    #    return fig
        
                   
    #def plot_dynamics(self, dataframe, mode):
        
    #    fig = make_subplots(rows=2, cols=2)
        
    #    df = dataframe.copy()
    #    df["start_time"] = df["start_time"].dt.strftime("%d.%m.%Y %H:%M")
        
    #    if mode == "relative_registered":
    #        df["late_students"] = df["late_students"] / df["registered_students"]
    #        df["leaving_early_students"] = df["leaving_early_students"] / df["registered_students"]
    #        relative=True
    #    elif mode == "relative_present":
    #        df["late_students"] = df["late_students"] / df["present_students"]
    #        df["leaving_early_students"] = df["leaving_early_students"] / df["present_students"]
    #        relative=True
    #    elif mode == "absolute":
    #        relative=False
    #    else:
    #        raise ValueError("Mode must be one of: relative_registered, absolute")
        
    #    top_n = 25
          
    #    df_hs19 = self.filter_by_room(df, 1).sort_values(by="late_students", ascending=False)
    #    df_hs18 = self.filter_by_room(df, 0).sort_values(by="late_students", ascending=False)
        
    #    fig = self.plot_late_students(fig, df_hs18, df_hs19, top_n=top_n)
        
    #    df_hs19 = df_hs19.sort_values(by="leaving_early_students", ascending=False)
    #    df_hs18 = df_hs18.sort_values(by="leaving_early_students", ascending=False)
    #    fig = self.plot_early_leaving_students(fig, df_hs18, df_hs19, top_n=top_n)

    #    #fig = self.add_title(fig, title)
    #    fig = self.apply_general_settings(fig)
    #    fig.show(config=self.config)
    
    
    
    
        # def plot_course_bar(self, dataframe):
    
        # df = dataframe.copy()
        
        # #y_column, realtive, before_after = self.handle_mode(mode)
        
        # if show_relative:
            
        #     if show_before_after:
        #         raise ValueError("Only one of show_relative and show_before_after can be True")
            
        #     else:
        #         rows, cols = 2, 1
        #         fig = make_subplots(rows=rows, 
        #                             cols=cols, 
        #                             shared_xaxes=True,
        #                             subplot_titles=("Absolute Frequencies", "Frequencies Relative to Registered Students"))
                
        #         fig = self.generate_particpants_bar_chart(fig=fig, df=df)
        #         fig = self.generate_relative_bar_chart(fig=fig, df=df)
                
        #         fig.update_layout(showlegend=False)
        #         fig = self.frequency_yaxis(fig=fig, 
        #                                    row=2, col=1, 
        #                                    relative=True)
            
        # else:
        #     rows, cols = 1, 1
        #     fig=make_subplots(rows=rows, cols=cols)    
                    
        #     if show_before_after:
        #         fig = self.generate_charts_before_after(fig, df)
                
        #     else:
        #         fig = self.generate_particpants_bar_chart(fig, df) 
        
        # # absolute frequency always on top    
        # fig = self.frequency_yaxis(fig=fig, 
        #                             row=1, col=1, 
        #                             relative=False)
        
        # # x-axis settings
        # fig = self.date_xaxis(fig=fig,
        #                       row=rows, col=cols,
        #                       x=list(range(len(df))),
        #                         ticktext=df["start_time"].dt.strftime("%d.%m.%Y <br> %H:%M"))
        
        # # get name of course
        # row = df.iloc[0]
        # name = row["course_name"]
        # title = f"<b>{name}</b> <br> Participants per Course Date <br>"
        # fig = self.add_title(fig, title)
        
        # fig = self.apply_general_settings(fig)
        
        # fig.show(config=self.config)