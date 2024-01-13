import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
from pathlib import Path

def get_available_resolutions(yt):
    return [stream.resolution for stream in yt.streams.filter(file_extension="mp4")]

def select_output_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_selected = filedialog.askdirectory(title="Select Output Folder")
    return folder_selected

def download_video(url, output_path=".", resolution="highest", audio_only=False, format_type="mp4"):
    try:
        yt = YouTube(url)
        available_resolutions = get_available_resolutions(yt)
        print("Available Resolutions:", available_resolutions)

        if resolution == "highest":
            video_stream = yt.streams.get_highest_resolution()
        elif resolution == "lowest":
            video_stream = yt.streams.get_lowest_resolution()
        else:
            # Check if the selected resolution is available
            if resolution in available_resolutions:
                video_stream = yt.streams.filter(res=resolution).first()
            else:
                print(f"Selected resolution {resolution} not available. Downloading the highest resolution.")
                video_stream = yt.streams.get_highest_resolution()

        if audio_only:
            video_stream = yt.streams.filter(only_audio=True).first()

        output_path = Path(output_path)
        print(f"Downloading: {yt.title}")
        video_stream.download(output_path, filename=f"{yt.title}.{format_type}")

        print("Download complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

def on_download_button_click():
    video_url = url_entry.get()
    output_directory = output_entry.get()
    selected_resolution = resolution_var.get()

    # Pass the selected resolution to the download function
    download_video(video_url, output_path=output_directory, resolution=selected_resolution, audio_only=audio_only_var.get())

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x300")

# Style for themed widgets
style = ttk.Style()
style.theme_use("clam")

# URL Entry
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

# Output Entry
output_label = ttk.Label(root, text="Select Output Folder:")
output_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
output_entry = ttk.Entry(root, width=40)
output_entry.insert(0, select_output_folder())
output_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

# Resolution Options
resolution_label = ttk.Label(root, text="Select Resolution:")
resolution_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p"]
resolution_var = tk.StringVar(root)
resolution_var.set(resolutions[0])
resolution_menu = ttk.Combobox(root, textvariable=resolution_var, values=resolutions, state="readonly")
resolution_menu.grid(row=2, column=1, pady=10, padx=10, sticky="w")

# Audio Only Checkbox
audio_only_var = tk.BooleanVar()
audio_only_check = ttk.Checkbutton(root, text="Audio Only", variable=audio_only_var)
audio_only_check.grid(row=3, column=1, pady=10, padx=10, sticky="w")

# Download Button
download_button = ttk.Button(root, text="Download", command=on_download_button_click)
download_button.grid(row=4, column=1, pady=20, padx=10, sticky="w")

# Run the GUI
root.mainloop()


