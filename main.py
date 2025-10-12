#!/usr/bin/env python3
import sys
import subprocess
import os
import shutil
import webbrowser
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu, 
                                QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QLineEdit, QPushButton, QSpinBox, QFileDialog, QMessageBox)
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QFont, QCursor
from PySide6.QtCore import Qt, QTimer, QUrl

class ConfigDialog(QDialog):
    def __init__(self, parent=None, current_dir="", current_interval=60):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Wallpaper directory selection
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Wallpaper Directory:")
        self.dir_input = QLineEdit(current_dir)
        self.dir_input.setReadOnly(True)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Rotation time input
        time_layout = QHBoxLayout()
        time_label = QLabel("Rotation Time (seconds):")
        self.time_input = QSpinBox()
        self.time_input.setMinimum(1)
        self.time_input.setMaximum(86400)  # Max 24 hours
        self.time_input.setValue(current_interval)
        self.time_input.setSuffix(" sec")
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)
        time_layout.addStretch()
        layout.addLayout(time_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Add spacing before branding
        layout.addStretch()
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Add fixed spacing before branding
        layout.addSpacing(0)
        
        # Branding/Version indicator
        branding_label = QLabel('<a href="https://ip.evenzero.in" style="color: palette(link); text-decoration: none;">inversepolarity v0.0.1</a>')
        branding_label.setAlignment(Qt.AlignRight)
        branding_label.setOpenExternalLinks(True)
        branding_label.setCursor(QCursor(Qt.PointingHandCursor))
        branding_label.setStyleSheet("QLabel { font-size: 10px; padding: 2px; }")
        layout.addWidget(branding_label)

        self.setLayout(layout)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Wallpaper Directory",
            self.dir_input.text() or str(Path.home())
        )
        if directory:
            self.dir_input.setText(directory)
    
    def validate_and_accept(self):
        # Validate directory
        directory = self.dir_input.text()
        if not directory:
            QMessageBox.warning(self, "Invalid Directory", "Please select a wallpaper directory.")
            return
        
        if not os.path.isdir(directory):
            QMessageBox.warning(self, "Invalid Directory", "The selected directory does not exist.")
            return
        
        # Check if directory contains any image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        has_images = False
        try:
            for item in Path(directory).rglob('*'):
                if item.is_file() and item.suffix.lower() in image_extensions:
                    has_images = True
                    break
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error reading directory: {e}")
            return
        
        if not has_images:
            QMessageBox.warning(self, "No Images Found", 
                              "No wallpaper images (.jpg, .jpeg, .png, .webp) found in the selected directory.")
            return
        
        # Validate rotation time (already validated by QSpinBox min/max)
        if self.time_input.value() < 1:
            QMessageBox.warning(self, "Invalid Time", "Rotation time must be at least 1 second.")
            return
        
        self.accept()
    
    def get_values(self):
        return self.dir_input.text(), self.time_input.value()


class TrayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("swwwcycle v0.0.1")
        self.is_paused = False
        
        # Default settings
        self.wallpaper_dir = str(Path.home() / "Pictures" / "wallpapers")
        self.rotation_interval = 60  # seconds
        
        # Create emoji icons
        self.active_icon = self.create_emoji_icon("♻️")
        self.paused_icon = self.create_emoji_icon("🧱")
        
        # Create tray icon
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.active_icon)
        
        # Create tray menu
        self.menu = QMenu()
        self.toggle_action = QAction("Pause", self)
        self.toggle_action.triggered.connect(self.toggle_state)
        
        change_now_action = QAction("Change Wallpaper Now", self)
        change_now_action.triggered.connect(self.change_wallpaper_now)
        
        config_action = QAction("Config", self)
        config_action.triggered.connect(self.open_config)
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        
        self.menu.addAction(self.toggle_action)
        self.menu.addAction(change_now_action)
        self.menu.addSeparator()
        self.menu.addAction(config_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)
        self.tray.setContextMenu(self.menu)
        
        # Click tray to toggle state
        self.tray.activated.connect(self.on_tray_click)
        self.tray.show()
        
        # Setup timer for wallpaper changing
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_wallpaper)
        self.timer.start(self.rotation_interval * 1000)
        
        # Change wallpaper immediately on start
        self.change_wallpaper()
    
    def create_emoji_icon(self, emoji):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setFont(QFont("Sans", 48))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, emoji)
        painter.end()
        
        return QIcon(pixmap)
    
    def open_config(self):
        dialog = ConfigDialog(None, self.wallpaper_dir, self.rotation_interval)
        if dialog.exec() == QDialog.Accepted:
            new_dir, new_interval = dialog.get_values()
            self.wallpaper_dir = new_dir
            self.rotation_interval = new_interval
            
            # Restart timer with new interval
            self.timer.stop()
            self.timer.start(self.rotation_interval * 1000)
            
            # Clear queue to use new directory
            queue_file = "/tmp/.wallpaper_queue"
            if os.path.exists(queue_file):
                os.remove(queue_file)
            
            # Change wallpaper immediately with new settings
            if not self.is_paused:
                self.change_wallpaper()
    
    def change_wallpaper_now(self):
        """Manually trigger wallpaper change, ignoring pause state"""
        self.change_wallpaper(force=True)
    
    def change_wallpaper(self, force=False):
        if self.is_paused and not force:
            return
        
        command = f'''
Q=/tmp/.wallpaper_queue; \
[ ! -s "$Q" ] && {{ find "{self.wallpaper_dir}" -type f -iname "*.jpg"; \
find "{self.wallpaper_dir}" -type f -iname "*.jpeg"; \
find "{self.wallpaper_dir}" -type f -iname "*.png"; \
find "{self.wallpaper_dir}" -type f -iname "*.webp"; }} | shuf > "$Q"; \
W=$(head -n1 "$Q"); tail -n +2 "$Q" > "$Q.tmp" && mv "$Q.tmp" "$Q"; \
swww img --transition-type fade --resize crop "$W"
'''
        
        try:
            subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error changing wallpaper: {e}")
    
    def toggle_state(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.tray.setIcon(self.paused_icon)
            self.toggle_action.setText("Resume")
        else:
            self.tray.setIcon(self.active_icon)
            self.toggle_action.setText("Pause")
        
    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_state()
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()


def check_swww():
    """Check if swww is available in the system"""
    if shutil.which("swww") is None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("swww Not Found")
        msg.setText("Error: swww is not installed or not in PATH")
        msg.setInformativeText("This application requires swww to function.\nPlease install swww and try again.")
        msg.exec()
        return False
    return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Enable system theme
    app.setStyle("Fusion")  # Use Fusion style which respects system colors
    
    # Check if swww is available
    if not check_swww():
        sys.exit(1)
    
    app.setQuitOnLastWindowClosed(False)
    window = TrayApp()
    window.hide()
    sys.exit(app.exec())