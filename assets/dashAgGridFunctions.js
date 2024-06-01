var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.rowSpanningComplex = function (params) {

    var fieldName = params.colDef.field;
    var fieldData = params.data[fieldName];
    const time = params.data.time;

    // try to extract duration from context else default to 1
    var context = params.context[fieldName][time];
    if (context === undefined) {
        return 1;
    }
    else if (fieldData === context['course_number']) {
        return context['duration']/15;
    } else {
        return 1;
    }
}
