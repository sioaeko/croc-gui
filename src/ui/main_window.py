import os
import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QProgressBar, QFileDialog,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFrame, QApplication, QMenu, QStatusBar,
    QSystemTrayIcon, QSplitter, QTextEdit, QToolButton,
    QGraphicsDropShadowEffect, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRectF
from PyQt6.QtGui import QIcon, QAction, QPixmap, QColor, QPalette, QFont, QPainter, QPainterPath

import qdarktheme

from src.utils.croc_utils import CrocUtils
from src.ui.send_widget import SendWidget
from src.ui.receive_widget import ReceiveWidget
from src.ui.history_widget import HistoryWidget
from src.ui.settings_widget import SettingsWidget


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.croc_utils = None
        self.animations = {}
        
        # UI 초기화
        self.init_ui()
        
        # Croc 초기화
        try:
            self.croc_utils = CrocUtils(self.config)
            self.statusBar().showMessage(f"Croc version: {self.croc_utils.get_version()}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.statusBar().showMessage("Croc not found or error initializing")
    
    def init_ui(self):
        # 창 속성 설정
        self.setWindowTitle("Sirodrop")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon(self.create_app_icon()))
        
        # 창 위치 및 크기 설정
        geometry = self.config.get_value("window_geometry")
        if geometry:
            self.setGeometry(*geometry)
        else:
            self.resize(950, 650)
            self.center_window()
        
        # 중앙 위젯 및 메인 레이아웃 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 통합 UI 구성
        self.create_header()
        self.create_tabs()
        
        # 통합 스타일 적용
        self.apply_global_style(is_dark=self.config.get_value("theme", "light") == "dark")
        
        # 서비스 초기화
        self.init_services()
    
    def create_header(self):
        """헤더 영역 생성"""
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_widget.setFixedHeight(50)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # 앱 로고
        app_logo = QLabel()
        logo_pixmap = QPixmap(self.create_app_icon())
        app_logo.setPixmap(logo_pixmap.scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        # 앱 제목
        app_title = QLabel("Sirodrop")
        app_title.setObjectName("appTitle")
        
        # 버전 정보
        self.version_label = QLabel("v1.0.0")
        self.version_label.setObjectName("versionLabel")
        
        # 헤더에 위젯 추가
        header_layout.addWidget(app_logo)
        header_layout.addWidget(app_title)
        header_layout.addStretch(1)
        header_layout.addWidget(self.version_label)
        
        # 메인 레이아웃에 헤더 추가
        self.main_layout.addWidget(header_widget)
    
    def create_tabs(self):
        """탭 영역 생성"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setObjectName("mainTabs")
        
        # 탭 생성
        self.send_widget = SendWidget(self.config)
        self.receive_widget = ReceiveWidget(self.config)
        self.history_widget = HistoryWidget(self.config)
        self.settings_widget = SettingsWidget(self.config, self)
        
        # 탭 추가
        self.tab_widget.addTab(self.send_widget, "Send")
        self.tab_widget.addTab(self.receive_widget, "Receive")
        self.tab_widget.addTab(self.history_widget, "History")
        self.tab_widget.addTab(self.settings_widget, "Settings")
        
        # 탭 변경 시그널 연결
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # 메인 레이아웃에 탭 위젯 추가
        self.main_layout.addWidget(self.tab_widget, 1)
    
    def apply_global_style(self, is_dark=False):
        """통합 스타일 적용"""
        # 테마 색상 정의
        if is_dark:
            # 다크 테마
            primary_color = "#7b68ee"
            primary_light = "#9281f0"  # 그라데이션용 라이트 컬러
            primary_dark = "#6550e1"   # 그라데이션용 다크 컬러
            bg_color = "#191919"
            bg_color_light = "#232323"  # 라이트 배경
            text_color = "#f0f0f0"
            secondary_text = "#a0a0a0"
            border_color = "#333333"
        else:
            # 라이트 테마
            primary_color = "#7b68ee"
            primary_light = "#9281f0"  # 그라데이션용 라이트 컬러
            primary_dark = "#6550e1"   # 그라데이션용 다크 컬러
            bg_color = "#ffffff"
            bg_color_light = "#f5f5f5"  # 라이트 배경
            text_color = "#333333"
            secondary_text = "#666666"
            border_color = "#e5e5e5"
        
        # 통합 스타일시트
        self.setStyleSheet(f"""
            /* 전체 앱 기본 스타일 */
            QMainWindow, QWidget, QTabWidget, QFrame, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QProgressBar, QTableWidget {{
                background-color: {bg_color};
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro', 'Helvetica Neue', Arial, sans-serif;
                font-size: 13px;
                color: {text_color};
                border: none;
            }}
            
            /* 헤더 */
            #headerWidget {{
                background-color: {bg_color};
            }}
            
            #appTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {primary_color};
            }}
            
            #versionLabel {{
                color: {secondary_text};
                font-size: 12px;
            }}
            
            /* 탭 위젯 */
            #mainTabs {{
                background-color: {bg_color};
            }}
            
            /* 탭 바 */
            QTabBar::tab {{
                background-color: {bg_color};
                color: {text_color};
                padding: 10px 20px;
                border: none;
                min-width: 80px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            
            QTabBar::tab:selected {{
                color: {primary_color};
                border-bottom: 2px solid {primary_color};
                font-weight: bold;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color_light}, stop:1 {bg_color});
            }}
            
            QTabBar::tab:hover:!selected {{
                color: {primary_color};
                background-color: {bg_color_light}50;
            }}
            
            /* 탭 콘텐츠 영역 */
            QTabWidget::pane {{
                border: none;
                background-color: {bg_color};
            }}
            
            /* 입력 필드 */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                padding: 10px;
                background-color: {bg_color_light};
                color: {text_color};
                selection-background-color: {primary_color};
                selection-color: white;
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 1px solid {primary_color};
                background-color: {bg_color};
            }}
            
            /* 버튼 */
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary_light}, stop:1 {primary_dark});
                color: white;
                padding: 10px 18px;
                border-radius: 10px;
                font-weight: bold;
                border: none;
                min-height: 20px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary_light}, stop:0.4 {primary_color}, stop:1 {primary_dark});
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                    stop:0 {primary_light}, stop:0.6 {primary_color}, stop:1 {primary_dark});
                padding-top: 12px;
                padding-bottom: 8px;
            }}
            
            QPushButton:disabled {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {secondary_text}, stop:1 {secondary_text}80);
                color: {bg_color};
            }}
            
            /* 프로그레스바 */
            QProgressBar {{
                border: 1px solid {border_color};
                background-color: {bg_color_light};
                text-align: center;
                color: {text_color};
                border-radius: 8px;
                height: 20px;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_dark}, stop:1 {primary_light});
                border-radius: 6px;
            }}
            
            /* 콤보박스 */
            QComboBox {{
                padding: 8px 12px;
                background-color: {bg_color_light};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                selection-background-color: {primary_color};
                selection-color: white;
                min-height: 20px;
            }}
            
            QComboBox:focus {{
                border: 1px solid {primary_color};
                background-color: {bg_color};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {bg_color};
                color: {text_color};
                selection-background-color: {primary_color};
                selection-color: white;
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
            
            /* 체크박스 */
            QCheckBox {{
                spacing: 8px;
                background-color: transparent;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                background-color: {bg_color_light};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
            
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary_light}, stop:1 {primary_dark});
                border: none;
            }}
            
            /* 스크롤바 */
            QScrollBar:vertical {{
                background: {bg_color};
                width: 8px;
                margin: 2px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_color}70, stop:1 {primary_light}70);
                min-height: 30px;
                border-radius: 4px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            
            /* 테이블 위젯 */
            QTableWidget {{
                background-color: {bg_color};
                gridline-color: {border_color};
                border-radius: 8px;
                border: 1px solid {border_color};
            }}
            
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {border_color};
            }}
            
            QTableWidget::item:selected {{
                background-color: {primary_color}20;
                color: {text_color};
                border-radius: 4px;
            }}
            
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color_light}, stop:1 {bg_color});
                color: {secondary_text};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {primary_color}50;
                font-weight: bold;
            }}
            
            /* 그룹 박스 */
            QGroupBox {{
                border: 1px solid {border_color};
                border-radius: 10px;
                margin-top: 20px;
                background-color: {bg_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: {primary_color};
                font-weight: bold;
            }}
            
            /* 상태바 */
            QStatusBar {{
                background-color: {bg_color};
                color: {secondary_text};
            }}
            
            /* 내용 패딩 */
            #mainTabs > QWidget {{
                padding: 15px;
            }}
            
            /* 섹션 제목 스타일 */
            #sectionTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {primary_color};
            }}
            
            /* 설정 라벨 */
            #settingLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {text_color};
            }}
            
            /* 설정 섹션 */
            #settingsSection {{
                border: 1px solid {border_color};
                border-radius: 10px;
                background-color: {bg_color};
            }}
        """)
    
    def on_tab_changed(self, index):
        """탭 변경 처리"""
        if index == 2:  # 기록 탭
            self.history_widget.refresh_history()
    
    def center_window(self):
        """화면 중앙에 창 배치"""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())
    
    def init_services(self):
        """서비스 초기화"""
        # 위젯 시그널 연결
        self.send_widget.send_requested.connect(self.on_send_requested)
        self.receive_widget.receive_requested.connect(self.on_receive_requested)
        
        # 테마 변경 시그널 연결
        self.settings_widget.theme_changed.connect(self.on_theme_changed)
        
        # 버전 정보 설정
        if hasattr(self, 'croc_utils') and self.croc_utils:
            version = self.croc_utils.get_version()
            if version and hasattr(self, 'version_label'):
                self.version_label.setText(f"Croc v{version}")
        
        # 상태바 메시지
        self.statusBar().showMessage("Sirodrop - Secure File Transfer")
    
    def on_theme_changed(self, theme):
        """테마 변경 처리"""
        # 통합 스타일 업데이트
        self.apply_global_style(is_dark=theme == "dark")
        
        # 위젯 테마 업데이트
        self.send_widget.update_theme(theme)
        self.receive_widget.update_theme(theme)
        self.history_widget.update_theme(theme)
        
        # 상태바 메시지
        self.statusBar().showMessage(f"Theme changed to {theme} mode", 3000)
        
        # qdarktheme 설정 제거 (자체 테마 사용)
        QApplication.instance().setStyleSheet("")
    
    def on_send_requested(self, code, options):
        """전송 요청 처리"""
        pass
    
    def on_receive_requested(self, code, options):
        """수신 요청 처리"""
        pass
    
    def closeEvent(self, event):
        """창 닫기 이벤트 처리"""
        # 창 위치 및 크기 저장
        self.config.set_value("window_geometry", [
            self.x(), self.y(), self.width(), self.height()
        ])
        
        # 이벤트 수락
        event.accept()
    
    def create_app_icon(self):
        """앱 아이콘 생성"""
        icon_size = 256
        pixmap = QPixmap(icon_size, icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 배경 그리기
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#7b68ee"))
        
        path = QPainterPath()
        path.addRoundedRect(QRectF(10, 10, icon_size-20, icon_size-20), 30, 30)
        painter.drawPath(path)
        
        # 화살표 그리기
        painter.setBrush(QColor("#ffffff"))
        
        arrow_path = QPainterPath()
        arrow_path.moveTo(icon_size/2, icon_size/4)
        arrow_path.lineTo(icon_size*3/4, icon_size/2)
        arrow_path.lineTo(icon_size/2, icon_size*3/4)
        arrow_path.lineTo(icon_size/4, icon_size/2)
        arrow_path.closeSubpath()
        
        painter.drawPath(arrow_path)
        painter.end()
        
        return pixmap 