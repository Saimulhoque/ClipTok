# from flask import Flask, render_template, request, flash, jsonify
# import os
# import yt_dlp
# import threading

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Required for flashing messages

# # Directory to save downloaded TikTok videos
# DOWNLOAD_FOLDER = 'tiktok_videos'
# if not os.path.exists(DOWNLOAD_FOLDER):
#     os.makedirs(DOWNLOAD_FOLDER)

# # Global variable to track download progress
# download_progress = 0


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global download_progress
#     if request.method == 'POST':
#         # Get the account URL from JSON request
#         account_url = request.json.get('account_url')
#         if account_url:
#             try:
#                 download_progress = 0  # Reset progress
#                 threading.Thread(target=download_tiktok_videos_from_account, args=(
#                     account_url,)).start()  # Start the download in a new thread
#                 return jsonify({"status": "success"}), 200
#             except Exception as e:
#                 return jsonify({"status": "error", "message": str(e)}), 500
#     return render_template('index.html')


# @app.route('/progress_status')
# def progress_status():
#     return jsonify({"progress": download_progress})


# def download_tiktok_videos_from_account(account_url):
#     global download_progress
#     ydl_opts = {
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
#         'format': 'best',
#         'extract_flat': True,  # Only extract URLs, don't download directly
#     }

#     downloaded_count = 0
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             account_info = ydl.extract_info(account_url, download=False)
#             # Total number of videos
#             total_videos = len(account_info.get('entries', []))
#             for i, entry in enumerate(account_info.get('entries', [])):
#                 video_url = entry.get('url')
#                 if video_url:
#                     if download_tiktok_video(video_url):
#                         downloaded_count += 1
#                         # Update progress
#                         download_progress = int(((i + 1) / total_videos) * 100)
#     except Exception as e:
#         print(f"Error downloading videos from account: {str(e)}")
#         download_progress = 100  # Set to 100 to indicate error completion

#     download_progress = 100  # Set progress to 100% when done
#     flash(f'Successfully downloaded {downloaded_count} videos.', 'success')


# def download_tiktok_video(video_url):
#     ydl_opts = {
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
#         'format': 'best',
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#             return True
#     except Exception as e:
#         print(f"Error downloading video: {str(e)}")
#         return False


# # Start the Flask server
# if __name__ == '__main__':
#     app.run(debug=True)


# ?????????? 2nd Version


# from flask import Flask, render_template, request, jsonify, send_file
# import os
# import yt_dlp
# import threading
# import zipfile

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Directory to save downloaded TikTok videos
# DOWNLOAD_FOLDER = 'tiktok_videos'
# if not os.path.exists(DOWNLOAD_FOLDER):
#     os.makedirs(DOWNLOAD_FOLDER)

# # Global variables
# download_progress = 0
# zip_file_path = None  # Path to the ZIP file


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global download_progress
#     global zip_file_path

#     if request.method == 'POST':
#         account_url = request.json.get('account_url')
#         if account_url:
#             try:
#                 download_progress = 0  # Reset progress
#                 zip_file_path = None  # Reset the ZIP file path
#                 threading.Thread(target=download_and_zip_videos,
#                                  args=(account_url,)).start()
#                 return jsonify({"status": "processing"}), 202
#             except Exception as e:
#                 return jsonify({"status": "error", "message": str(e)}), 500
#     return render_template('index.html')


# @app.route('/progress_status')
# def progress_status():
#     return jsonify({"progress": download_progress})


# @app.route('/download_zip')
# def download_zip():
#     global zip_file_path
#     if zip_file_path and os.path.exists(zip_file_path):
#         return send_file(zip_file_path, as_attachment=True)
#     return jsonify({"error": "No file available for download"}), 404


# def download_and_zip_videos(account_url):
#     """Download videos from the given TikTok account URL and create a ZIP file."""
#     global download_progress
#     global zip_file_path

