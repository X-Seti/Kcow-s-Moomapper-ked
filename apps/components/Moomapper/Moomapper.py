#!/usr/bin/env python3
#belongs in apps/components/Moomapper/Moomapper.py -Version: 5
# X-Seti-2026-08-01

import sys
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QSplitter, QOpenGLWidget
)

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QListWidget
from PyQt5.QtWidgets import QPushButton, QInputDialog

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False

try:
    from apps.utils.app_settings_system import AppSettings
    from apps.utils.App_System_Setting_Svg_icons import apply_theme_to_app
except ImportError:
    class AppSettings:
        def get_stylesheet(self): return ""
    def apply_theme_to_app(app, settings): pass

from apps.components.Moomapper.depends.icon_provider import MoomapperIconProvider
from apps.components.Moomapper.depends.gta_img import GTAImg
from apps.components.Moomapper.depends.gta_dff import GTADff
from apps.components.Moomapper.depends.gta_txd import GTATxd
from apps.components.Moomapper.depends.game_profiles import GameProfile, GameProfileManager


class MoomapperGLWidget(QOpenGLWidget):
    def __init__(self, parent=None): #vers 1
        super().__init__(parent)
        self.current_dff = None
        self.current_txd = None
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.zoom = -5.0
        self.last_pos = None
        self.texture_cache = {}


    def initializeGL(self): #vers 1
        if not OPENGL_AVAILABLE:
            return
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_TEXTURE_2D)


    def mouseMoveEvent(self, event): #vers 1
        if self.last_pos:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5
            self.last_pos = event.pos()
            self.update()


    def mousePressEvent(self, event): #vers 1
        self.last_pos = event.pos()


    def paintGL(self): #vers 1
        if not OPENGL_AVAILABLE:
            return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(self.rotation_x, 1.0, 0.0, 0.0)
        glRotatef(self.rotation_y, 0.0, 1.0, 0.0)
        
        if self.current_dff and self.current_dff.loaded:
            self._render_dff()


    def resizeGL(self, w, h): #vers 1
        if not OPENGL_AVAILABLE or h == 0:
            return
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w) / float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def set_model(self, dff: GTADff, txd: GTATxd = None): #vers 1
        self.current_dff = dff
        self.current_txd = txd
        self.texture_cache.clear()
        if txd and txd.loaded:
            self._load_textures(txd)
        self.update()


    def wheelEvent(self, event): #vers 1
        self.zoom += event.angleDelta().y() * 0.01
        self.update()


    def _load_textures(self, txd: GTATxd): #vers 1
        for i, tex in enumerate(txd.image):
            if tex.data and tex.width > 0 and tex.height > 0:
                tex_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                
                if tex.depth == 32:
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex.width, tex.height, 0,
                                GL_RGBA, GL_UNSIGNED_BYTE, tex.data)
                elif tex.depth == 8 and tex.palette:
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex.width, tex.height, 0,
                                GL_RGBA, GL_UNSIGNED_BYTE, tex.data)
                
                self.texture_cache[tex.name.lower()] = tex_id


    def _render_dff(self): #vers 1
        if not self.current_dff or not self.current_dff.clump:
            return
        
        clump = self.current_dff.clump[0]
        for geom in clump.geometry_list.geometry:
            data = geom.data
            if not data.vertex:
                continue
                
            glBegin(GL_TRIANGLES)
            for face_idx, face in enumerate(data.face):
                mat_idx = self._get_material_for_face(geom, face_idx)
                if mat_idx != -1 and mat_idx < len(geom.material_list.material):
                    mat = geom.material_list.material[mat_idx]
                    tex_name = mat.texture.name.lower()
                    if tex_name in self.texture_cache:
                        glEnable(GL_TEXTURE_2D)
                        glBindTexture(GL_TEXTURE_2D, self.texture_cache[tex_name])
                    else:
                        glDisable(GL_TEXTURE_2D)
                
                if face.v1 < len(data.vertex):
                    if data.uv and face.v1 < len(data.uv):
                        glTexCoord2f(data.uv[face.v1][0], data.uv[face.v1][1])
                    glVertex3f(*data.vertex[face.v1])
                    
                if face.v2 < len(data.vertex):
                    if data.uv and face.v2 < len(data.uv):
                        glTexCoord2f(data.uv[face.v2][0], data.uv[face.v2][1])
                    glVertex3f(*data.vertex[face.v2])
                    
                if face.v3 < len(data.vertex):
                    if data.uv and face.v3 < len(data.uv):
                        glTexCoord2f(data.uv[face.v3][0], data.uv[face.v3][1])
                    glVertex3f(*data.vertex[face.v3])
            glEnd()


    def _get_material_for_face(self, geom, face_idx: int) -> int: #vers 1
        for split in geom.material_split.split:
            if face_idx < split.face_index:
                return split.material_index
        return -1

