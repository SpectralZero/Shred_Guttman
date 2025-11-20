"""
Advanced MODE FILE SHREDDER - Ultimate PyQt6 GUI
Maximum security interface with file preservation options
"""

import sys
import os
import platform
import threading
from pathlib import Path
from typing import Optional
from datetime import datetime
import secrets

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QCheckBox,
                            QProgressBar, QTextEdit, QGroupBox, QFileDialog, 
                            QMessageBox, QSplitter, QFrame, QComboBox, QApplication)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QTextCursor

from secure_delete import shred_file, shred_directory, get_available_methods, validate_shredding_path
from theme_manager import ThemeManager

class ShreddingThread(QThread):
    """Thread for performing shredding operations"""
    
    progress_updated = pyqtSignal(int, int, str, int)
    operation_completed = pyqtSignal(bool, str)
    
    def __init__(self, target_path: str, keep_file: bool, preserve_location: str = None):
        super().__init__()
        self.target_path = target_path
        self.keep_file = keep_file
        self.preserve_location = preserve_location
        self.stop_event = threading.Event()
        
    def stop(self):
        """Request thread to stop"""
        self.stop_event.set()
        
    def run(self):
        """Main shredding operation"""
        try:
            if os.path.isfile(self.target_path):
                # For single files with preserve location, we need to handle the move manually
                if self.keep_file and self.preserve_location:
                    success, message = self._shred_file_with_custom_location()
                else:
                    success, message = shred_file(
                        self.target_path,
                        keep_file=self.keep_file,
                        progress=self._progress_callback,
                        stop_event=self.stop_event
                    )
            else:
                success, message = shred_directory(
                    self.target_path,
                    keep_file=self.keep_file,
                    progress=self._progress_callback,
                    stop_event=self.stop_event
                )
            
            self.operation_completed.emit(success, message)
            
        except Exception as e:
            self.operation_completed.emit(False, f"Unexpected error: {str(e)}")
    
    def _shred_file_with_custom_location(self):
        """Shred file and move to custom location"""
        try:
            import shutil
            from pathlib import Path
            
            source_file = Path(self.target_path)
            preserve_dir = Path(self.preserve_location)
            
            # Ensure preserve directory exists
            preserve_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate secure random name for preserved file
            random_name = "AdvancedMODE_PRESERVED_" + secrets.token_hex(16) + source_file.suffix
            final_path = preserve_dir / random_name
            
            # First shred the file in its original location
            success, message = shred_file(
                self.target_path,
                keep_file=True,  # Keep the file after shredding
                progress=self._progress_callback,
                stop_event=self.stop_event
            )
            
            if success:
                # Find the shredded file (it will have a random name in the same directory)
                source_dir = source_file.parent
                shredded_files = list(source_dir.glob("AdvancedMODE_*"))
                
                if shredded_files:
                    # Move the last shredded file to the preserve location
                    shutil.move(str(shredded_files[-1]), str(final_path))
                    return True, f"File shredded and moved to: {final_path}"
                else:
                    return False, "Could not find shredded file for moving"
            else:
                return False, message
                
        except Exception as e:
            return False, f"Error during file preservation: {str(e)}"
    
    def _progress_callback(self, current: int, total: int, status: str, bytes_processed: int) -> bool:
        """Progress callback for shredding operations"""
        if self.stop_event.is_set():
            return False
        self.progress_updated.emit(current, total, status, bytes_processed)
        return True

