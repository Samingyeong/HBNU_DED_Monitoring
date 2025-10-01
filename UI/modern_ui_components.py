"""
Modern UI Components for DED Monitoring Application
Enhanced components with professional styling and better UX
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyqtgraph as pg
from .modern_style import ModernStyle

class ModernDataCard(QFrame):
    """Modern card widget for displaying sensor data"""
    
    def __init__(self, title="", value="", unit="", status="normal", parent=None):
        super().__init__(parent)
        self.setObjectName("data_card")
        self.setup_ui(title, value, unit, status)
    
    def setup_ui(self, title, value, unit, status):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "label")
        layout.addWidget(self.title_label)
        
        # Value and unit container
        value_container = QHBoxLayout()
        value_container.setSpacing(4)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setProperty("class", "value")
        value_container.addWidget(self.value_label)
        
        # Unit
        if unit:
            self.unit_label = QLabel(unit)
            self.unit_label.setProperty("class", "unit")
            value_container.addWidget(self.unit_label)
        
        value_container.addStretch()
        layout.addLayout(value_container)
        
        # Status indicator
        self.status_label = QLabel()
        self.set_status(status)
        layout.addWidget(self.status_label)
        
        # Apply modern styling
        ModernStyle.apply_modern_style(self)
    
    def set_value(self, value):
        """Update the displayed value"""
        self.value_label.setText(str(value))
    
    def set_status(self, status):
        """Update the status indicator"""
        status_text = {
            'online': '● 온라인',
            'offline': '● 오프라인',
            'warning': '⚠ 경고',
            'error': '✗ 오류',
            'processing': '⟳ 처리중',
            'normal': ''
        }.get(status.lower(), '')
        
        self.status_label.setText(status_text)
        self.status_label.setProperty("class", f"status_{status.lower()}")
        self.status_label.setStyleSheet(self.styleSheet())

class ModernGraphWidget(QFrame):
    """Enhanced graph widget with modern styling"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("graph_container")
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "label")
            layout.addWidget(title_label)
        
        # Graph widget
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        self.graph_widget.setLabel('left', 'Value')
        self.graph_widget.setLabel('bottom', 'Time')
        
        # Style the graph
        self.style_graph()
        
        layout.addWidget(self.graph_widget)
        
        # Apply modern styling
        ModernStyle.apply_modern_style(self)
    
    def style_graph(self):
        """Apply modern styling to the graph"""
        # Set colors
        self.graph_widget.getAxis('left').setPen(pg.mkPen(color=ModernStyle.COLORS['on_surface']))
        self.graph_widget.getAxis('bottom').setPen(pg.mkPen(color=ModernStyle.COLORS['on_surface']))
        
        # Style grid
        self.graph_widget.getAxis('left').setGrid(255)
        self.graph_widget.getAxis('bottom').setGrid(255)
        
        # Set font
        font = QFont('Segoe UI', 10)
        self.graph_widget.getAxis('left').setTickFont(font)
        self.graph_widget.getAxis('bottom').setTickFont(font)
        self.graph_widget.getAxis('left').setLabelFont(font)
        self.graph_widget.getAxis('bottom').setLabelFont(font)
    
    def add_plot(self, pen_color=None):
        """Add a new plot line"""
        if pen_color is None:
            pen_color = ModernStyle.COLORS['primary']
        
        pen = pg.mkPen(color=pen_color, width=2)
        return self.graph_widget.plot(pen=pen)

class ModernStatusIndicator(QFrame):
    """Modern status indicator with icon and text"""
    
    def __init__(self, text="", status="normal", parent=None):
        super().__init__(parent)
        self.setup_ui(text, status)
    
    def setup_ui(self, text, status):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        
        # Status icon
        self.status_icon = QLabel()
        layout.addWidget(self.status_icon)
        
        # Status text
        self.status_text = QLabel(text)
        layout.addWidget(self.status_text)
        
        layout.addStretch()
        
        self.set_status(status)
        ModernStyle.apply_modern_style(self)
    
    def set_status(self, status):
        """Update status with appropriate icon and color"""
        status_config = {
            'online': ('●', ModernStyle.COLORS['status_online']),
            'offline': ('●', ModernStyle.COLORS['status_offline']),
            'warning': ('⚠', ModernStyle.COLORS['status_warning']),
            'error': ('✗', ModernStyle.COLORS['status_offline']),
            'processing': ('⟳', ModernStyle.COLORS['status_processing']),
            'normal': ('', ModernStyle.COLORS['on_surface_variant'])
        }
        
        icon, color = status_config.get(status.lower(), ('', ModernStyle.COLORS['on_surface_variant']))
        self.status_icon.setText(icon)
        self.status_icon.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        self.status_text.setStyleSheet(f"color: {color}; font-weight: 600;")

