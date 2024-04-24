import { showAlert } from './alerts.js';

var issueReport = {}
var reportingIssue = false;
var selectedElement = null;

function handleClick(event){
    if (reportingIssue && event.target !== $("#reportIssueBtn")[0]){
        event.preventDefault();
        event.stopPropagation();
    }
}

function handleKeyDown(event){
    if (reportingIssue && event.key === 'Escape'){
        exitReportingState();
    }
}

function handleMouseMove(event){
    var target = event.target;

    if (selectedElement && selectedElement !== target){
        selectedElement.classList.remove('hovered');
    }

    target.classList.add('hovered');
    selectedElement = target;
}

function enterReportingState(){
    reportingIssue = true;
    var alertDivMessage = "Click on where you see the issue";
    var alertType = 'info';
    showAlert(alertDivMessage, alertType);
    $("#reportIssueText").text('Cancel');
    $('body').css('cursor', 'crosshair');
    $('body').on('click', handleIssueReportClick);
    $('body').on('mousemove', handleMouseMove);
    $(document).on('click',handleClick);
    $(document).on('keydown',handleKeyDown);

    if (selectedElement){
        selectedElement.classList.remove('hovered');
        selectedElement = null;
    }

}

function exitReportingState(){
    reportingIssue = false;
    $("#reportIssueText").text('Report Issue');
    $('body').css('cursor','default');
    $('body').off('click',handleIssueReportClick);
    $('body').off('mousemove', handleMouseMove);
    $(document).off('click',handleClick);
    $(document).off('keydown',handleKeyDown);

    if (selectedElement){
        selectedElement.classList.remove('hovered');
        selectedElement = null;
    }
}

$("#reportIssueBtn").on('click',function(){
    event.stopPropagation();

    if (!reportingIssue){
        enterReportingState();
    } else {
        exitReportingState();
    }
});

function handleIssueReportClick(event){
    if (reportingIssue && event.target !== $("#reportIssueBtn")[0]){
        var target = event.target;

        // Remove the event listener for mouse move
        $('body').off('mousemove', handleMouseMove);

        var pageUrl = window.location.href;
        var elementType = target.tagName.toLowerCase();
        var elementId = target.id;
        var elementClass = target.className;
        var elementText = $(target).text().trim();

        // Check if the clicked element is a table cell
        var tableCellInfo = {};
        if (elementType == 'td'){
            var $cell = $(target);
            var $row = $cell.closest('tr');
            var $table = $row.closest('table');
            var rowIndex = $row.index();
            var columnIndex = $cell.index();
            var tableId = $table.attr('id');
            var rowName = $row.find('td:first-child').text().trim();
            var columnName = $table.DataTable().column(columnIndex).header().innerHTML;

            tableCellInfo = {
                tableId: tableId,
                rowIndex: rowIndex,
                columnIndex: columnIndex,
                rowName: rowName,
                columnName: columnName
            };
        }

        // Capture a screenshot of the website
        html2canvas(document.body).then(function(canvas){
            var captureDataUrl = canvas.toDataURL('image/png');
            
            // Create an object with the issue reporting data
        issueReport = {
            pageUrl: pageUrl,
            elementType: elementType,
            elementId: elementId,
            elementClass: elementClass,
            elementText: elementText,
            tableCellInfo: tableCellInfo,
            captureDataUrl: captureDataUrl
        };

        // Create a formatted string for the report details
        var reportDetails = "Page URL: " + issueReport.pageUrl + "\n" +
                            "Element Type: " + issueReport.elementType + "\n" +
                            "Element ID: " + issueReport.elementId + "\n" +
                            "Element Class: " + issueReport.elementClass + "\n" +
                            "Element Text: " + issueReport.elementText + "\n" +
                            "Table Cell Info: " + JSON.stringify(issueReport.tableCellInfo, null, 2);

            $("#reportDetails").text(reportDetails);

            // Show the modal
            $("#report-modal").modal('show');
            
            exitReportingState();
        });
    }
}

$("#sendReportBtn").on('click', function() {
    var feedback = $('#reportFeedback').val();
    var customIssue = $("#customIssueText").val();
  
    if (customIssue) {
      issueReport.customIssue = customIssue;
    }
  
    $.ajax({
      url: '/report-issue',
      type: 'POST',
      data: JSON.stringify({ feedback: feedback, reportDetails: issueReport }),
      contentType: 'application/json',
      success: function(response) {
        $('#report-modal').modal('hide');
        showAlert('Issue reported successfully!', 'success');
      },
      error: function(xhr, status, error) {
        console.error('Error reporting issue:', error);
        showAlert('Failed to report issue. Please try again.', 'danger');
      }
    });
});

$("#customReportBtn").on('click', function() {
    $("#customIssueText").val('');
    $("#reportFeedback").val('');
    $("#report-modal").modal('show');
  });
  
  $("#submitCustomReportBtn").on('click', function() {
    var customIssue = $("#customIssueText").val();
  
    if (customIssue) {
      issueReport = {
        pageUrl: window.location.href,
        customIssue: customIssue
      };
  
      $.ajax({
        url: '/report-issue',
        type: 'POST',
        data: JSON.stringify({ reportDetails: issueReport }),
        contentType: 'application/json',
        success: function(response) {
          $("#customReportModal").modal('hide');
          $("#reportDetails").text('Enter report details above');
          showAlert('Custom issue reported successfully!', 'success');
        },
        error: function(xhr, status, error) {
          console.error('Error reporting custom issue:', error);
          showAlert('Failed to report custom issue. Please try again.', 'danger');
        }
      });
    }
  });

$('#report-modal').on('hidden.bs.modal', function(e) {
    issueReport = {};
    $("#reportDetails").text('');
});