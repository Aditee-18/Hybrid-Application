import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QDialog)
from PyQt5.QtCore import Qt
from api_client import ChemAPIClient

#History Popup Window 
class HistoryDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.resize(800, 500)
        layout = QVBoxLayout(self)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Filename", "Avg Temp", "Avg Pressure", "Date"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        table.setRowCount(len(data))
        for row, rec in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(rec['filename'])))
            table.setItem(row, 1, QTableWidgetItem(f"{round(rec['avg_temp'], 2)}°C"))
            table.setItem(row, 2, QTableWidgetItem(f"{round(rec['avg_pressure'], 2)} bar"))
            table.setItem(row, 3, QTableWidgetItem(rec['uploaded_at'][:10]))
            
        layout.addWidget(table)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

#The Chart Widget 
class MktChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.fig.patch.set_facecolor('#f3f4f6')
        super().__init__(self.fig)

    def plot_data(self, summary):
        self.ax1.clear()
        self.ax2.clear()
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        self.ax1.pie(summary['type_dist'].values(), labels=summary['type_dist'].keys(), autopct='%1.1f%%', colors=colors)
        self.ax1.set_title("Equipment Types", fontweight='bold')
        self.ax2.bar(['Pressure', 'Temp', 'Flow'], [summary['avg_pressure'], summary['avg_temp'], summary['avg_flow']], color='#3b82f6')
        self.ax2.set_title("Process Averages", fontweight='bold')
        self.fig.tight_layout()
        self.draw()

#Main Dashboard
class ChemApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = ChemAPIClient()
        self.current_record_id = None
        self.setWindowTitle("Chemical Visualizer")
        self.resize(1200, 900)
        self.apply_styles()
        self.show_login_screen()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f3f4f6; }
            QLineEdit { padding: 12px; border: 2px solid #e2e8f0; border-radius: 8px; margin-bottom: 10px; }
            QPushButton { background-color: #2563eb; color: white; padding: 10px 18px; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #1d4ed8; }
            QPushButton#history_btn { background-color: #64748b; }
            QTableWidget { background-color: white; border: 1px solid #cbd5e1; gridline-color: #f1f5f9; }
            QHeaderView::section { background-color: #f8fafc; font-weight: bold; padding: 8px; border: none; border-bottom: 1px solid #cbd5e1; }
        """)

    def show_login_screen(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignCenter)
        self.user_input = QLineEdit(); self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit(); self.pass_input.setPlaceholderText("Password"); self.pass_input.setEchoMode(QLineEdit.Password)
        btn = QPushButton("Enter System"); btn.clicked.connect(self.handle_login)
        layout.addWidget(QLabel("<h2>Chemical Visualizer Login</h2>"))
        layout.addWidget(self.user_input); layout.addWidget(self.pass_input); layout.addWidget(btn)

    def show_dashboard(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Header with Buttons
        top_bar = QHBoxLayout()
        self.pdf_btn = QPushButton("Download PDF"); self.pdf_btn.setEnabled(False); self.pdf_btn.clicked.connect(self.handle_pdf)
        hist_btn = QPushButton("View History"); hist_btn.setObjectName("history_btn"); hist_btn.clicked.connect(self.open_history)
        up_btn = QPushButton("Upload CSV"); up_btn.clicked.connect(self.handle_upload)

        top_bar.addWidget(QLabel("<h1>System Dashboard</h1>"))
        top_bar.addStretch()
        top_bar.addWidget(hist_btn); top_bar.addWidget(self.pdf_btn); top_bar.addWidget(up_btn)
        main_layout.addLayout(top_bar)

        # Active Visualization
        self.canvas = MktChartCanvas(self)
        main_layout.addWidget(self.canvas)

        # Detailed Inventory
        main_layout.addWidget(QLabel("<h3>Active Dataset: Detailed Inventory</h3>"))
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(["Name", "Type", "Flowrate", "Pressure", "Temp"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.inventory_table)

    def handle_login(self):
        if self.api.login(self.user_input.text(), self.pass_input.text()): self.show_dashboard()
        else: QMessageBox.warning(self, "Error", "Invalid credentials")

    def open_history(self):
        history_data = self.api.get_history()
        dialog = HistoryDialog(history_data, self)
        dialog.exec_()

    def handle_upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if path:
            res = self.api.upload_csv(path)
            self.current_record_id = res['id']
            self.pdf_btn.setEnabled(True)
            self.canvas.plot_data(res['summary'])
            
            # Filling the Inventory Table
            rows = res['raw_data']
            self.inventory_table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                self.inventory_table.setItem(i, 0, QTableWidgetItem(str(row.get('Equipment Name', row.get('name', 'N/A')))))
                self.inventory_table.setItem(i, 1, QTableWidgetItem(str(row.get('Type', 'N/A'))))
                self.inventory_table.setItem(i, 2, QTableWidgetItem(str(row.get('Flowrate', '0'))))
                self.inventory_table.setItem(i, 3, QTableWidgetItem(str(row.get('Pressure', '0'))))
                self.inventory_table.setItem(i, 4, QTableWidgetItem(str(row.get('Temperature', '0'))))
            
            QMessageBox.information(self, "Done", "Analytics updated successfully.")

    def handle_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"Report_{self.current_record_id}.pdf", "PDF (*.pdf)")
        if save_path:
            content = self.api.download_pdf(self.current_record_id)
            if content:
                with open(save_path, 'wb') as f: f.write(content)
                QMessageBox.information(self, "Success", "PDF Saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv); win = ChemApp(); win.show(); sys.exit(app.exec_())