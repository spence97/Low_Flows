// the DOM tree finishes loading
$(document).ready(function() {
    // Initialize Global Variables
    var ol_map = TETHYS_MAP_VIEW.getMap();
    $("#watershedselect").on(change,function(e){
        console.log(e);
    });
});

