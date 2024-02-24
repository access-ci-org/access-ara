$(document).ready(function(){
    $("#app_content").removeClass()
    $("#app_content").addClass('col')

    // Function to make URLs clickable
    function makeLinkClickable(data) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return data.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank">' + url + '</a>';
        });
    }

    var staticTable = $('#softwareTable').DataTable({
        dom:'Qlfrtip',
        "sScrollX": "100%",
        "autoWidth": true,
        columnDefs: [{
                targets: [5, 6,7,8,9,10], // Direct URL columns
                render: function(data, type, row) {
                    if (type === 'display' && data) {
                        return makeLinkClickable(data);
                    }
                    return data;
                }
            }]
    });

    var dynamicTable = $('#softwareTableDynamic').DataTable({
        dom:'Qlfrtip',
        "sScrollX": "100%",
        "autoWidth": true,
    });

});