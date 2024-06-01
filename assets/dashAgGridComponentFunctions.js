
var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.RowSpanningComplexCellRenderer = function (props) {
    let children;
    if (props.value) {
        children = [
            React.createElement('div', {className: 'calendar--course-number'}, props.value),
            // we can add more elements here
        ]
    }
    return React.createElement('div', null, children)
}