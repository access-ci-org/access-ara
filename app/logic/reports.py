from datetime import datetime

def sanitize_and_process_reports(issue_report):
    feedback = issue_report.get('feedback', '')
    report_details = issue_report['reportDetails']
    page_url = report_details['pageUrl']
    element_type = report_details.get('elementType', '')
    element_id = report_details.get('elementId', '')
    element_class = report_details.get('elementClass', '')
    element_text = report_details.get('elementText', '')
    table_cell_info = report_details.get('tableCellInfo', {})
    capture_data_url = report_details.get('captureDataUrl', '')
    custom_issue = report_details.get('customIssue', '')
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    capture_filename = f"issue_{current_datetime}.png"
    report = {
        "datetime": current_datetime,
        "pageUrl": page_url,
        "elementType": element_type,
        "elementId": element_id,
        "elementClass": element_class,
        "elementText": element_text,
        "tableCellInfo": table_cell_info,
        "feedback": feedback,
        "customIssue": custom_issue,
        "captureFilename": capture_filename,
        "captureDataUrl": capture_data_url
    }
    return report