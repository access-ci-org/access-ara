$(document).ready(function(){
    $("#app_content").removeClass()
    $("#app_content").addClass('col')

    var page_title = $("#page_title");
    var path=window.location.pathname;

    if (path.includes('dynamic')){
        page_title.text('ACCESS Software Documentation Service (Dynamic)')
    } else{
        page_title.text('ACCESS Software Documentation Service (Static)')
    }

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
                targets: [5, 6,7,8,9], // Direct URL columns
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
        columnDefs:[
            {
                targets:9,
                render: function(data, type, row){
                    return '<button class="btn btn-info example-use-btn" type="button">Use Example</button>';
                }

            },
            {
                targets: [10,11,12],
                render: function(data, type, row){
                    if (type=='display' && data){
                        return makeLinkClickable(data);
                    }
                    return data;
                }
            }
        ]
    });


    // Initialize a Showdown converter with the Highlight.js extension
    var converter = new showdown.Converter({
        extensions: [highlightExtension]
    });


    dynamicTable.on('click','.example-use-btn', function(e){
        let rowData = dynamicTable.row(e.target.closest('tr')).data();
        var softwareName = rowData[0];
        var encodedSoftwareName = encodeURIComponent(softwareName);
        $.ajax({
            url: "/example_use/"+encodedSoftwareName,
            type:"GET",
            success: function(response){

                var useHtml = converter.makeHtml(response.use)
                $(".modal-title").html('Use Case for '+softwareName)
                $('#useCaseBody').html(useHtml);

                document.querySelectorAll('#useCaseBody pre Code').forEach((block)=>{
                    hljs.highlightBlock(block)
                })

                $('.modal').modal('show');
            },
            error: function(xhr, status, error){
                console.error("Error fetching example use: ", error);
            }
        })
    })

    var columnIndex = dynamicTable.column(':contains("Example Use")').index();
    console.log(columnIndex)
});

// Define the Highlight.js extension for Showdown
function highlightExtension() {
    return [{
        type: 'output',
        filter: function (text, converter, options) {
            var left = '<pre><code\\b[^>]*>',
                right = '</code></pre>',
                flags = 'g',
                replacement = function (wholeMatch, match, left, right) {
                    match = match.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                    return left + hljs.highlightAuto(match).value + right;
                };
            return showdown.helper.replaceRecursiveRegExp(text, replacement, left, right, flags);
        }
    }];
}

