from slack_sdk import WebClient
from datetime import datetime
#from dense_embeddings import slack_pipeline
import os, json


STATE_FILE = "slack_state.json"


def load_last_ts(channel_id: str):
    """Load last seen timestamp for a channel from state file."""
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
    return state.get(channel_id)




def save_last_ts(channel_id: str, ts: str):
    """Save last seen timestamp for a channel to state file."""
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    state[channel_id] = ts
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_username(msg):
    """Extract username or bot name from a Slack message dict."""
    user_id = msg.get("user")
    bot_id = msg.get("bot_id")
    username = msg.get("username")


    # Case 1: Human user
    if user_id:
        try:
            user_info = client.users_info(user=user_id)
            return user_info["user"].get("real_name") or user_info["user"].get("name")
        except Exception:
            return f"Unknown User ({user_id})"


    # Case 2: Bot message with a bot_id
    if bot_id:
        return f"Bot ({bot_id})"


    # Case 3: Message with 'username' field (custom integration)
    if username:
        return username


    # Fallback
    return "System"




def fetch_slack_messages(channel_id, limit=10):
    result = client.conversations_history(channel=channel_id, limit=limit)
    messages = []
    for msg in result["messages"]:
        text = msg.get("text", "")
        ts = msg.get("ts")
        user_id = msg.get("user")


        dt = datetime.fromtimestamp(float(ts))


        username = get_username(msg)


        messages.append({
            "user": username,
            "text": text,
            "timestamp": ts,
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S")
        })
    return messages


if __name__ == "__main__":
    channel_id = "C09HBSF54H3"  # replace with your channel id
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
        print(f"[{m['datetime']}] {m['user']}: {m['text']}")
    for m in msgs:
        print(f"[{m['datetime']}] {m['user']}: {m['text']}")
    #slack_pipeline(new_msgs)