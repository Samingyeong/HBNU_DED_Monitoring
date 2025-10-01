"""
Modern Animations and Interactions for DED Monitoring Application
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .modern_style import ModernStyle

class ModernAnimationManager:
    """Manages modern animations and interactions"""
    
    def __init__(self):
        self.animations = {}
    
    def create_hover_animation(self, widget, scale_factor=1.05, duration=200):
        """Create a hover scale animation for a widget"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        # Store original geometry
        original_geometry = widget.geometry()
        
        def on_hover_enter():
            # Scale up slightly
            center = original_geometry.center()
            new_width = int(original_geometry.width() * scale_factor)
            new_height = int(original_geometry.height() * scale_factor)
            new_x = center.x() - new_width // 2
            new_y = center.y() - new_height // 2
            
            animation.setStartValue(original_geometry)
            animation.setEndValue(QRect(new_x, new_y, new_width, new_height))
            animation.start()
        
        def on_hover_leave():
            # Scale back to original
            animation.setStartValue(widget.geometry())
            animation.setEndValue(original_geometry)
            animation.start()
        
        # Connect hover events
        widget.enterEvent = lambda event: on_hover_enter()
        widget.leaveEvent = lambda event: on_hover_leave()
        
        return animation
    
    def create_pulse_animation(self, widget, duration=1000):
        """Create a pulsing animation for attention-grabbing elements"""
        animation = QPropertyAnimation(widget, b"styleSheet")
        animation.setDuration(duration)
        animation.setLoopCount(-1)  # Infinite loop
        
        # Create pulsing effect with opacity
        animation.setStartValue(f"""
            background-color: {ModernStyle.COLORS['primary']};
            border-radius: 8px;
            opacity: 0.7;
        """)
        animation.setEndValue(f"""
            background-color: {ModernStyle.COLORS['primary']};
            border-radius: 8px;
            opacity: 1.0;
        """)
        
        return animation
    
    def create_slide_animation(self, widget, direction="right", duration=300):
        """Create a slide-in animation"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        original_geometry = widget.geometry()
        
        if direction == "right":
            start_geometry = QRect(
                original_geometry.x() + original_geometry.width(),
                original_geometry.y(),
                original_geometry.width(),
                original_geometry.height()
            )
        elif direction == "left":
            start_geometry = QRect(
                original_geometry.x() - original_geometry.width(),
                original_geometry.y(),
                original_geometry.width(),
                original_geometry.height()
            )
        elif direction == "up":
            start_geometry = QRect(
                original_geometry.x(),
                original_geometry.y() - original_geometry.height(),
                original_geometry.width(),
                original_geometry.height()
            )
        elif direction == "down":
            start_geometry = QRect(
                original_geometry.x(),
                original_geometry.y() + original_geometry.height(),
                original_geometry.width(),
                original_geometry.height()
            )
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(original_geometry)
        
        return animation
    
    def create_fade_animation(self, widget, duration=300):
        """Create a fade-in/fade-out animation"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        
        return animation
    
    def create_rotation_animation(self, widget, duration=1000):
        """Create a rotation animation (useful for loading indicators)"""
        animation = QPropertyAnimation(widget, b"rotation")
        animation.setDuration(duration)
        animation.setLoopCount(-1)
        animation.setStartValue(0)
        animation.setEndValue(360)
        
        return animation

