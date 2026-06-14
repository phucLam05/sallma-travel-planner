import logging

def get_logger(name: str):
    """
    Tạo logger để ghi log hệ thống ra terminal (INFO, DEBUG).
    Giúp theo dõi luồng chạy của các Agent và sự thay đổi của State.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # Định dạng log: Thời gian - Tên Logger - Mức độ - Nội dung thông báo
        formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        
        # In ra terminal (stdout)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    return logger
