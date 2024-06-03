
var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.RowSpanningComplexCellRenderer = function (props) {

    //var fieldName = params.colDef.field;
    //var fieldData = params.data[fieldName];
    //const time = params.data.time;

    // try to extract duration from context else default to 1
    //var context = props.context[fieldName][time];

    let children;
    if (props.value) {
        //console.log(props);
        var courseNumber = props.value;
        var weekDay = props.column.colId;
        var time = props.data.time;

        var context = props.context[weekDay][time];
        console.log(courseNumber, context);

        children = [
            
            React.createElement('div', {className: 'calendar--entry-course-number'}, props.value.length > 7 ? props.value.slice(0, 7).concat("...") : props.value),
            React.createElement('div', {className: 'calendar--entry-course-name'}, context["type"].concat(": ", context['course_name'])),
        ]
        return React.createElement('div', {className: 'calendar--entry'}, children)
    }else{
        return React.createElement('div', {className: 'calendar--empty-cell'}, null)
    }
}

//dagcomponentfuncs.TimeCellRenderer = function (props) {
//    console.log(props);
//    return React.createElement('div', {className: 'calendar--time-cell'}, props.valueFormatted)
//}