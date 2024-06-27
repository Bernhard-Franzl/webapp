from dash import html


def initialize_layout(id):
    return html.Div(
        className="details-info-container",
        id=id
    )
    
   
def generate_course_info(dataframe):
    df = dataframe.copy()
    first_row = df.iloc[0]
    # time 
    if df["start_time"].dt.time.nunique() == 1:
        time = f"{first_row['start_time'].strftime('%H:%M')} - {first_row['end_time'].strftime('%H:%M')}"
    else:
        time = "Irregular"
        
    if df["weekday"].nunique() == 1:
        weekday = first_row["weekday"]
    else:
        weekday = "Irregular    "
    
    return [
            html.Div(
                children=first_row["course_name"],
                className="plot--course-info-title"
            ),
            html.Table(
                className="plot--course-info-table",
                children=[
                    # ID
                    generate_table_row("ID:", first_row["course_number"]),
                    # Type
                    generate_table_row("Type:", first_row["type"]),
                    # Registered
                    generate_table_row("Registered:", first_row["registered_students"]),
                    # Room 
                    generate_table_row("Room:", first_row["room"]),
                    # Room Capacity
                    generate_table_row("Room Capacity:", first_row["room_capacity"]),
                    # Weekday
                    generate_table_row("Weekday:", weekday),
                    # Time
                    generate_table_row("Time:", time),
                    # No. of dates
                    generate_table_row("No. of Dates:", df["start_time"].nunique())
                ]
            )
        ]
    
def generate_table_row(label, text):
    return html.Tr(
        className="plot--course-info-table-row",
        children=[
            html.Td(label, 
                    className="plot--course-info-table-label"),
            html.Td(text,
                    className="plot--course-info-table-element")
        ]
    )
    

#if header_config["course_info"]:
#    out_list.append(Output("course_info", "children"))
        
        
#def generate_info_element(label, text):
#    return html.Div(
#        className="plot-header--info-element",
#        children=[
#            html.Div(
#                label, 
#                className="plot-header--info-element-label"
#            ),
#            html.Div(
#                text,
#                className="plot-header--info-element-text"
#            )
#        ]
#    )