#     ydl_opts = {
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
#         'format': 'best',
#         'extract_flat': True,
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             account_info = ydl.extract_info(account_url, download=False)
#             total_videos = len(account_info.get('entries', []))
#             downloaded_files = []

#             for i, entry in enumerate(account_info.get('entries', [])):
#                 video_url = entry.get('url')
#                 if video_url:
#                     video_path = download_tiktok_video(video_url)
#                     if video_path:
#                         downloaded_files.append(video_path)
#                 download_progress = int(((i + 1) / total_videos) * 100)

#             # Create a ZIP file from all downloaded videos
#             zip_file_path = os.path.join(DOWNLOAD_FOLDER, 'tiktok_videos.zip')
#             with zipfile.ZipFile(zip_file_path, 'w') as zipf:
#                 for file in downloaded_files:
#                     zipf.write(file, os.path.basename(file))
#     except Exception as e:
#         print(f"Error during download or zipping: {e}")
#         download_progress = 100  # Mark as completed even if there was an error

#     download_progress = 100  # Mark as completed


# def download_tiktok_video(video_url):
#     """Download a single TikTok video."""
#     ydl_opts = {
#         'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
#         'format': 'best',
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(video_url)
#             return os.path.join(DOWNLOAD_FOLDER, f"{info['id']}.{info['ext']}")
#     except Exception as e:
#         print(f"Error downloading video: {e}")
#         return None


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
import os
import yt_dlp
import threading
import zipfile
import shutil

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_fallback_key')

DOWNLOAD_FOLDER = 'tiktok_videos'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

download_progress = 0
zip_file_path = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global download_progress
    global zip_file_path

    if request.method == 'POST':
        account_url = request.json.get('account_url')
        if account_url:
            try:
                download_progress = 0
                zip_file_path = None
                threading.Thread(target=download_and_zip_videos,
                                 args=(account_url,)).start()
                return jsonify({"status": "processing"}), 202
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
    return render_template('index.html')


@app.route('/progress_status')
def progress_status():
    """Returns the current download progress."""
    return jsonify({"progress": download_progress})


@app.route('/download_zip')
def download_zip():
    """Serves the ZIP file to the user and deletes the folder after the response is sent."""
    global zip_file_path
    if zip_file_path and os.path.exists(zip_file_path):
        @after_this_request
        def cleanup(response):
            """Delete the DOWNLOAD_FOLDER and all its contents after the ZIP file is sent."""
            try:
                shutil.rmtree(DOWNLOAD_FOLDER)
                print("The DOWNLOAD_FOLDER and all its contents have been deleted.")
            except Exception as e:
                print(f"Error during folder cleanup: {e}")
            return response

        # Serve the ZIP file to the user
        return send_file(zip_file_path, as_attachment=True)

    return jsonify({"error": "No file available for download"}), 404


def download_and_zip_videos(account_url):
    """Download videos from the given TikTok account URL and create a ZIP file."""
    global download_progress
    global zip_file_path

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'format': 'best',
        'extract_flat': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            account_info = ydl.extract_info(account_url, download=False)
            total_videos = len(account_info.get('entries', []))
            downloaded_files = []

            for i, entry in enumerate(account_info.get('entries', [])):
                video_url = entry.get('url')
                if video_url:
                    video_path = download_tiktok_video(video_url)
                    if video_path:
                        downloaded_files.append(video_path)
                download_progress = int(((i + 1) / total_videos) * 100)

            # Create a ZIP file from all downloaded videos
            zip_file_path = os.path.join(DOWNLOAD_FOLDER, 'tiktok_videos.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for file in downloaded_files:
                    zipf.write(file, os.path.basename(file))
    except Exception as e:
        print(f"Error during download or zipping: {e}")
        download_progress = 100

    download_progress = 100


def download_tiktok_video(video_url):
    """Download a single TikTok video."""
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url)
            return os.path.join(DOWNLOAD_FOLDER, f"{info['id']}.{info['ext']}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
