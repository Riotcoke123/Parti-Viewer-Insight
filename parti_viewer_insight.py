import requests
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import urllib.request
import io

user_ids = ["465731", "348242"]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def get_livestream_info(user_id):
    url = f"https://api-backend.parti.com/parti_v2/profile/get_livestream_channel_info/{user_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[{user_id}] Error fetching livestream data: {e}")
        return None

def analyze_viewer_data(data):
    channel_info = data.get("channel_info", {})
    stream_info = channel_info.get("stream", {})
    channel_details = channel_info.get("channel", {})

    user_id = channel_details.get("user_id", "Unknown")
    total_viewers = stream_info.get("viewer_count", 0)

    real_viewers_8 = total_viewers / 9 if total_viewers else 0
    fake_viewers_8 = total_viewers - real_viewers_8

    real_viewers_12 = total_viewers / 13 if total_viewers else 0
    fake_viewers_12 = total_viewers - real_viewers_12

    return {
        "id": user_id,
        "total_viewer_count": total_viewers,
        "8:1_ratio": {
            "real_viewer_count": int(real_viewers_8),
            "bot_viewer_count": int(fake_viewers_8),
        },
        "12:1_ratio": {
            "real_viewer_count": int(real_viewers_12),
            "bot_viewer_count": int(fake_viewers_12),
        },
    }

def fetch_profile(user_id):
    url = f"https://api-backend.parti.com/parti_v2/profile/user_profile/{user_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[{user_id}] Error fetching profile data: {e}")
        return {}

def fetch_data_for_user(user_id):
    profile = fetch_profile(user_id) or {}
    livestream = get_livestream_info(user_id) or {}
    analysis = analyze_viewer_data(livestream)
    
    return {
        "user_id": user_id,
        "avatar_link": profile.get("avatar_link"),
        "social_username": profile.get("social_username"),
        "viewer_analysis": analysis,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def fetch_all_streamers(user_ids):
    results = []
    with ThreadPoolExecutor(max_workers=min(10, len(user_ids))) as executor:
        future_to_user = {executor.submit(fetch_data_for_user, uid): uid for uid in user_ids}
        for future in as_completed(future_to_user):
            uid = future_to_user[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print(f"[{uid}] Exception: {exc}")
    return results

def display_viewer_stats(container, analysis, viewer_img, bot_img):
    total = analysis.get("total_viewer_count", 0)

    r8 = analysis["8:1_ratio"]
    real_8, bots_8 = r8["real_viewer_count"], r8["bot_viewer_count"]
    ratio_percent_8 = int((bots_8 / total) * 100) if total else 0
    status_text_8 = "⚠️ Looks Botted" if ratio_percent_8 > 80 else "✅ Clean"
    status_color_8 = "red" if ratio_percent_8 > 80 else "green"

    r12 = analysis["12:1_ratio"]
    real_12, bots_12 = r12["real_viewer_count"], r12["bot_viewer_count"]
    ratio_percent_12 = int((bots_12 / total) * 100) if total else 0
    status_text_12 = "⚠️ Looks Botted" if ratio_percent_12 > 80 else "✅ Clean"
    status_color_12 = "red" if ratio_percent_12 > 80 else "green"

    center = tk.Frame(container)
    center.pack(anchor="center")

    total_frame = tk.Frame(center)
    total_frame.pack()
    tk.Label(total_frame, image=viewer_img).pack(side="left")
    tk.Label(total_frame, text=f"{total}", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    tk.Label(center, text="8:1 Ratio", font=("Arial", 10, "bold")).pack(pady=(5,0))
    real_frame = tk.Frame(center)
    real_frame.pack()
    tk.Label(real_frame, image=viewer_img).pack(side="left")
    tk.Label(real_frame, text=f"{real_8} Real Viewers").pack(side="left", padx=5)

    bot_frame = tk.Frame(center)
    bot_frame.pack()
    tk.Label(bot_frame, image=bot_img).pack(side="left")
    tk.Label(bot_frame, text=f"{bots_8} Fake Viewers").pack(side="left", padx=5)

    tk.Label(center, text=f"Status: {status_text_8}", fg=status_color_8, font=("Arial", 10, "bold")).pack(pady=(0, 5))

    tk.Label(center, text="12:1 Ratio", font=("Arial", 10, "bold")).pack(pady=(10,0))
    real_frame = tk.Frame(center)
    real_frame.pack()
    tk.Label(real_frame, image=viewer_img).pack(side="left")
    tk.Label(real_frame, text=f"{real_12} Real Viewers").pack(side="left", padx=5)

    bot_frame = tk.Frame(center)
    bot_frame.pack()
    tk.Label(bot_frame, image=bot_img).pack(side="left")
    tk.Label(bot_frame, text=f"{bots_12} Fake Viewers").pack(side="left", padx=5)

    tk.Label(center, text=f"Status: {status_text_12}", fg=status_color_12, font=("Arial", 10, "bold")).pack(pady=(0, 5))

def run_fetch():
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Fetching data...\n")

    def task():
        combined_data = fetch_all_streamers(user_ids)

        for widget in profile_frame.winfo_children():
            widget.destroy()

        for item in combined_data:
            container = tk.Frame(profile_frame, bd=2, relief="groove", padx=5, pady=5)
            container.pack(side="left", padx=5, pady=10)

            username = item.get("social_username", "Unknown")
            avatar_url = item.get("avatar_link")

            try:
                if avatar_url:
                    with urllib.request.urlopen(avatar_url) as u:
                        raw_data = u.read()
                    im = Image.open(io.BytesIO(raw_data)).resize((60, 60))
                    photo = ImageTk.PhotoImage(im)
                    img_label = tk.Label(container, image=photo)
                    img_label.image = photo
                    img_label.pack()
            except Exception as e:
                print(f"Image error for {username}: {e}")

            tk.Label(container, text=f"Username: {username}", font=("Arial", 12, "bold")).pack()
            display_viewer_stats(container, item["viewer_analysis"], viewer_icon, bot_icon)

        output_box.insert(tk.END, "Done.\n")

    threading.Thread(target=task).start()
    root.after(60000, run_fetch)

# GUI setup
root = tk.Tk()
root.title("Parti Stream Viewer Checker")
root.geometry("800x650")  # Increased window height

# Load icons
def load_image(url, size):
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    im = Image.open(io.BytesIO(raw_data)).resize(size)
    return ImageTk.PhotoImage(im)

top_banner = load_image("https://i.ibb.co/xKW6fznS/1.jpg", (175, 200))
viewer_icon = load_image("https://i.ibb.co/5hzdhk3G/icons8-viewer-50.png", (25, 25))
bot_icon = load_image("https://i.ibb.co/KpYp89wR/icons8-bot-100.png", (25, 25))

tk.Label(root, image=top_banner).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

start_button = tk.Button(frame, text="Fetch Stream Data", command=run_fetch, font=("Arial", 12))
start_button.pack()

# Scrollable profile display
canvas = tk.Canvas(root, height=400)  # Increased canvas height by 100
scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scroll_x.set)

scroll_x.pack(fill="x", side="bottom")
canvas.pack(fill="both", expand=True)

profile_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=profile_frame, anchor="nw")

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

profile_frame.bind("<Configure>", update_scrollregion)

output_box = scrolledtext.ScrolledText(root, width=80, height=6)
output_box.pack()

root.mainloop()