class ModernButton(QPushButton):
    """Enhanced button with modern styling and animations"""
    
    def __init__(self, text="", icon=None, button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setup_ui(icon)
    
    def setup_ui(self, icon):
        if icon:
            self.setIcon(icon)
        
        # Set object name for specific styling
        self.setObjectName(f"{self.button_type}_btn")
        
        # Apply modern styling
        ModernStyle.apply_modern_style(self)
        
        # Set cursor
        self.setCursor(Qt.PointingHandCursor)

class ModernImageDisplay(QFrame):
    """Enhanced image display widget"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("image_container")
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "label")
            layout.addWidget(title_label)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setObjectName("image_label")
        self.image_label.setMinimumSize(320, 240)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("이미지 없음")
        layout.addWidget(self.image_label)
        
        # Status bar
        self.status_bar = QLabel()
        self.status_bar.setProperty("class", "unit")
        layout.addWidget(self.status_bar)
        
        ModernStyle.apply_modern_style(self)
    
    def set_image(self, image):
        """Set the displayed image"""
        if image is not None:
            # Convert numpy array to QPixmap
            if hasattr(image, 'shape'):  # numpy array
                height, width = image.shape[:2]
                bytes_per_line = 3 * width
                q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
            else:
                pixmap = image
            
            # Scale to fit
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.status_bar.setText(f"이미지 크기: {width}x{height}")
        else:
            self.image_label.setText("이미지 없음")
            self.status_bar.setText("")

class ModernControlPanel(QFrame):
    """Modern control panel with organized buttons"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("Control")
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "label")
            layout.addWidget(title_label)
        
        # Button container
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(8)
        layout.addLayout(self.button_layout)
        
        ModernStyle.apply_modern_style(self)
    
    def add_button(self, text, button_type="primary", callback=None):
        """Add a button to the control panel"""
        button = ModernButton(text, button_type=button_type)
        if callback:
            button.clicked.connect(callback)
        self.button_layout.addWidget(button)
        return button

class ModernHeader(QFrame):
    """Modern header with logo, title, and time"""
    
    def __init__(self, title="DED 모니터링 시스템", parent=None):
        super().__init__(parent)
        self.setObjectName("Top")
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(16)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(":/logo/AMS_logo.png"))
        layout.addWidget(self.logo_label)
        
        # Title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            color: {ModernStyle.COLORS['on_primary']};
            font-size: 20px;
            font-weight: 600;
        """)
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # Time display
        self.time_display = QDateTimeEdit()
        self.time_display.setObjectName("current_time")
        self.time_display.setDisplayFormat("yyyy-MM-dd AP h:mm:ss")
        self.time_display.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.time_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_display)
        
        ModernStyle.apply_modern_style(self)
    
    def update_time(self):
        """Update the time display"""
        self.time_display.setDateTime(QDateTime.currentDateTime())

def create_modern_layout():
    """Create a modern layout with proper spacing and organization"""
    layout = QGridLayout()
    layout.setSpacing(16)
    layout.setContentsMargins(16, 16, 16, 16)
    return layout

def apply_card_style(widget, title=""):
    """Apply card styling to any widget"""
    widget.setObjectName("data_card")
    if title:
        # Create a container with title
        container = QFrame()
        container.setObjectName("data_card")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setProperty("class", "label")
        container_layout.addWidget(title_label)
        
        container_layout.addWidget(widget)
        
        ModernStyle.apply_modern_style(container)
        return container
    else:
        ModernStyle.apply_modern_style(widget)
        return widget
