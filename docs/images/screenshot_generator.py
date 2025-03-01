import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QListWidget,
    QProgressBar, QFrame
)
from PyQt6.QtGui import QPainter, QColor, QPixmap, QPen, QBrush, QFont
from PyQt6.QtCore import Qt, QSize, QRect

class MockScreenshot(QMainWindow):
    def __init__(self, is_dark=False):
        super().__init__()
        self.is_dark = is_dark
        self.init_ui()
        
    def init_ui(self):
        # 창 설정
        self.setWindowTitle("Sirodrop")
        self.resize(800, 600)
        
        # 색상 설정
        if self.is_dark:
            # 다크 모드
            self.bg_color = "#191919"
            self.text_color = "#f0f0f0"
            self.accent_color = "#7b68ee"
            self.secondary_bg = "#232323"
            self.border_color = "#333333"
        else:
            # 라이트 모드
            self.bg_color = "#ffffff"
            self.text_color = "#333333"
            self.accent_color = "#7b68ee"
            self.secondary_bg = "#f5f5f5"
            self.border_color = "#e5e5e5"
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 헤더 생성
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet(f"background-color: {self.bg_color};")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # 헤더 내용
        title = QLabel("Sirodrop")
        title.setStyleSheet(f"color: {self.accent_color}; font-size: 18px; font-weight: bold;")
        
        version = QLabel("v1.0.0")
        version.setStyleSheet(f"color: {self.text_color}80;")
        
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        header_layout.addWidget(version)
        
        # 탭 위젯 생성
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabBar::tab {{
                background-color: {self.bg_color};
                color: {self.text_color};
                padding: 10px 20px;
                border: none;
            }}
            
            QTabBar::tab:selected {{
                color: {self.accent_color};
                border-bottom: 2px solid {self.accent_color};
            }}
            
            QTabWidget::pane {{
                border: none;
                background-color: {self.bg_color};
            }}
        """)
        
        # 전송 탭 생성
        send_tab = QWidget()
        send_layout = QVBoxLayout(send_tab)
        send_layout.setContentsMargins(20, 20, 20, 20)
        
        # 전송 탭 내용
        send_title = QLabel("전송할 파일")
        send_title.setStyleSheet(f"color: {self.accent_color}; font-size: 16px; font-weight: bold;")
        
        file_input = QLineEdit()
        file_input.setPlaceholderText("파일 경로")
        file_input.setStyleSheet(f"""
            background-color: {self.secondary_bg};
            color: {self.text_color};
            border: 1px solid {self.border_color};
            border-radius: 8px;
            padding: 10px;
        """)
        
        browse_button = QPushButton("찾아보기")
        browse_button.setStyleSheet(f"""
            background-color: {self.accent_color};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
        """)
        
        file_input_layout = QHBoxLayout()
        file_input_layout.addWidget(file_input)
        file_input_layout.addWidget(browse_button)
        
        # 파일 목록
        file_list = QListWidget()
        file_list.setMinimumHeight(150)
        file_list.setStyleSheet(f"""
            background-color: {self.secondary_bg}30;
            color: {self.text_color};
            border: 2px dashed {self.accent_color};
            border-radius: 8px;
            padding: 5px;
        """)
        
        # 전송 버튼
        send_button = QPushButton("전송 시작")
        send_button.setMinimumHeight(50)
        send_button.setStyleSheet(f"""
            background-color: {self.accent_color};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 15px;
            font-weight: bold;
            font-size: 14px;
        """)
        
        # 전송 탭에 위젯 추가
        send_layout.addWidget(send_title)
        send_layout.addSpacing(10)
        send_layout.addLayout(file_input_layout)
        send_layout.addSpacing(10)
        send_layout.addWidget(file_list)
        send_layout.addSpacing(20)
        send_layout.addWidget(send_button)
        send_layout.addStretch(1)
        
        # 탭 추가
        tab_widget.addTab(send_tab, "Send")
        tab_widget.addTab(QWidget(), "Receive")
        tab_widget.addTab(QWidget(), "History")
        tab_widget.addTab(QWidget(), "Settings")
        
        # 상태 바
        status_bar = QWidget()
        status_bar.setFixedHeight(30)
        status_bar.setStyleSheet(f"background-color: {self.bg_color};")
        
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(20, 0, 20, 0)
        
        status_label = QLabel("준비됨")
        status_label.setStyleSheet(f"color: {self.text_color}80;")
        
        status_layout.addWidget(status_label)
        
        # 메인 레이아웃에 추가
        main_layout.addWidget(header)
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(status_bar)
        
        # 전체 스타일 설정
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {self.bg_color};
                color: {self.text_color};
                font-family: Arial, sans-serif;
            }}
        """)
    
    def capture_screenshot(self, save_path):
        """스크린샷 캡처 및 저장"""
        screenshot = QPixmap(self.size())
        self.render(screenshot)
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        screenshot.save(save_path)
        return save_path


if __name__ == "__main__":
    app = QApplication([])
    
    # 현재 디렉토리 확인
    current_dir = Path(__file__).parent.absolute()
    
    # 라이트 모드 스크린샷
    light_app = MockScreenshot(is_dark=False)
    light_path = current_dir / "screenshot_light.png"
    light_app.capture_screenshot(str(light_path))
    
    # 다크 모드 스크린샷
    dark_app = MockScreenshot(is_dark=True)
    dark_path = current_dir / "screenshot_dark.png"
    dark_app.capture_screenshot(str(dark_path))
    
    print(f"스크린샷이 생성되었습니다:\n- {light_path}\n- {dark_path}") 