from flask import Flask, render_template, request, flash, jsonify
import os
import yt_dlp
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Directory to save downloaded TikTok videos
DOWNLOAD_FOLDER = 'tiktok_videos'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Global variable to track download progress
download_progress = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    global download_progress
    if request.method == 'POST':
        # Get the account URL from JSON request
        account_url = request.json.get('account_url')
        if account_url:
            try:
                download_progress = 0  # Reset progress
                threading.Thread(target=download_tiktok_videos_from_account, args=(
                    account_url,)).start()  # Start the download in a new thread
                return jsonify({"status": "success"}), 200
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
    return render_template('index.html')


@app.route('/progress_status')
def progress_status():
    return jsonify({"progress": download_progress})


def download_tiktok_videos_from_account(account_url):
    global download_progress
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'format': 'best',
        'extract_flat': True,  # Only extract URLs, don't download directly
    }

    downloaded_count = 0
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            account_info = ydl.extract_info(account_url, download=False)
            # Total number of videos
            total_videos = len(account_info.get('entries', []))
            for i, entry in enumerate(account_info.get('entries', [])):
                video_url = entry.get('url')
                if video_url:
                    if download_tiktok_video(video_url):
                        downloaded_count += 1
                        # Update progress
                        download_progress = int(((i + 1) / total_videos) * 100)
    except Exception as e:
        print(f"Error downloading videos from account: {str(e)}")
        download_progress = 100  # Set to 100 to indicate error completion

    download_progress = 100  # Set progress to 100% when done
    flash(f'Successfully downloaded {downloaded_count} videos.', 'success')


def download_tiktok_video(video_url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return True
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False


# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