class AdvancedModeShredderWindow(QMainWindow):
    """Main application window with ultimate security interface"""
    
    def __init__(self):
        super().__init__()
        self.shredding_methods = get_available_methods()
        self.current_operation: Optional[ShreddingThread] = None
        self.operation_count = 0
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Load settings
        self.settings = QSettings("AdvancedModeShredder", "Config")
        
        self.init_ui()
        self.apply_theme(self.settings.value("theme", "cyber_dark"))
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(" Advanced MODE FILE SHREDDER - ULTIMATE SECURITY DATA DESTRUCTION")
        self.setMinimumSize(1050, 760)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (controls)
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel (log only)
        right_panel = self.create_log_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([600, 400])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("🟢 READY - Advanced MODE SHREDDER ACTIVE - SELECT TARGET")
        
        # Load saved settings
        self.load_settings()
        
    def create_control_panel(self) -> QWidget:
        """Create the left control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Target selection
        target_group = self.create_target_section()
        layout.addWidget(target_group)
        
        # Configuration
        config_group = self.create_config_section()
        layout.addWidget(config_group)
        
        # Keep file options
        self.keep_file_group = self.create_keep_file_section()
        self.keep_file_group.setVisible(False)
        layout.addWidget(self.keep_file_group)
        
        # Progress section
        progress_group = self.create_progress_section()
        layout.addWidget(progress_group)
        
        # Control buttons
        button_group = self.create_button_section()
        layout.addWidget(button_group)
        
        layout.addStretch()
        
        return panel
    
    def create_header(self) -> QWidget:
        """Create the header section"""
        header = QWidget()
        layout = QVBoxLayout(header)
        
        # Main title
        title = QLabel(" Advanced MODE FILE SHREDDER")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00ff88;
            margin-bottom: 5px;
        """)
        
        # Subtitle
        subtitle = QLabel(" GUTMANN 35-PASS METHOD - MAXIMUM SECURITY DESTRUCTION")
        subtitle.setStyleSheet("""
            font-size: 12px;
            color: #00ff88;
            margin-bottom: 10px;
        """)
        
        # Security info
        method_info = self.shredding_methods["gutmann_35_pass"]
        security_label = QLabel(f" {method_info['security']} SECURITY |  {method_info['passes']} PASSES |  AUTO-METADATA OBFUSCATION")
        security_label.setStyleSheet("""
            font-size: 10px;
            color: #00ff88;
            background-color: #003300;
            padding: 5px;
            border-radius: 3px;
            font-weight: bold;
        """)
        
        # Theme selector
        theme_widget = QWidget()
        theme_layout = QHBoxLayout(theme_widget)
        theme_layout.addWidget(QLabel("Theme:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.get_available_themes())
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        theme_layout.addWidget(self.theme_combo)
        
        theme_layout.addStretch()
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(security_label)
        layout.addWidget(theme_widget)
        
        return header
    
    def create_target_section(self) -> QGroupBox:
        """Create target selection section"""
        group = QGroupBox(" TARGET SELECTION")
        layout = QVBoxLayout(group)
        
        # Path input
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Target Path:"))
        
        self.path_edit = QLineEdit()
        self.path_edit.textChanged.connect(self.validate_path)
        self.path_edit.setPlaceholderText("Select file or folder for ULTIMATE destruction...")
        path_layout.addWidget(self.path_edit)
        
        # Browse buttons
        browse_layout = QVBoxLayout()
        self.browse_file_btn = QPushButton("📁 Browse File")
        self.browse_file_btn.clicked.connect(self.browse_file)
        browse_layout.addWidget(self.browse_file_btn)
        
        self.browse_folder_btn = QPushButton("📂 Browse Folder")
        self.browse_folder_btn.clicked.connect(self.browse_folder)
        browse_layout.addWidget(self.browse_folder_btn)
        
        path_layout.addLayout(browse_layout)
        layout.addLayout(path_layout)
        
        # Validation label
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet("color: #00ff88; font-size: 10px; font-weight: bold;")
        layout.addWidget(self.validation_label)
        
        return group
    
    def create_config_section(self) -> QGroupBox:
        """Create configuration section"""
        group = QGroupBox("⚙️ ULTIMATE SHREDDING CONFIGURATION")
        layout = QVBoxLayout(group)
        
        # Security info
        method_info = self.shredding_methods["gutmann_35_pass"]
        method_label = QLabel(f"🔄 {method_info['passes']} PASS GUTMANN METHOD | 🔒 {method_info['security']} SECURITY")
        method_label.setStyleSheet("color: #00ff88; font-size: 12px; font-weight: bold;")
        layout.addWidget(method_label)
        
        # Keep file option
        self.keep_file_check = QCheckBox("💾 Preserve file after shredding (for verification)")
        self.keep_file_check.stateChanged.connect(self.on_keep_file_changed)
        layout.addWidget(self.keep_file_check)
        
        info_label = QLabel(
            " FILE WILL BE: Overwritten 35 times with random data + Auto-renamed + Timestamps obfuscated\n"
            " DESTRUCTION: File completely destroyed and irrecoverable\n"
            " PRESERVATION: File preserved with obfuscated name and metadata"
        )
        info_label.setStyleSheet("color: #888888; font-size: 9px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        return group
    
    def create_keep_file_section(self) -> QGroupBox:
        """Create keep file options section"""
        group = QGroupBox("💾 FILE PRESERVATION LOCATION")
        layout = QVBoxLayout(group)
        
        # Location selection
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Preserve Location:"))
        
        self.preserve_location_edit = QLineEdit()
        self.preserve_location_edit.setPlaceholderText("Optional: Select location for preserved file...")
        location_layout.addWidget(self.preserve_location_edit)
        
        self.browse_preserve_btn = QPushButton("📁 Browse")
        self.browse_preserve_btn.clicked.connect(self.browse_preserve_location)
        location_layout.addWidget(self.browse_preserve_btn)
        
        layout.addLayout(location_layout)
        
        info_label = QLabel(
            "If no location specified, file will be preserved in original directory with obfuscated name.\n"
            "File will be automatically renamed and timestamps obfuscated for maximum security."
        )
        info_label.setStyleSheet("color: #888888; font-size: 9px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        return group
    
    def create_progress_section(self) -> QGroupBox:
        """Create progress monitoring section"""
        group = QGroupBox(" Advanced MODE PROGRESS")
        layout = QVBoxLayout(group)
        
        # Overall progress
        layout.addWidget(QLabel("Overall Progress:"))
        self.overall_progress = QProgressBar()
        self.overall_progress.setMinimum(0)
        self.overall_progress.setMaximum(100)
        layout.addWidget(self.overall_progress)
        
        self.overall_label = QLabel("🟢 READY FOR ULTIMATE DESTRUCTION")
        self.overall_label.setStyleSheet("font-size: 10px; color: #00ff88;")
        layout.addWidget(self.overall_label)
        
        # Current operation progress
        layout.addWidget(QLabel("Current Operation:"))
        self.current_progress = QProgressBar()
        self.current_progress.setMinimum(0)
        self.current_progress.setMaximum(100)
        layout.addWidget(self.current_progress)
        
        self.current_label = QLabel("Waiting for Advanced MODE engagement...")
        self.current_label.setStyleSheet("font-size: 10px; color: #888888;")
        layout.addWidget(self.current_label)
        
        return group
    
    def create_button_section(self) -> QWidget:
        """Create control buttons section"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Start button
        self.start_btn = QPushButton(" ENGAGE Advanced MODE SHREDDING")
        self.start_btn.clicked.connect(self.start_shredding)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff88;
                color: #000000;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00cc66;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        layout.addWidget(self.start_btn)
        
        # Stop button
        self.stop_btn = QPushButton("⏹️ ABORT OPERATION")
        self.stop_btn.clicked.connect(self.stop_shredding)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffaa00;
                color: #000000;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc8800;
            }
        """)
        layout.addWidget(self.stop_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_log_panel(self) -> QWidget:
        """Create the log display panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Log header
        log_header = QLabel("📝 Advanced MODE OPERATION LOG")
        log_header.setStyleSheet("font-size: 14pt; font-weight: bold; color: #00ff88; margin-bottom: 10px;")
        layout.addWidget(log_header)
        
        # Log controls
        controls = QHBoxLayout()
        
        self.clear_log_btn = QPushButton("🧹 Clear Log")
        self.clear_log_btn.clicked.connect(self.clear_log)
        controls.addWidget(self.clear_log_btn)
        
        self.export_log_btn = QPushButton("📤 Export Log")
        self.export_log_btn.clicked.connect(self.export_log)
        controls.addWidget(self.export_log_btn)
        
        controls.addStretch()
        
        # Operation counter
        self.op_counter_label = QLabel("Operations: 0")
        self.op_counter_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        controls.addWidget(self.op_counter_label)
        
        layout.addLayout(controls)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff88;
                font-family: 'Consolas', monospace;
                font-size: 10px;
                border: 2px solid #333333;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        return panel
    
    def apply_theme(self, theme_name: str):
        """Apply the selected theme"""
        self.theme_manager.apply_theme(theme_name, QApplication.instance())
        index = self.theme_combo.findText(theme_name)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        self.settings.setValue("theme", theme_name)
        
    def validate_path(self):
        """Validate the selected path"""
        path = self.path_edit.text().strip()
        if not path:
            self.validation_label.setText("")
            self.start_btn.setEnabled(False)
            return
            
        is_valid, message = validate_shredding_path(path)
        
        if is_valid:
            self.validation_label.setText(f"✅ {message}")
            self.validation_label.setStyleSheet("color: #00ff88; font-size: 10px; font-weight: bold;")
            self.start_btn.setEnabled(True)
        else:
            self.validation_label.setText(f"❌ {message}")
            self.validation_label.setStyleSheet("color: #ff4444; font-size: 10px; font-weight: bold;")
            self.start_btn.setEnabled(False)
    
    def browse_file(self):
        """Browse for file to shred"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select file for ULTIMATE destruction",
            "",
            "All files (*.*)"
        )
        if filename:
            self.path_edit.setText(filename)
    
    def browse_folder(self):
        """Browse for folder to shred"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder for ULTIMATE destruction"
        )
        if folder:
            self.path_edit.setText(folder)
    
    def browse_preserve_location(self):
        """Browse for location to preserve file"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select location for preserved file"
        )
        if folder:
            self.preserve_location_edit.setText(folder)
    
    def on_keep_file_changed(self, state):
        """Handle keep file option change"""
        self.keep_file_group.setVisible(state == Qt.CheckState.Checked.value)
        
        if state:
            self.log(" FILE PRESERVATION MODE ENABLED")
            self.log(" Files will be: Overwritten 35x + Auto-renamed + Timestamps obfuscated")
        else:
            self.log(" ULTIMATE DESTRUCTION MODE - Files will be PERMANENTLY DESTROYED")
    
    def start_shredding(self):
        """Start the shredding operation"""
        path = self.path_edit.text().strip()
        if not path:
            QMessageBox.critical(self, "❌ ERROR", "Please select a file or folder for destruction")
            return
            
        is_valid, message = validate_shredding_path(path)
        if not is_valid:
            QMessageBox.critical(self, "❌ SECURITY ERROR", f"Invalid path: {message}")
            return
        
        # ULTIMATE SECURITY CONFIRMATION
        if not self.keep_file_check.isChecked():
            target_type = "file" if os.path.isfile(path) else "folder and ALL its contents"
            reply = QMessageBox.critical(
                self,
                " FINAL ULTIMATE CONFIRMATION",
                f" ULTIMATE SECURITY WARNING \n\n"
                f"This action will PERMANENTLY DESTROY the {target_type}:\n\n"
                f" {path}\n\n"
                f" SECURITY: GUTMANN 35-PASS METHOD\n"
                f" PROCESS: 35 overwrites + Auto-rename + Timestamp obfuscation\n\n"
                f"❌ THIS ACTION IS COMPLETELY IRRECOVERABLE\n"
                f"❌ NO DATA CAN BE RESTORED AFTER THIS OPERATION\n\n"
                f"ARE YOU ABSOLUTELY CERTAIN?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                self.log(" Operation cancelled by user - ultimate destruction averted")
                return
        else:
            # For keep file mode
            preserve_location = self.preserve_location_edit.text().strip()
            if preserve_location:
                QMessageBox.information(
                    self,
                    "💾 File Preservation Mode",
                    f"FILE PRESERVATION MODE IS ENABLED.\n\n"
                    f"Files will be:\n"
                    f"• Overwritten 35 times with random data\n"
                    f"• Automatically renamed\n" 
                    f"• Timestamps obfuscated\n"
                    f"• Moved to: {preserve_location}\n\n"
                    f"Original files will be securely destroyed."
                )
            else:
                QMessageBox.information(
                    self,
                    "💾 File Preservation Mode",
                    "FILE PRESERVATION MODE IS ENABLED.\n\n"
                    "Files will be:\n"
                    "• Overwritten 35 times with random data\n"
                    "• Automatically renamed\n"
                    "• Timestamps obfuscated\n"
                    "• Preserved in original location with obfuscated names"
                )
        
        # Start shredding thread
        preserve_location = self.preserve_location_edit.text().strip() if self.keep_file_check.isChecked() else None
        self.current_operation = ShreddingThread(
            path,
            self.keep_file_check.isChecked(),
            preserve_location
        )
        
        self.current_operation.progress_updated.connect(self.update_progress)
        self.current_operation.operation_completed.connect(self.on_operation_complete)
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.overall_progress.setValue(0)
        self.current_progress.setValue(0)
        
        self.operation_count += 1
        self.op_counter_label.setText(f"Operations: {self.operation_count}")
        
        self.log(f" STARTING Advanced MODE OPERATION #{self.operation_count}")
        self.log(f" TARGET: {path}")
        self.log(f" METHOD: GUTMANN 35-PASS - MAXIMUM SECURITY")
        self.log(f" PRESERVE: {'YES' if self.keep_file_check.isChecked() else 'NO'}")
        if preserve_location:
            self.log(f"📦 LOCATION: {preserve_location}")
        
        self.current_operation.start()
    
    def stop_shredding(self):
        """Stop the current shredding operation"""
        if self.current_operation and self.current_operation.isRunning():
            self.current_operation.stop()
            self.stop_btn.setEnabled(False)
            self.statusBar().showMessage("🟡 Stopping operation...")
            self.log("⏹️ OPERATION CANCELLATION REQUESTED...")
    
    def update_progress(self, current: int, total: int, status: str, bytes_processed: int):
        """Update progress displays"""
        # Overall progress
        if total > 0:
            progress_percent = (current / total) * 100
            self.overall_progress.setValue(int(progress_percent))
            self.overall_label.setText(f"Overall: {current}/{total} ({progress_percent:.1f}%) - {status}")
        
        # Current operation progress
        if bytes_processed > 0:
            size_mb = bytes_processed / (1024 * 1024)
            progress_percent = min(int((bytes_processed / (1024 * 1024))), 100)
            self.current_progress.setValue(progress_percent)
            self.current_label.setText(f"Current: {size_mb:.1f} MB processed - {status}")
        else:
            self.current_label.setText(f"Current: {status}")
            
        self.statusBar().showMessage(f"Advanced MODE ACTIVE: {status}")
    
    def on_operation_complete(self, success: bool, message: str):
        """Handle operation completion"""
        # Reset UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.overall_progress.setValue(0)
        self.current_progress.setValue(0)
        
        if success:
            self.overall_label.setText("✅ Advanced MODE OPERATION COMPLETED SUCCESSFULLY")
            self.current_label.setText("🟢 Ready for next operation")
            self.statusBar().showMessage("✅ Advanced MODE OPERATION COMPLETED")
            self.log(f"✅ SUCCESS: {message}")
            
            if self.keep_file_check.isChecked():
                QMessageBox.information(
                    self,
                    "✅ Operation Complete",
                    f"Advanced MODE OVERWRITE COMPLETED:\n{message}\n\n"
                    f"Files have been securely overwritten and preserved with obfuscated metadata."
                )
            else:
                QMessageBox.information(
                    self,
                    "☠️ Destruction Complete", 
                    f"ULTIMATE DESTRUCTION SUCCESSFUL:\n{message}\n\n"
                    f"All data has been permanently destroyed and is irrecoverable."
                )
        else:
            self.overall_label.setText("❌ Advanced MODE OPERATION FAILED")
            self.current_label.setText("🔴 Check log for details")
            self.statusBar().showMessage("❌ OPERATION FAILED")
            self.log(f"❌ FAILED: {message}")
            if "cancelled" not in message.lower():
                QMessageBox.critical(self, "❌ Advanced Mode Error", f"OPERATION FAILED:\n{message}")
    
    def log(self, message: str):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # Auto-scroll to bottom
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.clear()
        self.log("🧹 LOG CLEARED - Advanced MODE SHREDDER ACTIVE")
    
    def export_log(self):
        """Export log to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Advanced Mode Log",
            f"Advanced_mode_shredder_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text files (*.txt);;All files (*.*)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                self.log(f"📤 Advanced MODE LOG EXPORTED TO: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "❌ Export Error", f"Failed to export log: {e}")
    
    def load_settings(self):
        """Load saved settings"""
        saved_theme = self.settings.value("theme", "cyber_dark")
        self.apply_theme(saved_theme)
        
        self.keep_file_check.setChecked(self.settings.value("keep_file", False, type=bool))
    
    def closeEvent(self, event):
        """Handle application close"""
        if self.current_operation and self.current_operation.isRunning():
            reply = QMessageBox.question(
                self,
                "Quit Advanced Mode Shredder",
                "Advanced MODE operation in progress. Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_operation.stop()
                self.current_operation.wait(2000)
                event.accept()
            else:
                event.ignore()
        else:
            # Save settings
            self.settings.setValue("keep_file", self.keep_file_check.isChecked())
            event.accept()