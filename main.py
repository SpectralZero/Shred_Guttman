#!/usr/bin/env python3
"""
Advanced MODE FILE SHREDDER - PyQt6 Launcher
Advanced military-grade file destruction tool with modern GUI
"""

import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from shredder_gui_pyqt import AdvancedModeShredderWindow
"""
file is gone

The filename is gone

The metadata is gone

The content is destroyed

The recovered blocks are overwritten

Autopsy cannot reconstruct anything

No forensic recovery is possible
"""
def main():
    """Launch the Advanced Mode File Shredder with PyQt6 GUI"""
    print(" Starting Advanced MODE File Shredder (PyQt6)...")
    print(" Military-Grade Secure Data Destruction")
    print(" Use with extreme caution - data destruction is PERMANENT")
    
    # Set high DPI scaling for modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Advanced Mode File Shredder")
    app.setApplicationVersion("2.0.0")
    
    window = AdvancedModeShredderWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()