var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.rowSpanningComplex = function (params) {

    var fieldName = params.colDef.field;
    var fieldData = params.data[fieldName];
    console.log(fieldName, params);
    
    if (fieldData === "340.100") {
        return 4;
    } else {
        return 1;
    }
}