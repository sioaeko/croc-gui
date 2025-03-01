import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QProgressBar, QFrame,
    QApplication, QToolButton, QSizePolicy, QSpacerItem,
    QCheckBox, QGridLayout, QMessageBox, QListWidget,
    QListWidgetItem, QAbstractItemView, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QMimeData, QTimer, QRect, QPoint
from PyQt6.QtGui import (
    QIcon, QDragEnterEvent, QDropEvent, QPainter, QColor, QPen, QBrush,
    QPixmap, QPainterPath, QFont, QFontMetrics
)

class FileListWidget(QListWidget):
    """Custom ListWidget with drag and drop support for files"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.setMinimumHeight(150)
        # Add visual cue for drag and drop area
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #7b68ee;
                border-radius: 8px;
                background-color: rgba(123, 104, 238, 0.05);
                padding: 5px;
            }
        """)
        # 드롭 영역 안내 텍스트 표시 여부
        self.isEmpty = True
        # 폴더 아이콘 생성
        self.folder_icon = self.create_folder_icon()
        self.file_icon = self.create_file_icon()
        
    def create_folder_icon(self, size=64):
        """폴더 아이콘 생성"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 폴더 바디 색상 및 브러시 설정
        folder_color = QColor("#7b68ee")
        folder_color.setAlpha(180)
        painter.setBrush(QBrush(folder_color))
        painter.setPen(Qt.PenStyle.NoPen)
        
        # 폴더 본체 그리기
        folder_path = QPainterPath()
        folder_path.moveTo(5, 15)
        folder_path.lineTo(20, 15)
        folder_path.lineTo(25, 10)
        folder_path.lineTo(55, 10)
        folder_path.lineTo(55, 50)
        folder_path.lineTo(5, 50)
        folder_path.closeSubpath()
        painter.drawPath(folder_path)
        
        # 폴더 탭 그리기
        tab_color = QColor(folder_color)
        tab_color = tab_color.lighter(110)
        painter.setBrush(QBrush(tab_color))
        
        tab_path = QPainterPath()
        tab_path.moveTo(25, 10)
        tab_path.lineTo(25, 20)
        tab_path.lineTo(55, 20)
        tab_path.lineTo(55, 10)
        tab_path.closeSubpath()
        painter.drawPath(tab_path)
        
        painter.end()
        return pixmap

    def create_file_icon(self, size=64):
        """파일 아이콘 생성"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 파일 색상 및 브러시 설정
        file_color = QColor("#ffffff")
        file_border = QColor("#7b68ee")
        file_border.setAlpha(180)
        
        # 파일 본체 그리기
        painter.setBrush(QBrush(file_color))
        painter.setPen(QPen(file_border, 2))
        
        file_path = QPainterPath()
        file_path.moveTo(15, 5)
        file_path.lineTo(40, 5)
        file_path.lineTo(50, 15)
        file_path.lineTo(50, 55)
        file_path.lineTo(15, 55)
        file_path.closeSubpath()
        painter.drawPath(file_path)
        
        # 파일 접힌 모서리 그리기
        corner_path = QPainterPath()
        corner_path.moveTo(40, 5)
        corner_path.lineTo(40, 15)
        corner_path.lineTo(50, 15)
        corner_path.closeSubpath()
        painter.drawPath(corner_path)
        
        # 파일 라인 그리기
        painter.setPen(QPen(file_border, 1))
        painter.drawLine(20, 25, 45, 25)
        painter.drawLine(20, 35, 45, 35)
        painter.drawLine(20, 45, 35, 45)
        
        painter.end()
        return pixmap
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # Change border style during drag
            self.setStyleSheet("""
                QListWidget {
                    border: 2px dashed #6550e1;
                    border-radius: 8px;
                    background-color: rgba(123, 104, 238, 0.1);
                    padding: 5px;
                }
            """)
        else:
            super().dragEnterEvent(event)
    
    def dragLeaveEvent(self, event):
        # Reset style when drag leaves
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #7b68ee;
                border-radius: 8px;
                background-color: rgba(123, 104, 238, 0.05);
                padding: 5px;
            }
        """)
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    filepath = url.toLocalFile()
                    item = QListWidgetItem(filepath)
                    
                    # 파일인지 폴더인지에 따라 아이콘 설정
                    if os.path.isdir(filepath):
                        item.setIcon(QIcon(self.folder_icon))
                    else:
                        item.setIcon(QIcon(self.file_icon))
                    
                    self.addItem(item)
            event.acceptProposedAction()
            # 아이템이 추가되면 isEmpty 상태 업데이트
            self.isEmpty = self.count() == 0
            # Reset style after drop
            self.setStyleSheet("""
                QListWidget {
                    border: 2px dashed #7b68ee;
                    border-radius: 8px;
                    background-color: rgba(123, 104, 238, 0.05);
                    padding: 5px;
                }
            """)
            self.update()
        else:
            super().dropEvent(event)
    
    def addItem(self, *args, **kwargs):
        if isinstance(args[0], str):
            # 문자열로 추가하는 경우 아이콘을 설정
            item = QListWidgetItem(args[0])
            if os.path.isdir(args[0]):
                item.setIcon(QIcon(self.folder_icon))
            else:
                item.setIcon(QIcon(self.file_icon))
            super().addItem(item)
        else:
            # QListWidgetItem으로 추가하는 경우
            super().addItem(*args, **kwargs)
        
        self.isEmpty = False
        self.update()
    
    def clear(self):
        super().clear()
        self.isEmpty = True
        self.update()
    
    def takeItem(self, *args, **kwargs):
        result = super().takeItem(*args, **kwargs)
        self.isEmpty = self.count() == 0
        self.update()
        return result
    
    def paintEvent(self, event):
        super().paintEvent(event)
        # 빈 상태일 때만 안내 텍스트와 아이콘 표시
        if self.isEmpty:
            painter = QPainter(self.viewport())
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 아이콘 크기와 위치 계산
            icon_size = min(self.width() / 3, 80)
            icon_x = (self.width() - icon_size) / 2
            icon_y = (self.height() - icon_size) / 2 - 20
            
            # 폴더 아이콘과 파일 아이콘 그리기
            folder_icon_rect = QRect(
                int(icon_x - icon_size/2), 
                int(icon_y), 
                int(icon_size), 
                int(icon_size)
            )
            file_icon_rect = QRect(
                int(icon_x + icon_size/2), 
                int(icon_y), 
                int(icon_size), 
                int(icon_size)
            )
            
            painter.drawPixmap(folder_icon_rect, self.folder_icon)
            painter.drawPixmap(file_icon_rect, self.file_icon)
            
            # 안내 텍스트 그리기
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.setPen(QPen(QColor("#666666")))
            
            text_rect = QRect(
                0, 
                int(icon_y + icon_size + 10), 
                self.width(), 
                30
            )
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "여기에 파일과 폴더를 드래그하세요")
            
            # 추가 안내 텍스트
            font.setPointSize(9)
            painter.setFont(font)
            text_rect2 = QRect(
                0, 
                int(icon_y + icon_size + 35), 
                self.width(), 
                20
            )
            painter.drawText(text_rect2, Qt.AlignmentFlag.AlignCenter, "또는 찾아보기 버튼을 사용하세요")
            
            painter.end()

class SendWidget(QWidget):
    # Define signals
    send_requested = pyqtSignal(str, object)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
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
        self.create_file_section()
        self.create_code_section()
        self.create_progress_section()
        
        # Add stretch to push all elements to the top
        self.main_layout.addStretch(1)
    
    def create_file_section(self):
        # 제목과 설명을 하나로 묶음
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # 간결한 제목
        title_label = QLabel("전송할 파일")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # File selection control
        file_input_layout = QHBoxLayout()
        file_input_layout.setContentsMargins(0, 0, 0, 0)
        file_input_layout.setSpacing(8)
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("파일 경로")
        
        # 아이콘 생성
        folder_icon = self.create_icon("folder")
        add_icon = self.create_icon("plus")
        
        # 파일 찾기 버튼
        browse_button = QPushButton("찾아보기")
        browse_button.setIcon(folder_icon)
        browse_button.setMinimumWidth(100)
        browse_button.clicked.connect(self.browse_file)
        
        # 추가 버튼
        add_button = QPushButton("추가")
        add_button.setIcon(add_icon)
        add_button.setMinimumWidth(80)
        add_button.clicked.connect(self.add_file)
        
        file_input_layout.addWidget(self.file_path_edit, 1)
        file_input_layout.addWidget(browse_button)
        file_input_layout.addWidget(add_button)
        
        # 파일 목록
        file_list_layout = QVBoxLayout()
        file_list_layout.setContentsMargins(0, 10, 0, 0)
        file_list_layout.setSpacing(5)
        
        # 파일 목록 설명
        list_label = QLabel("파일 또는 폴더를 드래그 앤 드롭하거나 추가 버튼을 사용하세요.")
        list_label.setStyleSheet("color: #666666; font-size: 12px;")
        
        # 파일 목록 위젯
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(150)
        
        # 파일 목록 버튼
        list_button_layout = QHBoxLayout()
        list_button_layout.setContentsMargins(0, 10, 0, 0)  # 버튼과 리스트 사이 간격 증가
        list_button_layout.setSpacing(8)
        
        # 아이콘 생성
        trash_icon = self.create_icon("trash")
        clear_icon = self.create_icon("clear")
        
        self.remove_button = QPushButton("선택 제거")
        self.remove_button.setIcon(trash_icon)
        self.remove_button.clicked.connect(self.remove_selected_files)
        
        self.clear_button = QPushButton("모두 제거")
        self.clear_button.setIcon(clear_icon)
        self.clear_button.clicked.connect(self.clear_files)
        
        list_button_layout.addWidget(self.remove_button)
        list_button_layout.addWidget(self.clear_button)
        list_button_layout.addStretch(1)
        
        file_list_layout.addWidget(list_label)
        file_list_layout.addWidget(self.file_list)
        file_list_layout.addLayout(list_button_layout)
        
        # 모든 컴포넌트 합치기
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        section_layout.addWidget(title_container)
        section_layout.addLayout(file_input_layout)
        section_layout.addLayout(file_list_layout)
        
        self.main_layout.addLayout(section_layout)
        
        # 섹션 구분선
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: transparent;")
        
        self.main_layout.addWidget(divider)
        
    def create_code_section(self):
        # 제목 레이아웃
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        # 간결한 제목
        title_label = QLabel("보내는 방법 선택")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # 코드 생성 옵션
        code_options_layout = QVBoxLayout()
        code_options_layout.setContentsMargins(0, 10, 0, 0)
        code_options_layout.setSpacing(15)
        
        # 코드 입력 필드
        code_input_layout = QHBoxLayout()
        code_input_layout.setContentsMargins(0, 0, 0, 0)
        code_input_layout.setSpacing(8)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("코드 입력 (선택사항)")
        
        # 아이콘 생성
        refresh_icon = self.create_icon("refresh")
        
        generate_button = QPushButton("코드 생성")
        generate_button.setIcon(refresh_icon)
        generate_button.setMinimumWidth(120)
        generate_button.clicked.connect(self.generate_code)
        
        code_input_layout.addWidget(self.code_input, 1)
        code_input_layout.addWidget(generate_button)
        
        # 설정 옵션
        options_layout = QVBoxLayout()
        options_layout.setContentsMargins(0, 10, 0, 0)
        options_layout.setSpacing(10)
        
        # 옵션 1: 암호화
        self.encrypt_check = QCheckBox("파일 암호화 사용")
        self.encrypt_check.setChecked(True)
        
        # 옵션 2: 압축
        self.zip_check = QCheckBox("ZIP 압축 적용")
        self.zip_check.setChecked(True)
        
        options_layout.addWidget(self.encrypt_check)
        options_layout.addWidget(self.zip_check)
        
        # 전송 버튼
        send_button_layout = QHBoxLayout()
        send_button_layout.setContentsMargins(0, 15, 0, 0)
        send_button_layout.addStretch(1)
        
        # 아이콘 생성
        send_icon = self.create_icon("send")
        
        self.send_button = QPushButton("전송 시작")
        self.send_button.setIcon(send_icon)
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setMinimumWidth(150)
        self.send_button.setMinimumHeight(50)
        self.send_button.clicked.connect(self.send_files)
        
        send_button_layout.addWidget(self.send_button)
        send_button_layout.addStretch(1)
        
        # 전체 레이아웃
        code_options_layout.addLayout(code_input_layout)
        code_options_layout.addLayout(options_layout)
        code_options_layout.addLayout(send_button_layout)
        
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        section_layout.addWidget(title_container)
        section_layout.addLayout(code_options_layout)
        
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
        
        # 간결한 제목
        title_label = QLabel("전송 상태")
        title_label.setObjectName("sectionTitle")
        title_layout.addWidget(title_label)
        
        # 진행 상태 표시
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 10, 0, 0)
        progress_layout.setSpacing(10)
        
        # 파일 이름과 크기
        self.file_info_label = QLabel("파일을 선택해주세요")
        self.file_info_label.setStyleSheet("color: #666666;")
        
        # 진행 상태 바
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
    
    def create_icon(self, icon_type, size=16):
        """아이콘 생성 함수"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 아이콘 색상
        icon_color = QColor("#7b68ee")
        painter.setPen(QPen(icon_color, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.transparent))
        
        if icon_type == "folder":
            # 폴더 아이콘
            painter.drawRect(2, 4, 12, 9)
            painter.drawRect(1, 7, 14, 8)
            
        elif icon_type == "plus":
            # 플러스 아이콘
            painter.drawLine(8, 3, 8, 13)
            painter.drawLine(3, 8, 13, 8)
            
        elif icon_type == "trash":
            # 삭제 아이콘
            painter.drawRect(3, 3, 10, 2)
            painter.drawLine(5, 3, 5, 1)
            painter.drawLine(11, 3, 11, 1)
            painter.drawLine(7, 3, 7, 1)
            painter.drawLine(4, 5, 4, 14)
            painter.drawLine(12, 5, 12, 14)
            painter.drawLine(4, 14, 12, 14)
            painter.drawLine(6, 7, 6, 12)
            painter.drawLine(8, 7, 8, 12)
            painter.drawLine(10, 7, 10, 12)
            
        elif icon_type == "clear":
            # 초기화 아이콘
            painter.drawArc(3, 3, 10, 10, 0, 5760)
            painter.drawLine(8, 8, 8, 3)
            painter.drawLine(8, 3, 11, 3)
            
        elif icon_type == "refresh":
            # 새로고침 아이콘
            path = QPainterPath()
            path.moveTo(8, 2)
            path.arcTo(3, 3, 10, 10, 90, 270)
            path.moveTo(8, 2)
            path.lineTo(11, 5)
            path.lineTo(5, 5)
            path.closeSubpath()
            painter.drawPath(path)
            
        elif icon_type == "send":
            # 전송 아이콘
            path = QPainterPath()
            path.moveTo(2, 8)
            path.lineTo(10, 3)
            path.lineTo(10, 6)
            path.lineTo(14, 6)
            path.lineTo(14, 10)
            path.lineTo(10, 10)
            path.lineTo(10, 13)
            path.closeSubpath()
            painter.setBrush(QBrush(icon_color))
            painter.drawPath(path)
        
        painter.end()
        return QIcon(pixmap)
    
    def update_theme(self, theme):
        """테마에 따라 위젯 스타일 업데이트"""
        is_dark = theme == "dark"
        
        # 테마 색상 정의
        if is_dark:
            # 다크 테마
            primary_color = "#7b68ee"
            bg_color = "#191919"
            text_color = "#f0f0f0"
            secondary_text = "#a0a0a0"
            list_bg = "#191919"
            list_alt_bg = "#202020"
            drop_area_bg = "rgba(123, 104, 238, 0.1)"
        else:
            # 라이트 테마
            primary_color = "#7b68ee"
            bg_color = "#ffffff"
            text_color = "#333333"
            secondary_text = "#666666"
            list_bg = "#ffffff"
            list_alt_bg = "#f5f5f5"
            drop_area_bg = "rgba(123, 104, 238, 0.05)"
        
        # 섹션 제목 스타일
        for widget in self.findChildren(QLabel):
            if widget.objectName() == "sectionTitle":
                widget.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {primary_color};")
        
        # 파일 목록 스타일 - 드래그 앤 드롭 시각적 표시 강화
        self.file_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {drop_area_bg};
                color: {text_color};
                border: 2px dashed {primary_color};
                border-radius: 8px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {secondary_text}30;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {primary_color}20;
                color: {text_color};
            }}
            QListWidget::item:alternate {{
                background-color: {list_alt_bg};
            }}
        """)
        
        # 버튼 스타일은 메인 윈도우의 글로벌 스타일로 처리됨
        # 진행 바 스타일은 메인 윈도우의 글로벌 스타일로 처리됨
    
    def browse_file(self):
        """파일 브라우저 열기"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "파일 선택", 
            self.config.get_value("default_dir", str(Path.home())),
            "모든 파일 (*.*)"
        )
        
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def add_file(self):
        """파일 목록에 파일 추가"""
        file_path = self.file_path_edit.text().strip()
        if file_path and os.path.exists(file_path):
            item = QListWidgetItem(file_path)
            # 파일인지 폴더인지에 따라 아이콘 설정
            if os.path.isdir(file_path):
                item.setIcon(QIcon(self.file_list.folder_icon))
            else:
                item.setIcon(QIcon(self.file_list.file_icon))
            
            self.file_list.addItem(item)
            self.file_path_edit.clear()
            self.update_file_info()
        else:
            QMessageBox.warning(self, "경고", "유효한 파일 경로를 입력해주세요.")
    
    def remove_selected_files(self):
        """선택된 파일 제거"""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))
        self.update_file_info()
    
    def clear_files(self):
        """모든 파일 제거"""
        self.file_list.clear()
        self.update_file_info()
    
    def update_file_info(self):
        """파일 정보 업데이트"""
        count = self.file_list.count()
        if count > 0:
            self.file_info_label.setText(f"선택된 파일: {count}개")
        else:
            self.file_info_label.setText("파일을 선택해주세요")
            self.file_list.isEmpty = True
            self.file_list.update()
    
    def generate_code(self):
        """코드 생성"""
        # 실제로는 서비스에서 코드 생성
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.code_input.setText(code)
    
    def send_files(self):
        """파일 전송 시작"""
        count = self.file_list.count()
        if count == 0:
            QMessageBox.warning(self, "경고", "전송할 파일을 추가해주세요.")
            return
        
        code = self.code_input.text().strip()
        if not code:
            self.generate_code()
            code = self.code_input.text()
        
        # 전송 옵션 설정
        options = {
            'encrypt': self.encrypt_check.isChecked(),
            'zip': self.zip_check.isChecked(),
            'files': [self.file_list.item(i).text() for i in range(self.file_list.count())]
        }
        
        # 전송 요청 신호 발생
        self.send_requested.emit(code, options)
        
        # UI 업데이트
        self.status_label.setText("전송 준비 중...")
        
        # 실제 구현에서는 백그라운드 작업으로 처리하고 진행 상황을 업데이트함
        # 여기서는 데모용으로 타이머 사용
        QTimer.singleShot(1000, self.simulate_progress)
    
    def simulate_progress(self):
        """전송 진행 상태 시뮬레이션 (데모용)"""
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
            self.status_label.setText(f"전송 중... {current + 10}%")
            QTimer.singleShot(500, self.simulate_progress)
        else:
            self.status_label.setText("전송 완료!")
            QTimer.singleShot(2000, self.reset_progress)
    
    def reset_progress(self):
        """진행 상태 초기화"""
        self.progress_bar.setValue(0)
        self.status_label.setText("준비됨") 