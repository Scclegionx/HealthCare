from model import HealthcareChatbot

def main():
    print("Bắt đầu huấn luyện mô hình...")
    chatbot = HealthcareChatbot()
    chatbot.train()
    print("Huấn luyện hoàn tất! Mô hình đã được lưu trong thư mục 'models'")

if __name__ == "__main__":
    main() 