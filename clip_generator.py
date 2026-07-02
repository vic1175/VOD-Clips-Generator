import csv
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta
import os

def browse_csv():
    file_path = filedialog.askopenfilename(
        title="Select OBS Timestamps CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, file_path)

def parse_timestamp(time_str):
    """Parses timestamps like 0:16:00 or 00:16:00 into a timedelta object"""
    parts = time_str.split(':')
    if len(parts) != 3:
        raise ValueError("Invalid format")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def format_timedelta(td):
    """Formats a timedelta object into HH:MM:SS string"""
    total_seconds = int(td.total_seconds())
    if total_seconds < 0:
        total_seconds = 0
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def start_download():
    url = url_entry.get().strip()
    csv_path = csv_entry.get().strip()
    duration_str = duration_entry.get().strip()
    
    if not url or not csv_path or not duration_str:
        messagebox.showerror("Error", "Please fill out all fields.")
        return
        
    try:
        clip_duration = int(duration_str)
    except ValueError:
        messagebox.showerror("Error", "Clip length must be a number (seconds).")
        return

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            status_label.config(text="Processing clips... please wait.")
            root.update()
            
            clips_found = False
            for index, row in enumerate(reader):
                if not row or not row[0].strip():
                    continue
                    
                button_press_str = row[0].strip()
                
                # Dynamic name mapping from Column B
                clip_name = f"clip_{index + 1}"
                if len(row) > 1 and row[1].strip():
                    clean_name = "".join(c for c in row[1].strip() if c.isalnum() or c in (' ', '_', '-')).rstrip()
                    if clean_name:
                        clip_name = clean_name
                
                try:
                    # Parse time safely without strict zero-padding rules
                    press_time_td = parse_timestamp(button_press_str)
                    start_time_td = press_time_td - timedelta(seconds=clip_duration)
                    
                    start_time = format_timedelta(start_time_td)
                    end_time = format_timedelta(press_time_td)
                    
                    output_template = f"{clip_name}.%(ext)s"
                    time_range = f"*{start_time}-{end_time}"
                    
                    cmd = [
                        "yt-dlp",
                        "--ffmpeg-location", "C:\\ffmpeg\\bin",  # Forces yt-dlp to find it here directly
                        "--download-sections", time_range,
                        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
                        "-o", output_template,
                        url
                    ]
                    
                    subprocess.run(cmd)
                    clips_found = True
                    
                except ValueError:
                    continue
            
            if clips_found:
                status_label.config(text="Finished downloading clips!")
                messagebox.showinfo("Success", "All valid clips have been downloaded successfully!")
            else:
                status_label.config(text="No valid timestamps found.")
                messagebox.showwarning("Warning", "No clips downloaded. Check your CSV time formatting.")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        status_label.config(text="Error occurred.")

# --- GUI Setup ---
root = tk.Tk()
root.title("OBS Studio VOD Clip Extractor")
root.geometry("550x280")
root.resizable(False, False)

tk.Label(root, text="YouTube VOD URL:").pack(anchor="w", padx=20, pady=(15, 2))
url_entry = tk.Entry(root, width=75)
url_entry.pack(padx=20, pady=2)

tk.Label(root, text="OBS Marker CSV Location:").pack(anchor="w", padx=20, pady=(10, 2))
csv_frame = tk.Frame(root)
csv_frame.pack(fill="x", padx=20, pady=2)
csv_entry = tk.Entry(csv_frame, width=58)
csv_entry.pack(side="left")
browse_btn = tk.Button(csv_frame, text="Browse...", command=browse_csv)
browse_btn.pack(side="right", padx=(5, 0))

tk.Label(root, text="Clip Length / Timeframe (Seconds before hotkey press):").pack(anchor="w", padx=20, pady=(10, 2))
duration_entry = tk.Entry(root, width=15)
duration_entry.pack(anchor="w", padx=20, pady=2)
duration_entry.insert(0, "60") 

status_label = tk.Label(root, text="Ready", fg="blue")
status_label.pack(pady=(10, 0))

download_btn = tk.Button(root, text="Extract & Download Clips", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=start_download)
download_btn.pack(pady=(10, 15))

root.mainloop()