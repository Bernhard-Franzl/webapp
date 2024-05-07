from matplotlib import pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

class Visualizer():
    def __init__(self, path="plots/", figsize=(10,5)):
        # maybe some general settings like style and window size
        # also the path where the plots are saved
        self.path = path
        self.figsize = figsize
        
        # font settings
        self.font_family = "Arial, sans-serif"
        self.axis_title_size = 18
        self.text_size = 14
        self.title_size = 25
        
        # format settings
        self.plot_height = 750

        # plotly config
        self.config={
            "responsive": True,
            'scrollZoom': True,
            "displaylogo": False,
            "displayModeBar": True,
            "modeBarButtonsToRemove": 
                ["select", "zoomIn", "zoomOut", "autoScale", "lasso2d"]}


############ Matplotlib ############
      
    ##### Plot Particpants Algorithm - How it works #####  
    def merge_participant_dfs(self, dataframes:list):
        
        if len(dataframes) != 3:
            raise ValueError("Expected 3 dataframes, got: ", len(dataframes))
        else:
            
            def correct_dataframes(dataframes, cur_last):
                # if dataframes is list
                df_list = []
                if type(dataframes) == list:
                    for df, info in dataframes:
                        pos, col = info.split("_")
                        
                        if col == "out":
                            df["people_out"] = df["people_out"] - df.iloc[0]["people_out"]
                            df["people_inside"] =  (-df["people_out"]) + cur_last
                            cur_last = cur_last + df.iloc[-1]["people_inside"]
                            df_list.append(df)
                            
                            
                        elif col == "in":
                            if cur_last != 0:
                                raise ValueError("First dataframe should start with 0 people inside")
                            
                            df["people_inside"] = df["people_in"] + cur_last
                            cur_last =  df.iloc[-1]["people_inside"]
                            df_list.append(df)

                            
                        else:
                            if pos == "before":
                                df["people_inside"] = df["people_inside"] - df.iloc[0]["people_inside"] + cur_last
                                cur_last = df.iloc[-1]["people_inside"]
                                df_list.append(df)
                                
                            if pos == "after":
                                df["people_inside"] = df["people_inside"] + cur_last
                                cur_last = df.iloc[-1]["people_inside"]
                                df_list.append(df)
            
                    return df_list, cur_last
                                
                else:
                    dataframes["people_inside"] = dataframes["people_inside"] + cur_last
                    cur_last = dataframes.iloc[-1]["people_inside"]
                    return [dataframes], cur_last
            
            df_list = []
            cur_last = 0
            for x in dataframes:        
                dfs, cur_last = correct_dataframes(x, cur_last)
                df_list += dfs

        return pd.concat(df_list).reset_index(drop=True)
    
    def plot_participants_algo(self, file_name, participants=None, 
                        df_list=None, control=None, 
                        extrema=None, horizontal_lines=[], title=None):
        
        if (participants is None) and (df_list is None) and (control is None):
            raise ValueError("Either participants, df_list or control must be provided")
        
        else:
            legend = []
            fig, ax = plt.subplots(figsize=self.figsize)
            
            if participants is not None:
                participants.plot(x="time", y="people_inside", kind="line", ax=ax)
                legend.append("participants")
            
            if df_list is not None:
                for df in df_list:
                    df.plot(x="time", y="people_inside", kind="line", ax=ax)
                    legend.append("control")
            
            if control is not None:
                control.plot(x="time", y="people_inside", kind="line", ax=ax)
                legend.append("simple")
                
            if extrema is not None:
                extrema.plot(x="time", y="min", kind="scatter", ax=ax, c="r")
                legend.append("min")
                extrema.plot(x="time", y="max", kind="scatter", ax=ax, c="g")
                legend.append("max")
            
            
            if len(horizontal_lines) > 0:
                for x, c, l in horizontal_lines:
                    plt.axhline(y = x, c=c, linestyle = '-')
                    legend.append(f"{l}")
                    
            if title is not None:
                plt.title(title)
                
            plt.legend(legend)
            plt.grid()
            fig.savefig(self.path + file_name)
            
            plt.close()


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
                'xanchor':'center',
                "automargin":True},)
        
        return fig
             
    def apply_general_settings(self, fig):
        
        # general layout settings
        fig.update_layout(
            barmode='group',
            dragmode='pan',
            font=dict(
                family=self.font_family,
                size=self.text_size,),
            minreducedheight=self.plot_height//4,
            height=self.plot_height)

        return fig

    def customize_yaxis(self, fig, title, range, row, col):
        
        fig.update_yaxes(
            title={
                "text": title,
                "font": {"size": self.axis_title_size}},
            range=range,
            automargin=True)

        
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
    
    def customize_hover(self, fig, mode="multi_bar"):
        if mode == "multi_bar":
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                            "Title: %{customdata[8]}<br>" +
                            "Y: %{y}<br>" +
                            "Present:%{customdata[19]} | Registered:%{customdata[16]}<br>" +
                            "Start Time: %{customdata[1]} %{customdata[5]}<br>" +
                            "Room:%{customdata[2]} | Capacity:%{customdata[7]} <br>"+
                            "Irregular: %{customdata[27]}<br>" +
                            "Note: %{customdata[3]}")
        return fig
    
    ##### One Course Particpants Bar Chart #####
    def generate_charts_before_after(self, fig, df):
        
            x = list(range(len(df)))
            y = df["present_students_b"]
                
            fig.add_trace(
                go.Bar(
                    x=x, 
                    y=y, 
                    name="Before",
                    text=y,
                    width=0.1),
                row=1, col=1)
            
            fig = self.generate_particpants_bar_chart(fig, df)
            
            y = df["present_students_a"]   
            fig.add_trace(
                go.Bar( 
                    x=x, 
                    y=y,
                    name="After",
                    text=y,
                    width=0.1),
                row=1, col=1)
            
            return fig
    
    def generate_particpants_bar_chart(self, fig, df):
        
        x = list(range(len(df)))
        y = df["present_students"]
        
        fig.add_trace(
            go.Bar(
                x=x, 
                y=y, 
                name="Combined",
                text=y,
                textposition='auto',
                width=0.4),
            row=1, col=1)
        
        return fig
    
    def generate_relative_bar_chart(self, fig, df):
        
        x = list(range(len(df)))
        y = (df["present_students"] / df["registered_students"]).round(4)
        
        fig.add_trace(
            go.Bar(
                x=x, 
                y=y, 
                name="Relative_Counts",
                text=y,
                textposition='auto',
                width=0.4),
            
            row=2, col=1)
        
        return fig
    
    def plot_course_bar(self, dataframe, course_number, show_relative=False, show_before_after=False):
    
        df = dataframe.copy()
         
        if show_relative:
            
            if show_before_after:
                raise ValueError("Only one of show_relative and show_before_after can be True")
            
            else:
                rows, cols = 2, 1
                fig = make_subplots(rows=rows, 
                                    cols=cols, 
                                    shared_xaxes=True,
                                    subplot_titles=("Absolute Frequencies", "Frequencies Relative to Registered Students"))
                
                fig = self.generate_particpants_bar_chart(fig=fig, df=df)
                fig = self.generate_relative_bar_chart(fig=fig, df=df)
                
                fig.update_layout(showlegend=False)
                fig = self.frequency_yaxis(fig=fig, 
                                           row=2, col=1, 
                                           relative=True)
            
        else:
            rows, cols = 1, 1
            fig=make_subplots(rows=rows, cols=cols)    
                    
            if show_before_after:
                fig = self.generate_charts_before_after(fig, df)
                
            else:
                fig = self.generate_particpants_bar_chart(fig, df) 
        
        # absolute frequency always on top    
        fig = self.frequency_yaxis(fig=fig, 
                                    row=1, col=1, 
                                    relative=False)
        
        # x-axis settings
        fig = self.date_xaxis(fig=fig,
                              row=rows, col=cols,
                              x=list(range(len(df))),
                                ticktext=df["start_time"].dt.strftime("%d.%m.%Y <br> %H:%M"))
        # get name of course
        row = df.iloc[0]
        name = row["course_name"]
        title = f"<b>{name}</b> <br> Participants per Course Date <br>"
        fig = self.add_title(fig, title)
        
        fig = self.apply_general_settings(fig)
        
        fig.show(config=self.config)
        
    ##### Multiple Courses Bar Chart #####
    def course_numbers_xaxis(self, fig, row, col, x, ticktext, n_rows):
        if row == n_rows:
            title_text = "<b> Course Number </b>"
        else:
            title_text = ""

        fig.update_xaxes(
            title={
                "text":title_text,
                "font": {"size": self.axis_title_size}},
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
    
    def plot_multiple_courses_bars(self, dataframe, course_numbers, title, mode):
        
        df = dataframe.copy()
        course_numbers = sorted(course_numbers.copy())
        
        df["start_time"] = df["start_time"].dt.strftime("%d.%m.%Y %H:%M")
        
        n_courses = len(course_numbers)
        n_rows = int(np.ceil(n_courses/15))
        course_indices = np.array_split(np.arange(n_courses), n_rows)
        n_cols = 1
        
        if mode == "absolute":
            y_column = "present_students"
            relative = False
        
        elif mode == "relative_registered":
            y_column = "relative_registered"
            relative = True
            
        elif mode == "relative_capacity":
            y_column = "relative_capacity"
            relative = True
            
        else:
            raise ValueError("Mode must be one of: absolute, relative_registered, relative_capacity")

            
        fig = make_subplots(rows=n_rows, cols=n_cols)

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
            fig = self.frequency_yaxis(fig=fig, row=row, col=n_cols, relative=relative, title=True)
        
        fig = self.add_title(fig, title)
        fig = self.apply_general_settings(fig)
        fig = self.customize_hover(fig=fig, mode="multi_bar")
        
        fig.update_layout(showlegend=False)
        fig.show(config=self.config)

    ##### Charts for Attendance Dynamics #####
    
    #def plot_dynamics_single_course(self, attend):
    # detailed version of the below function -> only one course date!
    
    def plot_dynamics(self, attendance_dynamics:tuple):
        
        df_coming_late, df_leaving_early, df_list_entering_during, df_list_leaving_during = attendance_dynamics
        
        fig = make_subplots(rows=3, cols=2,
                            specs=[[{"colspan": 2}, None],
                                   [{"colspan": 2}, None],
                                   [{},{}]])
        
        print(df_coming_late)
        fig.add_trace(
            go.Bar(
                x=df_coming_late["time"], 
                y=df_coming_late["diff_inside"],
                name="",
                customdata=df_coming_late),
            row=1, col=1)
            
        fig.show()