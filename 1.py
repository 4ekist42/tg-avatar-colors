import sys
from PyQt5 import QtWidgets, QtCore

TDESKTOP_PALETTE = [
    ("Red", "#d45246"),
    ("Green", "#46ba43"),
    ("Yellow", "#e5ca77"),
    ("Blue", "#408acf"),
    ("Purple", "#6c61df"),
    ("Pink", "#d95574"),
    ("Sea", "#359ad4"),
    ("Orange", "#f68136"),
]

TDESKTOP_VISIBLE_INDICES = [0, 1, 3, 4, 5, 6, 7]

TDX_PALETTE = [
    ("Red", "#CC5049"),
    ("Green", "#40A920"),
    ("Blue", "#368AD1"),
    ("Violet", "#955CDB"),
    ("Pink", "#C7508B"),
    ("Cyan", "#309EBA"),
    ("Orange", "#D67722"),
]

TDX_VISIBLE = [TDX_PALETTE[i] for i in range(len(TDX_PALETTE))]

IOS_GRADIENTS = [
    ("Red", "#ff516a"),
    ("Orange", "#ffa85c"),
    ("Violet", "#665fff"),
    ("Green", "#54cb68"),
    ("Cyan", "#4acccd"),
    ("Blue", "#2a9ef1"),
    ("Pink", "#d669ed"),
]

MAP = [0, 7, 4, 1, 6, 3, 5]

TDESKTOP_INDEX_TO_TDX_POS = {idx: pos for pos, idx in enumerate(TDESKTOP_VISIBLE_INDICES)}


def tdesktop_palette_index(peer_id: int) -> int:
    return MAP[peer_id % len(MAP)]


def tdesktop_color_name(peer_id: int) -> str:
    return TDESKTOP_PALETTE[tdesktop_palette_index(peer_id)][0]


def tdx_color_name(peer_id: int) -> str:
    desktop_index = tdesktop_palette_index(peer_id)
    pos = TDESKTOP_INDEX_TO_TDX_POS.get(desktop_index)
    if pos is None:
        return "Unknown"
    return TDX_VISIBLE[pos][0]


def ios_color_name(peer_id: int) -> str:
    idx = abs(int(peer_id)) % len(IOS_GRADIENTS)
    return IOS_GRADIENTS[idx][0]


def macos_color_name(peer_id: int) -> str:
    idx = abs(int(peer_id)) % len(IOS_GRADIENTS)
    return IOS_GRADIENTS[idx][0]


