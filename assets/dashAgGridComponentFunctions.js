var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

dagfuncs.rowSpanningComplex = function (params) {
    console.log(params.data);
    if (params.data == "361.001") {
        return 4;
    } else {
        return 1;
    }
}