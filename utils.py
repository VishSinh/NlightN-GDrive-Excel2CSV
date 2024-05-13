import io
import pandas as pd

from services import gdrive_services
from googleapiclient.http import MediaIoBaseDownload


def get_drive_folders():
    try:
        service = gdrive_services()
        print('Service:',service)
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q="mimeType='application/vnd.google-apps.folder'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            return response.get('files', [])

    except Exception as error:
        print(f"An error occurred: {error}")
        files = None

def list_excel_files(folder_id):
    service = gdrive_services()
    print('Folder ID:',folder_id)
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    print('Results:',results)
    return results.get('files', [])

def download_and_convert_to_csv(file_id, file_name):
    service = gdrive_services()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    xls = pd.ExcelFile(fh)
    csv_paths = [convert_sheet_to_csv(xls, sheet, f"{file_name}_{sheet}.csv") for sheet in xls.sheet_names]
    return csv_paths

def convert_sheet_to_csv(xls, sheet_name, csv_path):
    df = pd.read_excel(xls, sheet_name=sheet_name)
    df.to_csv(csv_path, index=False)
    return csv_path