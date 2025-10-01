"""
UI Enhancer for adding modern components to existing DED Monitoring UI
"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .modern_ui_components import ModernStatusIndicator, ModernDataCard, ModernControlPanel
from .modern_style import ModernStyle

class UIEnhancer:
    """Enhances existing UI with modern components"""
    
    @staticmethod
    def add_status_panel_to_layout(layout, title="시스템 상태"):
        """Add a modern status panel to an existing layout"""
        status_frame = QFrame()
        status_frame.setObjectName("data_card")
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(16, 16, 16, 16)
        status_layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setProperty("class", "label")
        status_layout.addWidget(title_label)
        
        # Status indicators
        status_indicators = {
            'cnc': ModernStatusIndicator("CNC 시스템", "offline"),
            'laser': ModernStatusIndicator("레이저 시스템", "offline"),
            'camera': ModernStatusIndicator("카메라 시스템", "offline"),
            'pyrometer': ModernStatusIndicator("피로미터", "offline"),
            'ded_log': ModernStatusIndicator("DED 로그", "offline")
        }
        
        for indicator in status_indicators.values():
            status_layout.addWidget(indicator)
        
        status_layout.addStretch()
        
        # Apply styling
        ModernStyle.apply_modern_style(status_frame)
        
        # Add to layout
        layout.addWidget(status_frame)
        
        return status_indicators
    
    @staticmethod
    def add_data_cards_to_layout(layout, data_configs):
        """Add modern data cards to an existing layout
        
        Args:
            layout: QLayout to add cards to
            data_configs: List of dicts with 'title', 'value', 'unit', 'status' keys
        """
        cards = {}
        
        for config in data_configs:
            card = ModernDataCard(
                title=config.get('title', ''),
                value=config.get('value', ''),
                unit=config.get('unit', ''),
                status=config.get('status', 'normal')
            )
            layout.addWidget(card)
            cards[config.get('key', config['title'])] = card
        
        return cards
    
    @staticmethod
    def enhance_existing_buttons(ui):
        """Enhance existing buttons with modern styling"""
        button_mappings = {
            'Save_btn': 'primary_btn',
            'setting_btn': 'info_btn', 
            'Exit_btn': 'error_btn',
            'start_btn': 'start_btn',
            'stop_btn': 'stop_btn',
            'camera_btn': 'camera_btn'
        }
        
        for button_name, object_name in button_mappings.items():
            if hasattr(ui, button_name):
                button = getattr(ui, button_name)
                button.setObjectName(object_name)
                ModernStyle.apply_modern_style(button)
    
    @staticmethod
    def enhance_existing_frames(ui):
        """Enhance existing frames with modern styling"""
        frame_mappings = {
            'Control': 'Control',
            'Top': 'Top',
            'Main_frame': 'Main_frame'
        }
        
        for frame_name, object_name in frame_mappings.items():
            if hasattr(ui, frame_name):
                frame = getattr(ui, frame_name)
                frame.setObjectName(object_name)
                ModernStyle.apply_modern_style(frame)
    
    @staticmethod
    def create_modern_data_display(data_items, title="실시간 데이터"):
        """Create a modern data display widget"""
        container = QFrame()
        container.setObjectName("data_card")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Title
        title_label = QLabel(title)
        title_label.setProperty("class", "label")
        layout.addWidget(title_label)
        
        # Data grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        data_widgets = {}
        row = 0
        col = 0
        max_cols = 3
        
        for item in data_items:
            # Create label-value pair
            label = QLabel(item['label'])
            label.setProperty("class", "label")
            
            value = QLabel(item.get('value', 'N/A'))
            value.setProperty("class", "value")
            
            unit = QLabel(item.get('unit', ''))
            unit.setProperty("class", "unit")
            
            # Create horizontal layout for value and unit
            value_layout = QHBoxLayout()
            value_layout.addWidget(value)
            value_layout.addWidget(unit)
            value_layout.addStretch()
            
            # Add to grid
            grid_layout.addWidget(label, row, col * 2)
            grid_layout.addLayout(value_layout, row, col * 2 + 1)
            
            data_widgets[item['key']] = value
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)
        layout.addStretch()
        
        ModernStyle.apply_modern_style(container)
        
        return container, data_widgets
    
    @staticmethod
    def create_modern_control_panel(buttons_config, title="제어 패널"):
        """Create a modern control panel"""
        panel = ModernControlPanel(title)
        
        for config in buttons_config:
            panel.add_button(
                text=config['text'],
                button_type=config.get('type', 'primary'),
                callback=config.get('callback')
            )
        
        return panel
    
    @staticmethod
    def enhance_graph_widget(graph_widget, title=""):
        """Enhance an existing pyqtgraph widget with modern styling"""
        # Create container
        container = QFrame()
        container.setObjectName("graph_container")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "label")
            layout.addWidget(title_label)
        
        # Add graph widget
        layout.addWidget(graph_widget)
        
        ModernStyle.apply_modern_style(container)
        
        return container
    
    @staticmethod
    def enhance_image_display(image_label, title="카메라 이미지"):
        """Enhance an existing image label with modern styling"""
        container = QFrame()
        container.setObjectName("image_container")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setProperty("class", "label")
        layout.addWidget(title_label)
        
        # Image label
        image_label.setObjectName("image_label")
        image_label.setMinimumSize(320, 240)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
        # Status bar
        status_bar = QLabel()
        status_bar.setProperty("class", "unit")
        layout.addWidget(status_bar)
        
        ModernStyle.apply_modern_style(container)
        
        return container, status_bar

def enhance_ui_layout(layout, enhancement_type, **kwargs):
    """Convenience function to enhance UI layouts"""
    if enhancement_type == "status_panel":
        return UIEnhancer.add_status_panel_to_layout(layout, **kwargs)
    elif enhancement_type == "data_cards":
        return UIEnhancer.add_data_cards_to_layout(layout, **kwargs)
    elif enhancement_type == "data_display":
        return UIEnhancer.create_modern_data_display(**kwargs)
    elif enhancement_type == "control_panel":
        return UIEnhancer.create_modern_control_panel(**kwargs)
    else:
        raise ValueError(f"Unknown enhancement type: {enhancement_type}")