class ColorButton(QtWidgets.QPushButton):
    def __init__(self, name: str, hex_color: str, on_click):
        super().__init__(name)
        self.name = name
        self.hex = hex_color
        self.on_click = on_click
        self.setFixedSize(150, 80)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                border-radius: 8px;
                border: 3px solid #222;
                font-size: 18px;
                font-weight: bold;
                color: white;
            }}
            QPushButton:hover {{
                border: 3px solid white;
            }}
        """)
        self.clicked.connect(lambda: self.on_click(self.name))


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Avatar Color Inspector")
        self.resize(1100, 900)

        self.current_client = "tdesktop"
        self.selected_color_name = None

        main_layout = QtWidgets.QVBoxLayout()

        self.info_label = QtWidgets.QLabel("")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #999; font-size: 13px;")
        main_layout.addWidget(self.info_label)

        client_layout = QtWidgets.QHBoxLayout()
        client_label = QtWidgets.QLabel("Клиент:")
        client_label.setFixedWidth(120)
        self.client_combo = QtWidgets.QComboBox()
        self.client_combo.addItem("Telegram Desktop", "tdesktop")
        self.client_combo.addItem("Telegram X (Android)", "tgx")
        self.client_combo.addItem("Telegram iOS", "ios")
        self.client_combo.addItem("Telegram macOS (native)", "macos")
        self.client_combo.currentIndexChanged.connect(self.on_client_changed)
        client_layout.addWidget(client_label)
        client_layout.addWidget(self.client_combo)
        client_layout.addStretch()
        main_layout.addLayout(client_layout)

        self.palette_group = QtWidgets.QGroupBox("Палитра")
        self.palette_layout = QtWidgets.QGridLayout()
        self.palette_group.setLayout(self.palette_layout)
        main_layout.addWidget(self.palette_group)

        self.rebuild_palette()

        self.ids_input = QtWidgets.QPlainTextEdit()
        self.ids_input.setPlaceholderText("Введи Telegram ID построчно…")
        self.ids_input.setFixedHeight(170)
        main_layout.addWidget(self.ids_input)

        btns = QtWidgets.QHBoxLayout()

        self.filter_btn = QtWidgets.QPushButton("Фильтр по выбранному цвету")
        self.filter_btn.setFixedHeight(60)
        self.filter_btn.setStyleSheet("font-size:18px; font-weight:bold;")
        self.filter_btn.clicked.connect(self.apply_filter)
        btns.addWidget(self.filter_btn)

        self.show_btn = QtWidgets.QPushButton("Показать цвета для ID\n(во всех клиентах)")
        self.show_btn.setFixedHeight(60)
        self.show_btn.setStyleSheet("font-size:16px; font-weight:bold;")
        self.show_btn.clicked.connect(self.show_colors_for_ids)
        btns.addWidget(self.show_btn)

        main_layout.addLayout(btns)

        self.result_box = QtWidgets.QPlainTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(300)
        main_layout.addWidget(self.result_box)

        self.setLayout(main_layout)

    def rebuild_palette(self):
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        if self.current_client == "tdesktop":
            palette = [(TDESKTOP_PALETTE[i][0], TDESKTOP_PALETTE[i][1]) for i in TDESKTOP_VISIBLE_INDICES]
        elif self.current_client == "tgx":
            palette = TDX_VISIBLE
        else:
            palette = IOS_GRADIENTS

        row, col = 0, 0
        for name, hexcol in palette:
            btn = ColorButton(name, hexcol, self.on_color_clicked)
            self.palette_layout.addWidget(btn, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

        self.selected_color_name = None
        self.info_label.setText("Выбери цвет, затем используй фильтр или просмотр.")

    def on_client_changed(self, idx):
        self.current_client = self.client_combo.itemData(idx)
        self.result_box.clear()
        self.rebuild_palette()

    def on_color_clicked(self, name):
        self.selected_color_name = name
        self.info_label.setText(f"Выбран цвет [{self.current_client}]: {name}")
        self.result_box.clear()

    def _parse_ids(self):
        ids = []
        for line in self.ids_input.toPlainText().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ids.append(int(line))
            except ValueError:
                pass
        return ids

    def apply_filter(self):
        ids = self._parse_ids()
        if not ids:
            self.result_box.setPlainText("Нет валидных ID.")
            return

        if not self.selected_color_name:
            self.result_box.setPlainText("Сначала выбери цвет.")
            return

        want = self.selected_color_name
        matched = []

        for pid in ids:
            if self.current_client == "tdesktop":
                name = tdesktop_color_name(pid)
            elif self.current_client == "tgx":
                name = tdx_color_name(pid)
            elif self.current_client == "ios":
                name = ios_color_name(pid)
            else:
                name = macos_color_name(pid)

            if name == want:
                matched.append(pid)

        if matched:
            self.result_box.setPlainText("\n".join(map(str, matched)))
        else:
            self.result_box.setPlainText("Нет совпадений для выбранного цвета.")

    def show_colors_for_ids(self):
        ids = self._parse_ids()
        if not ids:
            self.result_box.setPlainText("Нет валидных ID.")
            return

        out = []
        for pid in ids:
            td = tdesktop_color_name(pid)
            tgx = tdx_color_name(pid)
            ios_name = ios_color_name(pid)
            mac_name = macos_color_name(pid)
            out.append(f"{pid}:  TDesktop={td},  TGX={tgx},  iOS={ios_name},  macOS={mac_name}")

        self.result_box.setPlainText("\n".join(out))


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()