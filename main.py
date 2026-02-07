
from crawler import check_tickets
from notify import send_email_notification

if __name__ == "__main__":
    print("正在檢查票券...")
    tickets = check_tickets()
    # TODO: remove this
    send_email_notification("WBC 2026 台灣賽事釋出票券！", "testing")
    if tickets:
        for ticket in tickets:
            send_email_notification("WBC 2026 台灣賽事釋出票券！", ticket)
    else:
        print("目前沒有台灣賽事的票券。")
        
