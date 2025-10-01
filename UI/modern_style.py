"""
Modern Professional UI Stylesheet for DED Monitoring Application
Dark Navy Theme with Professional Dashboard Styling
"""

class ModernStyle:
    # Color Palette - Dark Navy Professional Theme
    COLORS = {
        'primary': '#1e4976',           # Dark Navy Blue
        'primary_dark': '#0a1929',      # Very Dark Navy
        'primary_light': '#2d5a8a',     # Light Navy
        'secondary': '#ff6b35',         # Orange for alerts/warnings
        'secondary_dark': '#e65100',    # Dark Orange
        'success': '#4caf50',           # Green for success
        'warning': '#ff9800',           # Orange for warnings
        'error': '#f44336',             # Red for errors
        'info': '#2196f3',              # Info Blue
        
        # Dark Theme Colors
        'background': '#0a1929',        # Main Background - Dark Navy
        'surface': '#132f4c',           # Card Background - Medium Navy
        'surface_variant': '#1e4976',   # Elevated Surface - Light Navy
        'outline': '#2d5a8a',           # Border Color
        'outline_variant': '#3d6a9a',   # Lighter Border
        
        # Text Colors for Dark Theme
        'on_primary': '#ffffff',        # White text on primary
        'on_secondary': '#ffffff',      # White text on secondary
        'on_surface': '#ffffff',        # White text on surface
        'on_surface_variant': '#b0bec5', # Light gray text
        'on_background': '#ffffff',     # White text on background
        
        # Status Colors
        'status_online': '#4caf50',     # Online status - Green
        'status_offline': '#f44336',    # Offline status - Red
        'status_warning': '#ff9800',    # Warning status - Orange
        'status_processing': '#2196f3', # Processing status - Blue
    }
    
    @classmethod
    def get_stylesheet(cls):
        """Return the complete dark navy stylesheet"""
        return f"""
        /* Global Styles */
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['on_background']};
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 14px;
        }}
        
        QWidget {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['on_background']};
        }}
        
        /* Header Frame */
        QFrame#headerFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 {cls.COLORS['primary']}, 
                stop:1 {cls.COLORS['primary_dark']});
            border: none;
            border-radius: 0px;
            padding: 8px;
            margin: 0px;
        }}
        
        QFrame#headerFrame QLabel {{
            color: {cls.COLORS['on_primary']};
            font-weight: 500;
            font-size: 16px;
        }}
        
        /* Time Display */
        QDateTimeEdit#current_time {{
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: {cls.COLORS['on_primary']};
            font-weight: 600;
            font-size: 16px;
            padding: 8px 12px;
            selection-background-color: {cls.COLORS['primary_light']};
        }}
        
        QDateTimeEdit#current_time:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        
        /* Left Sidebar */
        QFrame#leftSidebar {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 10px;
        }}
        
        /* Position Section */
        QFrame#positionSection {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
        }}
        
        /* Status Section */
        QFrame#statusSection {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
        }}
        
        /* Operating Section */
        QFrame#operatingSection {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
        }}
        
        /* Dashboard Frame */
        QFrame#dashboardFrame {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 10px;
        }}
        
        /* Camera Frame */
        QFrame#cameraFrame {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
        }}
        
        /* Chart Frames */
        QFrame#meltpoolAreaFrame, QFrame#meltpoolTempFrame, QFrame#laserPowerFrame {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
        }}
        
        /* Footer Frame */
        QFrame#footerFrame {{
            background-color: {cls.COLORS['surface']};
            border-top: 2px solid {cls.COLORS['outline']};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            color: {cls.COLORS['on_surface']};
            border: 2px solid {cls.COLORS['outline']};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
            font-size: 12px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: {cls.COLORS['on_surface']};
        }}
        
        /* Labels */
        QLabel {{
            color: {cls.COLORS['on_surface']};
            font-weight: 500;
        }}
        
        QLabel[class="title"] {{
            color: {cls.COLORS['on_surface']};
            font-weight: 600;
            font-size: 14px;
            padding: 5px;
        }}
        
        QLabel[class="value"] {{
            color: {cls.COLORS['primary_light']};
            font-weight: 700;
            font-size: 16px;
            padding: 4px 0px;
            background-color: {cls.COLORS['primary_dark']};
            border-radius: 3px;
            padding: 5px;
        }}
        
        QLabel[class="unit"] {{
            color: {cls.COLORS['on_surface_variant']};
            font-weight: 400;
            font-size: 12px;
        }}
        
        /* Modern Buttons */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary']},
                stop:1 {cls.COLORS['primary_dark']});
            border: none;
            border-radius: 8px;
            color: {cls.COLORS['on_primary']};
            font-weight: 600;
            font-size: 14px;
            padding: 12px 24px;
            margin: 4px;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_light']},
                stop:1 {cls.COLORS['primary']});
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_dark']},
                stop:1 {cls.COLORS['primary']});
        }}
        
        QPushButton:disabled {{
            background-color: {cls.COLORS['outline']};
            color: {cls.COLORS['on_surface_variant']};
        }}
        
        /* Save Button */
        QPushButton#Save_btn {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['success']},
                stop:1 #388e3c);
        }}
        
        QPushButton#Save_btn:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #66bb6a,
                stop:1 {cls.COLORS['success']});
        }}
        
        /* Exit Button */
        QPushButton#Exit_btn {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['error']},
                stop:1 #d32f2f);
        }}
        
        QPushButton#Exit_btn:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ef5350,
                stop:1 {cls.COLORS['error']});
        }}
        
        /* Settings Button */
        QPushButton#setting_btn {{
            background-color: {cls.COLORS['primary_light']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 25px;
            padding: 5px;
        }}
        
        QPushButton#setting_btn:hover {{
            background-color: {cls.COLORS['outline']};
        }}
        
        QPushButton#setting_btn:pressed {{
            background-color: {cls.COLORS['primary_dark']};
        }}
        
        /* Status Indicators */
        QLabel[class="status_online"] {{
            color: {cls.COLORS['status_online']};
            font-weight: 600;
            background-color: rgba(76, 175, 80, 0.1);
            border: 1px solid {cls.COLORS['status_online']};
            border-radius: 5px;
            padding: 8px;
        }}
        
        QLabel[class="status_offline"] {{
            color: {cls.COLORS['status_offline']};
            font-weight: 600;
            background-color: rgba(244, 67, 54, 0.1);
            border: 1px solid {cls.COLORS['status_offline']};
            border-radius: 5px;
            padding: 8px;
        }}
        
        QLabel[class="status_warning"] {{
            color: {cls.COLORS['status_warning']};
            font-weight: 600;
            background-color: rgba(255, 152, 0, 0.1);
            border: 1px solid {cls.COLORS['status_warning']};
            border-radius: 5px;
            padding: 8px;
        }}
        
        QLabel[class="status_processing"] {{
            color: {cls.COLORS['status_processing']};
            font-weight: 600;
            background-color: rgba(33, 150, 243, 0.1);
            border: 1px solid {cls.COLORS['status_processing']};
            border-radius: 5px;
            padding: 8px;
        }}
        
        /* Graph Widgets */
        QFrame#graph_container {{
            background-color: {cls.COLORS['surface_variant']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 8px;
            margin: 8px;
            padding: 16px;
        }}
        
        /* Image Display */
        QLabel#img_label {{
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 5px;
            background-color: {cls.COLORS['primary_dark']};
            color: {cls.COLORS['on_surface_variant']};
        }}
        
        /* Checkbox */
        QCheckBox {{
            color: {cls.COLORS['on_surface']};
            spacing: 10px;
            font-weight: 500;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {cls.COLORS['outline']};
            border-radius: 3px;
            background-color: {cls.COLORS['surface_variant']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {cls.COLORS['error']};
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {cls.COLORS['surface_variant']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.COLORS['outline_variant']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.COLORS['primary_light']};
        }}
        
        /* Tool Tips */
        QToolTip {{
            background-color: {cls.COLORS['surface']};
            border: 1px solid {cls.COLORS['outline']};
            border-radius: 6px;
            color: {cls.COLORS['on_surface']};
            font-size: 12px;
            padding: 8px;
        }}
        """
    
    @classmethod
    def apply_modern_style(cls, widget):
        """Apply modern styling to a widget"""
        widget.setStyleSheet(cls.get_stylesheet())
        
        # Set modern font
        font = widget.font()
        font.setFamily('Segoe UI')
        font.setPointSize(10)
        widget.setFont(font)
    
    @classmethod
    def get_status_color(cls, status):
        """Get color for status indicators"""
        status_colors = {
            'online': cls.COLORS['status_online'],
            'offline': cls.COLORS['status_offline'],
            'warning': cls.COLORS['status_warning'],
            'processing': cls.COLORS['status_processing'],
            'error': cls.COLORS['error'],
            'success': cls.COLORS['success']
        }
        return status_colors.get(status.lower(), cls.COLORS['on_surface_variant'])
