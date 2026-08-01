#belongs in apps/components/Moomapper/depends/icon_provider.py -Version:1.6
# X-Seti-2026-08-01

from PyQt5.QtGui import QIcon, QColor, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray

from apps.components.Moomapper.depends.moomapper_svg_icons import (
    COLLISION_SVG, EXIT_SVG, EXTRACT_SVG, FOLDER_SVG, MAP_SVG,
    MODEL_SVG, OPEN_SVG, ROTATE_SVG, TEXTURE_SVG, ZOOM_SVG
)

# vers: 1.6
class MoomapperIconProvider:
    def __init__(self, tint_color: str = "#ffffff"):
        self.tint_color = QColor(tint_color)
        self._cache = {}

    # vers: 1.6
    def _load_icon(self, svg_data: str) -> QIcon:
        cache_key = id(svg_data)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        renderer = QSvgRenderer(QByteArray(svg_data.encode('utf-8')))
        pixmap = QPixmap(24, 24)
        pixmap.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        icon = QIcon(pixmap)
        self._cache[cache_key] = icon
        return icon

    # vers: 1.6
    def collision_icon(self) -> QIcon:
        return self._load_icon(COLLISION_SVG)

    # vers: 1.6
    def exit_icon(self) -> QIcon:
        return self._load_icon(EXIT_SVG)

    # vers: 1.6
    def extract_icon(self) -> QIcon:
        return self._load_icon(EXTRACT_SVG)

    # vers: 1.6
    def folder_icon(self) -> QIcon:
        return self._load_icon(FOLDER_SVG)

    # vers: 1.6
    def map_icon(self) -> QIcon:
        return self._load_icon(MAP_SVG)

    # vers: 1.6
    def model_icon(self) -> QIcon:
        return self._load_icon(MODEL_SVG)

    # vers: 1.6
    def open_icon(self) -> QIcon:
        return self._load_icon(OPEN_SVG)

    # vers: 1.6
    def rotate_icon(self) -> QIcon:
        return self._load_icon(ROTATE_SVG)

    # vers: 1.6
    def texture_icon(self) -> QIcon:
        return self._load_icon(TEXTURE_SVG)

    # vers: 1.6
    def zoom_icon(self) -> QIcon:
        return self._load_icon(ZOOM_SVG)