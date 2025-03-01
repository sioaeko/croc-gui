import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QFrame, QComboBox,
    QFormLayout, QSpinBox, QCheckBox, QMessageBox,
    QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QColor, QFont, QPalette

class SettingsWidget(QWidget):
    # Define signals
    theme_changed = pyqtSignal(str)
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.main_window = parent
        self.init_ui()
    
    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(20)
        
        # 스크롤 영역 설정
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(30)
        
        # 헤더 영역
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        title_label = QLabel("설정")
        title_label.setObjectName("sectionTitle")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        
        scroll_layout.addWidget(header_widget)
        
        # 폴더 설정 섹션
        scroll_layout.addWidget(self.create_folder_section())
        
        # 앱 설정 섹션
        scroll_layout.addWidget(self.create_app_section())
        
        # 테마 설정 섹션
        scroll_layout.addWidget(self.create_theme_section())
        
        # 스크롤 영역 설정
        scroll_area.setWidget(scroll_content)
        self.main_layout.addWidget(scroll_area)
        
        # 저장 버튼
        self.save_button = QPushButton("설정 저장")
        self.save_button.setMinimumHeight(50)
        self.save_button.clicked.connect(self.save_settings)
        
        self.main_layout.addWidget(self.save_button)
    
    def create_folder_section(self):
        """폴더 설정 섹션 생성"""
        section = QGroupBox("폴더 설정")
        section.setObjectName("settingsSection")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # 기본 저장 폴더
        dir_container = QWidget()
        dir_layout = QVBoxLayout(dir_container)
        dir_layout.setContentsMargins(0, 0, 0, 0)
        dir_layout.setSpacing(8)
        
        dir_label = QLabel("기본 저장 폴더")
        dir_label.setObjectName("settingLabel")
        
        dir_input_layout = QHBoxLayout()
        dir_input_layout.setContentsMargins(0, 0, 0, 0)
        dir_input_layout.setSpacing(10)
        
        self.default_dir_input = QLineEdit()
        self.default_dir_input.setPlaceholderText("기본 저장 경로를 선택하세요")
        self.default_dir_input.setText(self.config.get_value("default_dir", ""))
        
        browse_button = QPushButton("찾아보기")
        browse_button.clicked.connect(self.browse_default_dir)
        browse_button.setMinimumWidth(100)
        
        dir_input_layout.addWidget(self.default_dir_input, 1)
        dir_input_layout.addWidget(browse_button)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addLayout(dir_input_layout)
        
        # 자동으로 폴더 생성
        auto_create_check = QCheckBox("존재하지 않는 폴더 자동 생성")
        auto_create_check.setChecked(self.config.get_value("auto_create_folder", True))
        self.auto_create_check = auto_create_check
        
        layout.addWidget(dir_container)
        layout.addWidget(auto_create_check)
        
        return section
    
    def create_app_section(self):
        """앱 설정 섹션 생성"""
        section = QGroupBox("앱 설정")
        section.setObjectName("settingsSection")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # Croc 경로 설정
        croc_container = QWidget()
        croc_layout = QVBoxLayout(croc_container)
        croc_layout.setContentsMargins(0, 0, 0, 0)
        croc_layout.setSpacing(8)
        
        croc_label = QLabel("Croc 실행 파일 경로")
        croc_label.setObjectName("settingLabel")
        
        croc_input_layout = QHBoxLayout()
        croc_input_layout.setContentsMargins(0, 0, 0, 0)
        croc_input_layout.setSpacing(10)
        
        self.croc_path_input = QLineEdit()
        self.croc_path_input.setPlaceholderText("Croc 실행 파일 경로 (비워두면 기본 PATH 사용)")
        self.croc_path_input.setText(self.config.get_value("croc_path", ""))
        
        browse_button = QPushButton("찾아보기")
        browse_button.clicked.connect(self.browse_croc_path)
        browse_button.setMinimumWidth(100)
        
        croc_input_layout.addWidget(self.croc_path_input, 1)
        croc_input_layout.addWidget(browse_button)
        
        croc_layout.addWidget(croc_label)
        croc_layout.addLayout(croc_input_layout)
        
        # 시작 시 자동 연결
        auto_connect_check = QCheckBox("시작 시 자동으로 연결")
        auto_connect_check.setChecked(self.config.get_value("auto_connect", True))
        self.auto_connect_check = auto_connect_check
        
        # 상세 로그 활성화
        verbose_log_check = QCheckBox("상세 로그 활성화")
        verbose_log_check.setChecked(self.config.get_value("verbose_log", False))
        self.verbose_log_check = verbose_log_check
        
        layout.addWidget(croc_container)
        layout.addWidget(auto_connect_check)
        layout.addWidget(verbose_log_check)
        
        return section
    
    def create_theme_section(self):
        """테마 설정 섹션 생성"""
        section = QGroupBox("테마 설정")
        section.setObjectName("settingsSection")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # 테마 선택
        theme_container = QWidget()
        theme_layout = QVBoxLayout(theme_container)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(8)
        
        theme_label = QLabel("테마 선택")
        theme_label.setObjectName("settingLabel")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("라이트 모드", "light")
        self.theme_combo.addItem("다크 모드", "dark")
        
        # 현재 선택된 테마 설정
        current_theme = self.config.get_value("theme", "light")
        index = 0 if current_theme == "light" else 1
        self.theme_combo.setCurrentIndex(index)
        
        # 테마 변경 시 미리보기
        self.theme_combo.currentIndexChanged.connect(self.preview_theme)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        
        layout.addWidget(theme_container)
        
        return section
    
    def browse_default_dir(self):
        """기본 저장 폴더 선택"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "기본 저장 폴더 선택", 
            self.default_dir_input.text() or str(Path.home())
        )
        
        if dir_path:
            self.default_dir_input.setText(dir_path)
    
    def browse_croc_path(self):
        """Croc 실행 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Croc 실행 파일 선택", 
            "/usr/local/bin" if os.name == 'posix' else "C:\\",
            "실행 파일 (*)" if os.name == 'nt' else "All Files (*)"
        )
        
        if file_path:
            self.croc_path_input.setText(file_path)
    
    def preview_theme(self, index):
        """테마 미리보기"""
        theme = self.theme_combo.itemData(index)
        self.theme_changed.emit(theme)
    
    def save_settings(self):
        """설정 저장"""
        # 폴더 설정
        self.config.set_value("default_dir", self.default_dir_input.text())
        self.config.set_value("auto_create_folder", self.auto_create_check.isChecked())
        
        # 앱 설정
        self.config.set_value("croc_path", self.croc_path_input.text())
        self.config.set_value("auto_connect", self.auto_connect_check.isChecked())
        self.config.set_value("verbose_log", self.verbose_log_check.isChecked())
        
        # 테마 설정
        theme = self.theme_combo.itemData(self.theme_combo.currentIndex())
        self.config.set_value("theme", theme)
        
        # 설정 저장
        self.config.save()
        
        # 알림 표시
        QMessageBox.information(self, "설정 저장", "설정이 성공적으로 저장되었습니다.")
        
        # 테마 변경 신호 발생
        self.theme_changed.emit(theme) 