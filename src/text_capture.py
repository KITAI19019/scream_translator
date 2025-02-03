import keyboard
import pyperclip
import pytesseract
from PIL import ImageGrab, Image
import numpy as np
from typing import Callable
import time

class TextCapture:
    def __init__(self, callback: Callable[[str], None]):
        """
        初始化文本捕获类
        :param callback: 捕获到文本后的回调函数
        """
        self.callback = callback
        self.last_clipboard_content = ''
        self.is_monitoring = False

    def start_capture(self):
        """启动文本捕获"""
        self.is_monitoring = True
        # 设置快捷键监听
        keyboard.add_hotkey('ctrl+shift+s', self._capture_screen)
        # 启动剪贴板监控
        self._monitor_clipboard()

    def stop_capture(self):
        """停止文本捕获"""
        self.is_monitoring = False
        keyboard.remove_hotkey('ctrl+shift+s')

    def _capture_screen(self):
        """屏幕文字识别"""
        try:
            # 捕获屏幕截图
            screenshot = ImageGrab.grab()
            # 转换为numpy数组进行处理
            img_np = np.array(screenshot)
            # 使用tesseract进行OCR识别
            text = pytesseract.image_to_string(img_np, lang='chi_sim+eng')
            if text.strip():
                self.callback(text.strip())
        except Exception as e:
            print(f"截图识别错误: {str(e)}")

    def _monitor_clipboard(self):
        """监控剪贴板"""
        while self.is_monitoring:
            try:
                current_content = pyperclip.paste()
                if current_content != self.last_clipboard_content:
                    self.last_clipboard_content = current_content
                    if current_content.strip():
                        self.callback(current_content.strip())
            except Exception as e:
                print(f"剪贴板监控错误: {str(e)}")
            time.sleep(0.5)  # 降低CPU使用率

def example_callback(text: str):
    """示例回调函数"""
    print(f"捕获到文本: {text}")

if __name__ == "__main__":
    # 使用示例
    capture = TextCapture(example_callback)
    capture.start_capture()
    print("文本捕获已启动...")
    print("按Ctrl+Shift+S进行屏幕文字识别")
    print("复制文本会自动捕获")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        capture.stop_capture()
        print("文本捕获已停止")