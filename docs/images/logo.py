import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QPixmap, QBrush, QPen
from PyQt6.QtCore import Qt, QRectF

def create_app_icon(size=256, save_path=None):
    """앱 아이콘 생성"""
    app = QApplication([])
    
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # 배경 그리기
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#7b68ee"))
    
    path = QPainterPath()
    path.addRoundedRect(QRectF(10, 10, size-20, size-20), 30, 30)
    painter.drawPath(path)
    
    # 화살표 그리기
    painter.setBrush(QColor("#ffffff"))
    
    arrow_path = QPainterPath()
    arrow_path.moveTo(size/2, size/4)
    arrow_path.lineTo(size*3/4, size/2)
    arrow_path.lineTo(size/2, size*3/4)
    arrow_path.lineTo(size/4, size/2)
    arrow_path.closeSubpath()
    
    painter.drawPath(arrow_path)
    painter.end()
    
    # 이미지 저장
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        pixmap.save(save_path)
    
    return pixmap

if __name__ == "__main__":
    # 현재 디렉토리 확인
    current_dir = Path(__file__).parent.absolute()
    
    # 로고 생성 및 저장
    logo_path = current_dir / "logo.png"
    create_app_icon(256, str(logo_path))
    
    print(f"로고가 생성되었습니다: {logo_path}") 