class ModernButton(QPushButton):
    """Enhanced button with modern animations and interactions"""
    
    def __init__(self, text="", icon=None, button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.animation_manager = ModernAnimationManager()
        self.setup_ui(icon)
        self.setup_animations()
    
    def setup_ui(self, icon):
        if icon:
            self.setIcon(icon)
        
        # Set object name for specific styling
        self.setObjectName(f"{self.button_type}_btn")
        
        # Apply modern styling
        from .modern_style import ModernStyle
        ModernStyle.apply_modern_style(self)
        
        # Set cursor
        self.setCursor(Qt.PointingHandCursor)
    
    def setup_animations(self):
        """Setup button animations"""
        # Create hover animation
        self.hover_animation = self.animation_manager.create_hover_animation(self)
        
        # Create click animation
        self.click_animation = QPropertyAnimation(self, b"styleSheet")
        self.click_animation.setDuration(100)
    
    def mousePressEvent(self, event):
        """Handle mouse press with animation"""
        if event.button() == Qt.LeftButton:
            # Create press effect
            self.click_animation.setStartValue(self.styleSheet())
            self.click_animation.setEndValue(f"""
                {self.styleSheet()}
                background-color: {ModernStyle.COLORS['primary_dark']};
                transform: translateY(1px);
            """)
            self.click_animation.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release with animation"""
        if event.button() == Qt.LeftButton:
            # Restore original style
            self.click_animation.setStartValue(self.styleSheet())
            self.click_animation.setEndValue(self.styleSheet().replace(
                ModernStyle.COLORS['primary_dark'],
                ModernStyle.COLORS['primary']
            ).replace("transform: translateY(1px);", ""))
            self.click_animation.start()
        
        super().mouseReleaseEvent(event)

class ModernDataCard(QFrame):
    """Enhanced data card with animations"""
    
    def __init__(self, title="", value="", unit="", status="normal", parent=None):
        super().__init__(parent)
        self.setObjectName("data_card")
        self.animation_manager = ModernAnimationManager()
        self.setup_ui(title, value, unit, status)
        self.setup_animations()
    
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
        from .modern_style import ModernStyle
        ModernStyle.apply_modern_style(self)
    
    def setup_animations(self):
        """Setup card animations"""
        # Create hover animation
        self.hover_animation = self.animation_manager.create_hover_animation(self, scale_factor=1.02)
        
        # Create value change animation
        self.value_animation = QPropertyAnimation(self.value_label, b"styleSheet")
        self.value_animation.setDuration(300)
    
    def set_value(self, value):
        """Update the displayed value with animation"""
        old_value = self.value_label.text()
        self.value_label.setText(str(value))
        
        # Animate value change
        if old_value != str(value):
            self.animate_value_change()
    
    def animate_value_change(self):
        """Animate value change with highlight effect"""
        original_style = self.value_label.styleSheet()
        
        # Highlight effect
        self.value_animation.setStartValue(original_style)
        self.value_animation.setEndValue(f"""
            {original_style}
            color: {ModernStyle.COLORS['secondary']};
            font-weight: 800;
        """)
        self.value_animation.start()
        
        # Restore original style after animation
        QTimer.singleShot(300, lambda: self.value_label.setStyleSheet(original_style))
    
    def set_status(self, status):
        """Update the status indicator with animation"""
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
        
        # Animate status change
        if status.lower() in ['warning', 'error']:
            self.animate_status_warning()
    
    def animate_status_warning(self):
        """Animate warning/error status with pulse effect"""
        pulse_animation = self.animation_manager.create_pulse_animation(self.status_label)
        pulse_animation.start()
        
        # Stop animation after 3 seconds
        QTimer.singleShot(3000, pulse_animation.stop)

class ModernLoadingIndicator(QWidget):
    """Modern loading indicator with rotation animation"""
    
    def __init__(self, text="로딩 중...", parent=None):
        super().__init__(parent)
        self.setup_ui(text)
        self.setup_animations()
    
    def setup_ui(self, text):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Loading spinner
        self.spinner = QLabel("⟳")
        self.spinner.setAlignment(Qt.AlignCenter)
        self.spinner.setStyleSheet(f"""
            font-size: 24px;
            color: {ModernStyle.COLORS['primary']};
        """)
        layout.addWidget(self.spinner)
        
        # Loading text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setProperty("class", "label")
        layout.addWidget(self.text_label)
        
        from .modern_style import ModernStyle
        ModernStyle.apply_modern_style(self)
    
    def setup_animations(self):
        """Setup loading animations"""
        self.animation_manager = ModernAnimationManager()
        self.rotation_animation = self.animation_manager.create_rotation_animation(self.spinner)
    
    def start_loading(self):
        """Start the loading animation"""
        self.show()
        self.rotation_animation.start()
    
    def stop_loading(self):
        """Stop the loading animation"""
        self.rotation_animation.stop()
        self.hide()

def create_modern_tooltip(widget, text, position="top"):
    """Create a modern tooltip for a widget"""
    tooltip = QLabel(text)
    tooltip.setObjectName("modern_tooltip")
    tooltip.setStyleSheet(f"""
        background-color: {ModernStyle.COLORS['surface']};
        border: 1px solid {ModernStyle.COLORS['outline']};
        border-radius: 6px;
        color: {ModernStyle.COLORS['on_surface']};
        font-size: 12px;
        padding: 8px;
        margin: 4px;
    """)
    
    # Position tooltip
    if position == "top":
        tooltip.move(widget.x(), widget.y() - tooltip.height() - 10)
    elif position == "bottom":
        tooltip.move(widget.x(), widget.y() + widget.height() + 10)
    elif position == "left":
        tooltip.move(widget.x() - tooltip.width() - 10, widget.y())
    elif position == "right":
        tooltip.move(widget.x() + widget.width() + 10, widget.y())
    
    return tooltip
