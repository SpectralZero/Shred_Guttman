"""
Advanced MODE SHREDDER - Advanced PyQt6 Theme Manager
Professional theme system with QSS stylesheets
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class ThemeManager:
    """Advanced theme management for PyQt6 application"""
    
    THEMES = {
        "cyber_dark": {
            "name": "Cyber Dark",
            "type": "dark",
            "colors": {
                "primary": "#00ff88",
                "secondary": "#0088ff",
                "accent": "#ff0088",
                "background": "#0a0a0a",
                "surface": "#1a1a1a",
                "surface_variant": "#2a2a2a",
                "text_primary": "#ffffff",
                "text_secondary": "#cccccc",
                "text_accent": "#00ff88",
                "error": "#ff4444",
                "warning": "#ffaa00",
                "success": "#00ff88",
                "border": "#333333",
                "button_bg": "#2a2a2a",
                "button_hover": "#3a3a3a",
                "entry_bg": "#1a1a1a",
                "entry_fg": "#ffffff",
                "entry_border": "#444444",
                "disabled": "#555555"
            }
        },
        
        "midnight_blue": {
            "name": "Midnight Blue",
            "type": "dark",
            "colors": {
                "primary": "#4fc3f7",
                "secondary": "#29b6f6",
                "accent": "#ff6e40",
                "background": "#0d1b2a",
                "surface": "#1b263b",
                "surface_variant": "#2d3e57",
                "text_primary": "#e0e1dd",
                "text_secondary": "#b8c2cc",
                "text_accent": "#ff6e40",
                "error": "#ff5252",
                "warning": "#ffb74d",
                "success": "#69f0ae",
                "border": "#37474f",
                "button_bg": "#2d3e57",
                "button_hover": "#3a4d6b",
                "entry_bg": "#1b263b",
                "entry_fg": "#e0e1dd",
                "entry_border": "#3a4d6b",
                "disabled": "#4a5a72"
            }
        },
        
        "military_green": {
            "name": "Military Green",
            "type": "dark",
            "colors": {
                "primary": "#689f38",
                "secondary": "#388e3c",
                "accent": "#ff5722",
                "background": "#1a1f1a",
                "surface": "#2d332d",
                "surface_variant": "#3e443e",
                "text_primary": "#e8f5e8",
                "text_secondary": "#b8c8b8",
                "text_accent": "#ff5722",
                "error": "#f44336",
                "warning": "#ff9800",
                "success": "#4caf50",
                "border": "#2e342e",
                "button_bg": "#3e443e",
                "button_hover": "#4a504a",
                "entry_bg": "#2d332d",
                "entry_fg": "#e8f5e8",
                "entry_border": "#4a504a",
                "disabled": "#5a605a"
            }
        },
        
        "matrix_green": {
            "name": "Matrix Green",
            "type": "dark",
            "colors": {
                "primary": "#00ff41",
                "secondary": "#008f11",
                "accent": "#00ff88",
                "background": "#001100",
                "surface": "#002200",
                "surface_variant": "#003300",
                "text_primary": "#00ff41",
                "text_secondary": "#00cc33",
                "text_accent": "#00ff88",
                "error": "#ff0044",
                "warning": "#ffff00",
                "success": "#00ff41",
                "border": "#004400",
                "button_bg": "#003300",
                "button_hover": "#004400",
                "entry_bg": "#002200",
                "entry_fg": "#00ff41",
                "entry_border": "#005500",
                "disabled": "#005500"
            }
        },
        
        "professional_light": {
            "name": "Professional Light",
            "type": "light",
            "colors": {
                "primary": "#1976d2",
                "secondary": "#424242",
                "accent": "#ff4081",
                "background": "#f8f9fa",
                "surface": "#ffffff",
                "surface_variant": "#e9ecef",
                "text_primary": "#212121",
                "text_secondary": "#666666",
                "text_accent": "#1976d2",
                "error": "#d32f2f",
                "warning": "#f57c00",
                "success": "#388e3c",
                "border": "#dee2e6",
                "button_bg": "#e9ecef",
                "button_hover": "#dee2e6",
                "entry_bg": "#ffffff",
                "entry_fg": "#212121",
                "entry_border": "#ced4da",
                "disabled": "#adb5bd"
            }
        }
    }
    
    def __init__(self):
        self.current_theme = "cyber_dark"
        self.current_colors = self.THEMES[self.current_theme]["colors"]
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.THEMES.keys())
    
    def apply_theme(self, theme_name: str, app: QApplication):
        """Apply complete theme to the application"""
        if theme_name not in self.THEMES:
            theme_name = "cyber_dark"
            
        self.current_theme = theme_name
        self.current_colors = self.THEMES[theme_name]["colors"]
        
        # Apply QSS stylesheet
        stylesheet = self._generate_stylesheet()
        app.setStyleSheet(stylesheet)
        
        # Apply palette for native widgets
        self._apply_palette(app)
    
    def _generate_stylesheet(self) -> str:
        """Generate complete QSS stylesheet for the theme"""
        c = self.current_colors
        
        return f"""
            /* Main Application Styles */
            QMainWindow {{
                background-color: {c['background']};
                color: {c['text_primary']};
            }}
            
            QWidget {{
                background-color: {c['background']};
                color: {c['text_primary']};
                font-family: "Segoe UI", "Arial", sans-serif;
            }}
            
            /* Group Boxes */
            QGroupBox {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: 2px solid {c['border']};
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: {c['surface']};
                color: {c['text_accent']};
            }}
            
            /* Labels */
            QLabel {{
                background-color: transparent;
                color: {c['text_primary']};
            }}
            
            QLabel[cssClass="accent"] {{
                color: {c['text_accent']};
                font-weight: bold;
            }}
            
            QLabel[cssClass="success"] {{
                color: {c['success']};
            }}
            
            QLabel[cssClass="error"] {{
                color: {c['error']};
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {c['button_bg']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }}
            
            QPushButton:hover {{
                background-color: {c['button_hover']};
                border: 1px solid {c['primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {c['primary']};
                color: {c['background']};
            }}
            
            QPushButton:disabled {{
                background-color: {c['disabled']};
                color: {c['text_secondary']};
                border: 1px solid {c['border']};
            }}
            
            QPushButton[cssClass="primary"] {{
                background-color: {c['primary']};
                color: {c['background']};
                font-weight: bold;
            }}
            
            QPushButton[cssClass="primary"]:hover {{
                background-color: {c['secondary']};
            }}
            
            QPushButton[cssClass="danger"] {{
                background-color: {c['error']};
                color: white;
            }}
            
            /* Line Edits */
            QLineEdit {{
                background-color: {c['entry_bg']};
                color: {c['entry_fg']};
                border: 1px solid {c['entry_border']};
                border-radius: 4px;
                padding: 6px 8px;
                selection-background-color: {c['primary']};
            }}
            
            QLineEdit:focus {{
                border: 1px solid {c['primary']};
            }}
            
            QLineEdit:disabled {{
                background-color: {c['disabled']};
                color: {c['text_secondary']};
            }}
            
            /* Combo Boxes */
            QComboBox {{
                background-color: {c['entry_bg']};
                color: {c['entry_fg']};
                border: 1px solid {c['entry_border']};
                border-radius: 4px;
                padding: 6px 8px;
                min-width: 120px;
            }}
            
            QComboBox:hover {{
                border: 1px solid {c['primary']};
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid {c['border']};
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {c['text_primary']};
                width: 0px;
                height: 0px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
                selection-background-color: {c['primary']};
            }}
            
            /* Checkboxes */
            QCheckBox {{
                background-color: transparent;
                color: {c['text_primary']};
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {c['border']};
                border-radius: 3px;
                background-color: {c['entry_bg']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {c['primary']};
                border: 1px solid {c['primary']};
            }}
            
            QCheckBox::indicator:disabled {{
                background-color: {c['disabled']};
                border: 1px solid {c['border']};
            }}
            
            /* Progress Bars */
            QProgressBar {{
                background-color: {c['surface_variant']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
                border-radius: 4px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {c['primary']};
                border-radius: 3px;
            }}
            
            /* Text Edit */
            QTextEdit {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
                border-radius: 4px;
                padding: 4px;
                selection-background-color: {c['primary']};
            }}
            
            QTextEdit:focus {{
                border: 1px solid {c['primary']};
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: {c['surface_variant']};
                width: 15px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {c['button_bg']};
                border-radius: 7px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {c['button_hover']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Tab Widget */
            QTabWidget::pane {{
                background-color: {c['surface']};
                border: 1px solid {c['border']};
                border-radius: 4px;
            }}
            
            QTabBar::tab {{
                background-color: {c['surface_variant']};
                color: {c['text_secondary']};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border-bottom: 2px solid {c['primary']};
            }}
            
            QTabBar::tab:hover:!selected {{
                background-color: {c['button_hover']};
                color: {c['text_primary']};
            }}
            
            /* Splitter */
            QSplitter::handle {{
                background-color: {c['border']};
                margin: 2px;
            }}
            
            QSplitter::handle:hover {{
                background-color: {c['primary']};
            }}
            
            /* Status Bar */
            QStatusBar {{
                background-color: {c['surface']};
                color: {c['text_primary']};
                border-top: 1px solid {c['border']};
            }}
        """
    
    def _apply_palette(self, app: QApplication):
        """Apply color palette for native widgets"""
        palette = QPalette()
        c = self.current_colors
        
        # Set palette colors based on theme type
        if self.THEMES[self.current_theme]["type"] == "dark":
            palette.setColor(QPalette.ColorRole.Window, QColor(c['background']))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Base, QColor(c['surface']))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c['surface_variant']))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(c['surface']))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Text, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Button, QColor(c['button_bg']))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(c['text_accent']))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(c['primary']))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(c['background']))
        else:
            # Light theme palette
            palette.setColor(QPalette.ColorRole.Window, QColor(c['background']))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Base, QColor(c['surface']))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c['surface_variant']))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(c['surface']))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Text, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.Button, QColor(c['button_bg']))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(c['text_primary']))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(c['text_accent']))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(c['primary']))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(c['surface']))
        
        app.setPalette(palette)
    
    
    def get_color(self, color_name: str) -> str:
        """Get color by name from current theme"""
        return self.current_colors.get(color_name, "#000000")