
var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.RowSpanningComplexCellRenderer = function (props) {

    //var fieldName = params.colDef.field;
    //var fieldData = params.data[fieldName];
    //const time = params.data.time;

    // try to extract duration from context else default to 1
    //var context = props.context[fieldName][time];

    let children;
    if (props.value) {

        var courseNumber = props.value;
        var weekDay = props.column.colId;
        var time = props.data.time;

        var context = props.context[weekDay][time];
        //console.log(context);
        var mode = context["mode"];
        
        children = [
            React.createElement('div', {className: 'calendar--entry-course-number'}, props.value.length > 7 ? props.value.slice(0, 7).concat("...") : props.value),
            React.createElement('a', {href: "/details/" + courseNumber, className:'calendar--entry-course-name'}, context["type"].concat(": ", context['course_name'])),
            React.createElement('div', {className: 'calendar--entry-course-time'}, context['time_span_str']),
            React.createElement('div', {className: 'calendar--entry-course-time'}, "Present".concat(": ", context['present_students'])),
            React.createElement('div', {className: 'calendar--entry-course-time'}, "Relative Freq.".concat(": ", context[mode])),
        ]
        relInt = Math.round(context[mode]*100)
        relBot= String(relInt).concat("%")
        relTop = String(100-relInt).concat("%")
        return React.createElement('div', {className:'calendar--entry-wrapper'},[
            React.createElement(
                'div', 
                {className: 'calendar--entry-background-bot', style: {height: relBot}}, null),
            React.createElement(
                'div', 
                {className: 'calendar--entry-background-top', style: {height: relTop}}, null),
            React.createElement('div', {className: 'calendar--entry'}, children)
        ])
        //return React.createElement('div', {className: 'calendar--entry'}, children)
    }else{
        return React.createElement('div', {className: 'calendar--empty-cell'}, null)
    }
}

//dagcomponentfuncs.TimeCellRenderer = function (props) {
//    console.log(props);
//    return React.createElement('div', {className: 'calendar--time-cell'}, props.valueFormatted)
//}