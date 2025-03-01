import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QProgressBar, QFrame,
    QMessageBox, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QColor

class ReceiveWidget(QWidget):
    # Define signals
    receive_requested = pyqtSignal(str, object)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.animations = {}  # 애니메이션 객체 저장
        self.init_ui()
        self.update_theme(self.config.get_value("theme", "light"))
    
    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 스크롤 영역 생성
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 스크롤 영역에 들어갈 위젯 생성
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(15, 15, 15, 15)
        scroll_layout.setSpacing(20)
        
        # 스크롤 영역 설정
        scroll_area.setWidget(scroll_content)
        self.main_layout.addWidget(scroll_area)
        
        # 원래 main_layout을 scroll_layout으로 변경
        self.main_layout = scroll_layout
        
        # Create sections
        self.create_code_section()
        self.create_save_section()
        self.create_progress_section()
        
        # Add stretch to push all elements to the top
        self.main_layout.addStretch(1)
    
    def create_code_section(self):
        # 제목 레이아웃
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # 제목
        title_label = QLabel("코드 구문 입력")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # 코드 입력 필드 레이아웃
        code_input_layout = QHBoxLayout()
        code_input_layout.setContentsMargins(0, 10, 0, 0)
        code_input_layout.setSpacing(8)
        
        # 코드 입력 필드
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("발신자가 제공한 코드 구문을 입력하세요")
        
        # 수신 버튼
        self.receive_button = QPushButton("수신 시작")
        self.receive_button.setMinimumWidth(120)
        self.receive_button.clicked.connect(self.receive_files)
        
        code_input_layout.addWidget(self.code_input, 1)
        code_input_layout.addWidget(self.receive_button)
        
        # 전체 레이아웃
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        section_layout.addWidget(title_container)
        section_layout.addLayout(code_input_layout)
        
        self.main_layout.addLayout(section_layout)
        
        # 섹션 구분선
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: transparent;")
        
        self.main_layout.addWidget(divider)
    
    def create_save_section(self):
        # 제목 레이아웃
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # 제목
        title_label = QLabel("저장 위치")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # 저장 경로 레이아웃
        save_path_layout = QHBoxLayout()
        save_path_layout.setContentsMargins(0, 10, 0, 0)
        save_path_layout.setSpacing(8)
        
        # 경로 입력 필드
        self.save_path_input = QLineEdit()
        self.save_path_input.setPlaceholderText("저장 경로 선택 (기본 위치: 다운로드 폴더)")
        
        # 찾아보기 버튼
        browse_button = QPushButton("찾아보기")
        browse_button.setMinimumWidth(100)
        browse_button.clicked.connect(self.browse_save_location)
        
        save_path_layout.addWidget(self.save_path_input, 1)
        save_path_layout.addWidget(browse_button)
        
        # 전체 레이아웃
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        section_layout.addWidget(title_container)
        section_layout.addLayout(save_path_layout)
        
        self.main_layout.addLayout(section_layout)
        
        # 섹션 구분선
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: transparent;")
        
        self.main_layout.addWidget(divider)
    
    def create_progress_section(self):
        # 제목 레이아웃
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # 제목
        title_label = QLabel("수신 상태")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # 진행 상태 레이아웃
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 10, 0, 0)
        progress_layout.setSpacing(10)
        
        # 파일 정보
        self.file_info_label = QLabel("파일 정보가 여기에 표시됩니다")
        self.file_info_label.setStyleSheet("color: #666666;")
        
        # 진행 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumHeight(20)
        
        # 상태 메시지
        self.status_label = QLabel("준비됨")
        self.status_label.setStyleSheet("color: #666666;")
        
        progress_layout.addWidget(self.file_info_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        # 전체 레이아웃
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        section_layout.addWidget(title_container)
        section_layout.addLayout(progress_layout)
        
        self.main_layout.addLayout(section_layout)
    
    def update_theme(self, theme):
        """테마에 따라 위젯 스타일 업데이트"""
        is_dark = theme == "dark"
        
        # 테마 색상 정의
        if is_dark:
            # 다크 테마
            primary_color = "#7b68ee"
            text_color = "#f0f0f0"
            secondary_text = "#a0a0a0"
        else:
            # 라이트 테마
            primary_color = "#7b68ee"
            text_color = "#333333"
            secondary_text = "#666666"
        
        # 섹션 제목 스타일
        for widget in self.findChildren(QLabel):
            if widget.objectName() == "sectionTitle":
                widget.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {primary_color};")
    
    def browse_save_location(self):
        """저장 경로 선택"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "저장 위치 선택", 
            self.config.get_value("default_dir", str(Path.home()))
        )
        
        if dir_path:
            self.save_path_input.setText(dir_path)
    
    def receive_files(self):
        """파일 수신 시작"""
        code = self.code_input.text().strip()
        if not code:
            QMessageBox.warning(self, "경고", "코드 구문을 입력해주세요.")
            return
        
        # 저장 경로 확인
        save_path = self.save_path_input.text().strip()
        if not save_path:
            # 기본 경로 설정
            save_path = self.config.get_value(
                "default_dir", 
                str(Path.home() / "Downloads")
            )
            self.save_path_input.setText(save_path)
        
        # 경로 존재 확인
        if not os.path.isdir(save_path):
            try:
                os.makedirs(save_path, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "경로 오류", f"저장 경로를 생성할 수 없습니다: {str(e)}")
                return
        
        # 옵션 설정
        options = {
            'save_path': save_path
        }
        
        # 수신 요청 신호 발생
        self.receive_requested.emit(code, options)
        
        # UI 업데이트
        self.file_info_label.setText("연결 중...")
        self.status_label.setText("발신자를 찾는 중...")
        
        # 실제 구현에서는 백그라운드 작업으로 처리하고 진행 상황을 업데이트함
        # 여기서는 데모용으로 타이머 사용
        QTimer.singleShot(1500, self.simulate_connection)
    
    def simulate_connection(self):
        """연결 시뮬레이션 (데모용)"""
        self.file_info_label.setText("파일: example_document.pdf (2.5 MB)")
        self.status_label.setText("연결됨, 수신 시작 중...")
        QTimer.singleShot(1000, self.simulate_progress)
    
    def simulate_progress(self):
        """진행 상태 시뮬레이션 (데모용)"""
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
            self.status_label.setText(f"파일 수신 중... {current + 10}%")
            QTimer.singleShot(500, self.simulate_progress)
        else:
            self.status_label.setText("수신 완료!")
            self.file_info_label.setText("파일이 성공적으로 저장되었습니다")
            QTimer.singleShot(2000, self.reset_progress)
    
    def reset_progress(self):
        """진행 상태 초기화"""
        self.progress_bar.setValue(0)
        self.status_label.setText("준비됨")
        self.file_info_label.setText("파일 정보가 여기에 표시됩니다") 