# vers: 1.6
class MoomapperWindow(QMainWindow):
    def __init__(self):  #vers 1
        super().__init__()
        self.app_settings = AppSettings()
        self.icons = MoomapperIconProvider()
        
        self.current_img = None
        self.current_dff = None
        self.current_txd = None
        
        self.setWindowTitle("Moo Mapper - IMG Factory 1.6")
        self.resize(1200, 800)
        
        self._init_menu()
        self._init_toolbar()
        self._init_ui()
        self._init_statusbar()
        self._init_profiles()


    def _init_menu(self): #vers 3
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_profile_action = QAction(self.icons.open_icon(), "Open Game Profile...", self)
        open_profile_action.setShortcut("Ctrl+O")
        open_profile_action.triggered.connect(self.open_profile_dialog)
        file_menu.addAction(open_profile_action)

        open_game_action = QAction(self.icons.folder_icon(), "Select Game (gta3.dat)...", self)
        open_game_action.setShortcut("Ctrl+Shift+O")
        open_game_action.triggered.connect(self.open_game)
        file_menu.addAction(open_game_action)

        open_img_action = QAction(self.icons.folder_icon(), "Open IMG File Directly...", self)
        open_img_action.setShortcut("Ctrl+Shift+I")
        open_img_action.triggered.connect(self.open_img)
        file_menu.addAction(open_img_action)

        file_menu.addSeparator()

        manage_profiles_action = QAction("Manage Game Profiles...", self)
        manage_profiles_action.triggered.connect(self.manage_profiles)
        file_menu.addAction(manage_profiles_action)

        file_menu.addSeparator()

        exit_action = QAction(self.icons.exit_icon(), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


    def _init_statusbar(self): #vers 1
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")


    def _init_toolbar(self): #vers 2
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        open_profile_action = QAction(self.icons.open_icon(), "Open Profile", self)
        open_profile_action.triggered.connect(self.open_profile_dialog)
        self.toolbar.addAction(open_profile_action)

        open_game_action = QAction(self.icons.folder_icon(), "Select Game", self)
        open_game_action.triggered.connect(self.open_game)
        self.toolbar.addAction(open_game_action)


    def _init_ui(self): #vers 1
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.load_selected_file)
        left_layout.addWidget(QLabel("Archive Contents:"))
        left_layout.addWidget(self.file_list)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        if OPENGL_AVAILABLE:
            self.gl_widget = MoomapperGLWidget()
            right_layout.addWidget(self.gl_widget)
        else:
            right_layout.addWidget(QLabel("OpenGL not available. Install PyOpenGL."))
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])


    def _init_profiles(self): #vers 1
        self.profile_manager = GameProfileManager()


    def _detect_game_from_dat(self, dat_path: str): #vers 1
        """Detect game type and locate IMG file from default.dat"""
        dat_name = os.path.basename(dat_path).lower()
        game_folder = os.path.dirname(dat_path)

        # Try multiple possible IMG locations
        possible_paths = []

        if dat_name == 'gta3.dat':
            possible_paths = [
                os.path.join(game_folder, 'models', 'gta3.img'),
                os.path.join(game_folder, '..', 'models', 'gta3.img'),
                os.path.join(game_folder, 'gta3.img')
            ]
            game_type = 'gta3'
        elif dat_name == 'gta_vc.dat':
            possible_paths = [
                os.path.join(game_folder, 'models', 'gta3.img'),
                os.path.join(game_folder, '..', 'models', 'gta3.img'),
                os.path.join(game_folder, 'gta3.img')
            ]
            game_type = 'gta_vc'
        elif dat_name == 'gta_sa.dat':
            possible_paths = [
                os.path.join(game_folder, 'gta3.img'),
                os.path.join(game_folder, 'models', 'gta3.img'),
                os.path.join(game_folder, '..', 'models', 'gta3.img')
            ]
            game_type = 'gta_sa'
        else:
            return None, None

        # Find first existing path
        for path in possible_paths:
            if os.path.exists(path):
                return game_type, path

        # Return first path even if it doesn't exist (for error message)
        return game_type, possible_paths[0] if possible_paths else None


    def load_selected_file(self, item: QListWidgetItem): #vers 1
        if not self.current_img:
            return
            
        index = item.data(Qt.UserRole)
        entry = self.current_img.get_entry(index)
        
        try:
            stream = io.BytesIO()
            self.current_img.extract(index, stream)
            stream.seek(0)
            
            if entry.name.lower().endswith('.dff'):
                self.current_dff = GTADff(stream, entry.name, 0, len(stream.getvalue()))
                self.current_dff.load_from_stream()
                
                txd_name = entry.name[:-4]
                if self.current_img.txd_exists(txd_name):
                    txd_index = self.current_img.get_entry_num(txd_name + '.txd')
                    if txd_index != -1:
                        txd_stream = io.BytesIO()
                        self.current_img.extract(txd_index, txd_stream)
                        txd_stream.seek(0)
                        self.current_txd = GTATxd(txd_stream, txd_name, 0, len(txd_stream.getvalue()))
                        self.current_txd.load_from_stream()
                
                if OPENGL_AVAILABLE:
                    self.gl_widget.set_model(self.current_dff, self.current_txd)
                
                self.statusbar.showMessage(f"Loaded DFF: {entry.name}")
                
            elif entry.name.lower().endswith('.txd'):
                self.current_txd = GTATxd(stream, entry.name, 0, len(stream.getvalue()))
                self.current_txd.load_from_stream()
                self.statusbar.showMessage(f"Loaded TXD: {entry.name} ({self.current_txd.image_count} textures)")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")


    def open_profile_dialog(self): #vers 1
        """Show dialog to select from saved game profiles"""
        profiles = self.profile_manager.get_all_profiles()

        if not profiles:
            QMessageBox.information(
                self,
                "No Profiles",
                "No game profiles configured.\n\nUse 'Select Game' to add your first profile."
            )
            self.open_game()
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Game Profile")
        dialog.resize(400, 300)

        layout = QVBoxLayout(dialog)

        profile_list = QListWidget()
        for profile in profiles:
            profile_list.addItem(f"{profile.name} ({profile.game_type})")

        layout.addWidget(profile_list)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted and profile_list.currentRow() >= 0:
            profile = profiles[profile_list.currentRow()]
            self.load_profile(profile)


    def open_img(self): #vers 2
        """Open IMG file directly (legacy mode)"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open IMG Archive", "", "IMG Files (*.img);;All Files (*)"
        )
        if filename:
            try:
                self.current_img = GTAImg(filename)
                self.file_list.clear()
                for i in range(self.current_img.entry_count()):
                    entry = self.current_img.get_entry(i)
                    item = QListWidgetItem(entry.name)
                    item.setData(Qt.UserRole, i)
                    self.file_list.addItem(item)
                self.setWindowTitle(f"Moo Mapper - IMG Factory 1.6")
                self.statusbar.showMessage(f"Loaded: {filename} ({self.current_img.entry_count()} entries)")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open IMG:\n{str(e)}")


    def load_profile(self, profile: GameProfile): #vers 1
        """Load a game profile"""
        if not os.path.exists(profile.img_path):
            QMessageBox.critical(
                self,
                "IMG Not Found",
                f"IMG file not found:\n{profile.img_path}\n\nPlease update the profile."
            )
            return

        try:
            self.current_img = GTAImg(profile.img_path)
            self.file_list.clear()
            for i in range(self.current_img.entry_count()):
                entry = self.current_img.get_entry(i)
                item = QListWidgetItem(entry.name)
                item.setData(Qt.UserRole, i)
                self.file_list.addItem(item)

            game_names = {
                'gta3': 'GTA III',
                'gta_vc': 'Vice City',
                'gta_sa': 'San Andreas'
            }
            self.setWindowTitle(f"Moo Mapper - {profile.name} - IMG Factory 1.6")
            self.statusbar.showMessage(f"Loaded {profile.name}: {profile.img_path} ({self.current_img.entry_count()} entries)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open IMG:\n{str(e)}")


    def manage_profiles(self): #vers 1
        """Show profile management dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Game Profiles")
        dialog.resize(500, 400)

        layout = QVBoxLayout(dialog)

        profile_list = QListWidget()
        self._refresh_profile_list(profile_list)
        layout.addWidget(profile_list)

        button_layout = QHBoxLayout()

        add_button = QPushButton("Add New Profile")
        add_button.clicked.connect(lambda: self._add_profile_dialog(dialog, profile_list))
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(lambda: self._edit_profile_dialog(dialog, profile_list))
        button_layout.addWidget(edit_button)

        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(lambda: self._remove_profile(profile_list))
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()


    def _refresh_profile_list(self, list_widget: QListWidget): #vers 1
        list_widget.clear()
        for profile in self.profile_manager.get_all_profiles():
            list_widget.addItem(f"{profile.name} ({profile.game_type}) - {profile.img_path}")


    def _add_profile_dialog(self, parent, list_widget): #vers 1
        dialog = QDialog(parent)
        dialog.setWindowTitle("Add Game Profile")

        layout = QFormLayout(dialog)

        name_edit = QLineEdit()
        game_combo = QComboBox()
        game_combo.addItems(['gta3', 'gta_vc', 'gta_sa'])
        dat_edit = QLineEdit()
        img_edit = QLineEdit()

        layout.addRow("Profile Name:", name_edit)
        layout.addRow("Game Type:", game_combo)
        layout.addRow("DAT File Path:", dat_edit)
        layout.addRow("IMG File Path:", img_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        if dialog.exec_() == QDialog.Accepted:
            profile = GameProfile(
                name=name_edit.text(),
                game_type=game_combo.currentText(),
                dat_path=dat_edit.text(),
                img_path=img_edit.text()
            )
            self.profile_manager.add_profile(profile)
            self._refresh_profile_list(list_widget)


    def _remove_profile(self, list_widget): #vers 1
        current_row = list_widget.currentRow()
        if current_row < 0:
            return

        reply = QMessageBox.question(
            self,
            "Remove Profile",
            "Are you sure you want to remove this profile?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.profile_manager.remove_profile(current_row)
            self._refresh_profile_list(list_widget)


    def _edit_profile_dialog(self, parent, list_widget): #vers 1
        current_row = list_widget.currentRow()
        if current_row < 0:
            return

        profile = self.profile_manager.get_profile(current_row)
        if not profile:
            return

        dialog = QDialog(parent)
        dialog.setWindowTitle("Edit Game Profile")

        layout = QFormLayout(dialog)

        name_edit = QLineEdit(profile.name)
        game_combo = QComboBox()
        game_combo.addItems(['gta3', 'gta_vc', 'gta_sa'])
        game_combo.setCurrentText(profile.game_type)
        dat_edit = QLineEdit(profile.dat_path)
        img_edit = QLineEdit(profile.img_path)

        layout.addRow("Profile Name:", name_edit)
        layout.addRow("Game Type:", game_combo)
        layout.addRow("DAT File Path:", dat_edit)
        layout.addRow("IMG File Path:", img_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        if dialog.exec_() == QDialog.Accepted:
            profile.name = name_edit.text()
            profile.game_type = game_combo.currentText()
            profile.dat_path = dat_edit.text()
            profile.img_path = img_edit.text()
            self.profile_manager.update_profile(current_row, profile)
            self._refresh_profile_list(list_widget)


    def open_game(self): #vers 2
        """Open game via default.dat file and optionally save as profile"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game Data File",
            "",
            "GTA Data Files (gta3.dat gta_vc.dat gta_sa.dat);;GTA III (gta3.dat);;Vice City (gta_vc.dat);;San Andreas (gta_sa.dat);;All Files (*)"
        )
        if not filename:
            return

        game_type, img_path = self._detect_game_from_dat(filename)

        if not game_type:
            QMessageBox.warning(self, "Unknown Game", f"Unrecognized data file: {filename}")
            return

        # Ask if user wants to save as profile
        reply = QMessageBox.question(
            self,
            "Save Profile?",
            f"Would you like to save this as a game profile?\n\nGame: {game_type}\nDAT: {filename}\nIMG: {img_path}",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            profile_name, ok = QInputDialog.getText(
                self,
                "Profile Name",
                "Enter a name for this profile:",
                text=f"{game_type.upper()} Game"
            )
            if ok and profile_name:
                profile = GameProfile(
                    name=profile_name,
                    game_type=game_type,
                    dat_path=filename,
                    img_path=img_path
                )
                self.profile_manager.add_profile(profile)

        if not os.path.exists(img_path):
            QMessageBox.critical(
                self,
                "IMG Not Found",
                f"Could not find IMG file:\n{img_path}\n\nPlease check the path and try again."
            )
            return

        try:
            self.current_img = GTAImg(img_path)
            self.file_list.clear()
            for i in range(self.current_img.entry_count()):
                entry = self.current_img.get_entry(i)
                item = QListWidgetItem(entry.name)
                item.setData(Qt.UserRole, i)
                self.file_list.addItem(item)

            game_names = {
                'gta3': 'GTA III',
                'gta_vc': 'Vice City',
                'gta_sa': 'San Andreas'
            }
            self.setWindowTitle(f"Moo Mapper - {game_names.get(game_type, game_type)} - IMG Factory 1.6")
            self.statusbar.showMessage(f"Loaded {game_names.get(game_type)}: {img_path} ({self.current_img.entry_count()} entries)")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open IMG:\n{str(e)}")


def main(): #vers 2
    app = QApplication(sys.argv)
    app.setApplicationName("Moo Mapper")
    app.setOrganizationName("X-Seti")
    
    settings = AppSettings()
    apply_theme_to_app(app, settings)
    
    window = MoomapperWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
