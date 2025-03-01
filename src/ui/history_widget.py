import os
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QMenu, QMessageBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QIcon, QAction, QColor, QCursor, QFont

class HistoryWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.update_theme(self.config.get_value("theme", "light"))
        self.refresh_history()
    
    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        # 상단 컨테이너 (타이틀 + 버튼)
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 10)
        
        # 제목
        title_label = QLabel("전송 기록")
        title_label.setObjectName("sectionTitle")
        
        # 버튼 영역
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # 새로고침 버튼
        self.refresh_button = QPushButton("새로고침")
        self.refresh_button.clicked.connect(self.refresh_history)
        self.refresh_button.setFixedSize(100, 36)
        
        # 기록 삭제 버튼
        self.clear_button = QPushButton("기록 삭제")
        self.clear_button.clicked.connect(self.clear_history)
        self.clear_button.setFixedSize(100, 36)
        
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.clear_button)
        
        top_layout.addWidget(title_label)
        top_layout.addStretch(1)
        top_layout.addWidget(button_container)
        
        self.main_layout.addWidget(top_container)
        
        # 기록 테이블
        self.create_history_table()
    
    def create_history_table(self):
        """기록 테이블 생성"""
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["날짜", "파일", "크기", "유형"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # 테이블 설정
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.history_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.main_layout.addWidget(self.history_table)
    
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
                widget.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {primary_color};")
    
    def refresh_history(self):
        """기록 새로고침"""
        # 실제 구현에서는 설정이나 DB에서 기록 로드
        self.history_table.setRowCount(0)  # 테이블 초기화
        
        # 샘플 데이터 (실제로는 저장된 기록 사용)
        sample_data = [
            {"date": "2025-03-01 14:30", "file": "project_report.pdf", "size": "2.5 MB", "type": "보냄"},
            {"date": "2025-03-01 12:15", "file": "presentation.pptx", "size": "4.8 MB", "type": "받음"},
            {"date": "2025-02-28 18:45", "file": "source_code.zip", "size": "1.2 MB", "type": "보냄"},
            {"date": "2025-02-28 10:20", "file": "meeting_notes.docx", "size": "0.5 MB", "type": "받음"},
            {"date": "2025-02-27 16:10", "file": "images.zip", "size": "8.7 MB", "type": "보냄"}
        ]
        
        # 테이블에 데이터 추가
        for row, data in enumerate(sample_data):
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(data["date"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(data["file"]))
            self.history_table.setItem(row, 2, QTableWidgetItem(data["size"]))
            
            type_item = QTableWidgetItem(data["type"])
            if data["type"] == "보냄":
                type_item.setForeground(QColor("#7b68ee"))  # 보낸 파일은 보라색
            else:
                type_item.setForeground(QColor("#4CAF50"))  # 받은 파일은 초록색
            
            self.history_table.setItem(row, 3, type_item)
    
    def clear_history(self):
        """기록 삭제"""
        reply = QMessageBox.question(
            self, "기록 삭제", 
            "모든 전송 기록을 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.history_table.setRowCount(0)
            # 실제 구현에서는 저장된 기록 삭제
    
    def show_context_menu(self, position):
        """테이블에 컨텍스트 메뉴 표시"""
        menu = QMenu(self)
        
        # 선택된 행 확인
        if self.history_table.selectedItems():
            # 액션 추가
            open_location_action = QAction("저장 위치 열기", self)
            open_location_action.triggered.connect(self.open_file_location)
            
            delete_action = QAction("항목 삭제", self)
            delete_action.triggered.connect(self.delete_selected_items)
            
            # 액션 메뉴에 추가
            menu.addAction(open_location_action)
            menu.addAction(delete_action)
            
            # 메뉴 표시
            menu.popup(QCursor.pos())
    
    def open_file_location(self):
        """선택한 파일 위치 열기"""
        if not self.history_table.selectedItems():
            return
        
        # 실제 구현에서는 파일 경로 가져오기
        row = self.history_table.currentRow()
        file_name = self.history_table.item(row, 1).text()
        
        # 임시로 경로 지정 (실제로는 저장된 경로 사용)
        downloads_path = str(Path.home() / "Downloads")
        
        # 파일 위치 열기 (실제로는 OS에 맞게 처리)
        QMessageBox.information(
            self, 
            "파일 위치", 
            f"이 기능은 데모입니다. 실제로는 다음 경로가 열립니다:\n{downloads_path}"
        )
    
    def delete_selected_items(self):
        """선택한 항목 삭제"""
        if not self.history_table.selectedItems():
            return
        
        reply = QMessageBox.question(
            self, 
            "항목 삭제", 
            "선택한 기록을 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 선택된 행 제거 (역순으로 삭제하여 인덱스 문제 방지)
            rows = sorted(set(item.row() for item in self.history_table.selectedItems()), reverse=True)
            for row in rows:
                self.history_table.removeRow(row)
            # 실제 구현에서는 DB에서 삭제 