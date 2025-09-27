from slack_sdk import WebClient
from datetime import datetime


#client = WebClient(token="xoxb-9589898794277-9607064077553-v3qyYofyeh79xKRuKugxDaLr")

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

        # Convert Slack ts to datetime
        dt = datetime.fromtimestamp(float(ts))

        # Look up username
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
    for m in msgs:
        print(f"[{m['datetime']}] {m['user']}: {m['text']}")
