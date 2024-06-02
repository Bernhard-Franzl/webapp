
var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.RowSpanningComplexCellRenderer = function (props) {
    let children;
    console.log(props);
    if (props.value) {
        children = [
            React.createElement('div', {className: 'calendar--entry-course-number'}, props.value),
            // we can add more elements here
        ]
        return React.createElement('div', {className: 'calendar--entry'}, children)
    }else{
        return React.createElement('div', {className: 'calendar--empty-cell'}, null)
    }
}