from slack_sdk import WebClient
from datetime import datetime
#from dense_embeddings import slack_pipeline
from dotenv import load_dotenv
import os, json, time

load_dotenv()
slack_key = os.getenv("SLACK_KEY")
client = WebClient(token=slack_key)

STATE_FILE = "slack_state.json"

def load_last_ts(channel_id: str):
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except (json.JSONDecodeError, ValueError):
        state = {}
    return state.get(channel_id)

def save_last_ts(channel_id: str, ts: str):
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
        except (json.JSONDecodeError, ValueError):
            state = {}
    state[channel_id] = ts
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_username(msg):
    user_id = msg.get("user")
    bot_id = msg.get("bot_id")
    username = msg.get("username")

    if user_id:
        try:
            user_info = client.users_info(user=user_id)
            return user_info["user"].get("real_name") or user_info["user"].get("name")
        except Exception:
            return f"Unknown User ({user_id})"


    if bot_id:
        return f"Bot ({bot_id})"


    if username:
        return username


    return "System"

def normalize_message(msg, channel_name, is_thread=False):
    text = msg.get("text", "")
    ts = msg.get("ts")
    dt = datetime.fromtimestamp(float(ts))
    username = get_username(msg)

    return {
        "user": username,
        "text": text,
        "timestamp": ts,
        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "thread": is_thread,
        "channel": channel_name
    }

def fetch_slack_messages(channel_id, limit=10):
    channel_info = client.conversations_info(channel=channel_id)
    channel_name = channel_info["channel"]["name"]

    result = client.conversations_history(channel=channel_id, limit=limit)
    messages = []

    for msg in result["messages"]:
        # Add top-level message
        messages.append(normalize_message(msg, channel_name, is_thread=False))

        # If the message has a thread, fetch replies
        if "thread_ts" in msg and msg["thread_ts"] == msg["ts"]:
            replies = client.conversations_replies(channel=channel_id, ts=msg["ts"])
            for reply in replies["messages"][1:]:  # skip parent
                messages.append(normalize_message(reply, channel_name, is_thread=True))

    return messages

if __name__ == "__main__":
    # 🔹 Replace with the list of channel IDs you want to track
    channel_ids = ["C09HBSF54H3", "C09HA76R50B"]

    while True:
        for channel_id in channel_ids:
            msgs = fetch_slack_messages(channel_id)

            last_ts = load_last_ts(channel_id)
            if msgs:
                latest_ts = msgs[0]["timestamp"]
            else:
                latest_ts = last_ts

            if last_ts:
                new_msgs = [m for m in msgs if float(m["timestamp"]) > float(last_ts)]
            else:
                new_msgs = msgs

            if latest_ts:
                save_last_ts(channel_id, latest_ts)

            for m in new_msgs:
                print(f"[{m['datetime']}] (#{m['channel']}) {m['user']}: {m['text']}")

        time.sleep(60)