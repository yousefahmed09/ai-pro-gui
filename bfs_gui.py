import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import copy
import sys

# Attempt DPI awareness for sharp rendering on Windows
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ==========================================
# PRESET MAZES FROM ORIGINAL SCRIPT
# ==========================================
MAZE_PRESETS = {
    "Maze 1 (10x10)": [
        [0,0,0,1,0,0,0,0,0,0],
        [1,1,0,1,0,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,0,1,0],
        [0,0,0,0,0,0,1,0,0,0],
        [1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,1,1,0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,0,0,0]
    ],
    "Maze 2 (15x15)": [
        [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
        [1,1,0,1,0,1,1,0,1,0,1,1,1,1,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,0,1,1,1,1,1,1,0,1,0],
        [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
        [1,1,1,0,1,1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
        [1,1,1,1,1,1,0,1,1,1,1,1,0,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,1,1,1,0,1,1,1,1,1,0,1,1,1,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
        [1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    "Maze 3 (21x21)": [
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
        [1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
        [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
}

# BFS movement order matching original script: (Right, Down, Left, Up)
DIRECTIONS = [
    (0, 1),   # right
    (1, 0),   # down
    (0, -1),  # left
    (-1, 0)   # up
]

class BFSMazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Maze Solver & Pathfinding Visualizer")
        self.root.geometry("1100x800")
        self.root.minsize(950, 700)
        self.root.configure(bg="#1e1e2e")

        # Color palette
        self.COLOR_BG = "#1e1e2e"
        self.COLOR_PANEL = "#252538"
        self.COLOR_TEXT = "#cdd6f4"
        self.COLOR_SUBTEXT = "#a6adc8"
        self.COLOR_WALL = "#11111b"
        self.COLOR_EMPTY = "#313244"
        self.COLOR_GRID_LINE = "#45475a"
        self.COLOR_START = "#a6e3a1"       # Light green
        self.COLOR_END = "#f38ba8"         # Coral red
        self.COLOR_VISITED = "#89b4fa"     # Soft blue
        self.COLOR_FRONTIER = "#cba6f7"    # Purple/Lilac
        self.COLOR_PATH = "#f9e2af"        # Soft gold/yellow
        self.COLOR_PATH_ARROW = "#181825"  # Dark contrast for arrow

        # State
        self.current_preset_name = "Maze 1 (10x10)"
        self.maze = copy.deepcopy(MAZE_PRESETS[self.current_preset_name])
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)

        # Ensure start and end are not on walls initially
        self._ensure_endpoints_valid()

        # Visualizer state
        self.interaction_mode = tk.StringVar(value="wall")  # "wall", "start", "end", "erase"
        self.is_animating = False
        self.is_paused = False
        self.anim_job = None
        self.visited_set = set()
        self.final_path = []
        self.bfs_queue = deque()
        self.parent_map = {}
        self.step_delay_ms = tk.IntVar(value=30)
        self.paint_value = None

        self._init_styles()
        self._create_layout()
        self._draw_board()

    def _ensure_endpoints_valid(self):
        """Make sure start and end positions are within bounds and on open cells."""
        if self.maze[self.start[0]][self.start[1]] == 1:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.maze[r][c] == 0:
                        self.start = (r, c)
                        break
                else:
                    continue
                break

        if self.maze[self.end[0]][self.end[1]] == 1 or self.end == self.start:
            for r in range(self.rows - 1, -1, -1):
                for c in range(self.cols - 1, -1, -1):
                    if self.maze[r][c] == 0 and (r, c) != self.start:
                        self.end = (r, c)
                        break
                else:
                    continue
                break

    def _init_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=self.COLOR_BG)
        style.configure("Card.TFrame", background=self.COLOR_PANEL)

        style.configure(
            "TLabel",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_TEXT,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Header.TLabel",
            background=self.COLOR_PANEL,
            foreground="#fab387",
            font=("Segoe UI", 11, "bold")
        )
        style.configure(
            "Title.TLabel",
            background=self.COLOR_BG,
            foreground="#cdd6f4",
            font=("Segoe UI", 16, "bold")
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#89b4fa",
            foreground="#11111b",
            borderwidth=0,
            padding=6
        )
        style.map("Action.TButton", background=[("active", "#b4befe")])

        style.configure(
            "Instant.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#a6e3a1",
            foreground="#11111b",
            borderwidth=0,
            padding=6
        )
        style.map("Instant.TButton", background=[("active", "#94e2d5")])

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 9),
            background="#45475a",
            foreground="#cdd6f4",
            borderwidth=0,
            padding=5
        )
        style.map("Secondary.TButton", background=[("active", "#585b70")])

        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 9, "bold"),
            background="#f38ba8",
            foreground="#11111b",
            borderwidth=0,
            padding=5
        )
        style.map("Danger.TButton", background=[("active", "#eba0ac")])

        style.configure(
            "TRadiobutton",
            background=self.COLOR_PANEL,
            foreground=self.COLOR_TEXT,
            font=("Segoe UI", 9)
        )

    def _create_layout(self):
        # Top title banner
        header_frame = tk.Frame(self.root, bg=self.COLOR_BG, pady=10, padx=20)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = ttk.Label(
            header_frame,
            text="BFS Maze Pathfinding Visualizer",
            style="Title.TLabel"
        )
        title_lbl.pack(side=tk.LEFT)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Interactive Breadth-First Search Algorithm",
            bg=self.COLOR_BG,
            fg=self.COLOR_SUBTEXT,
            font=("Segoe UI", 10, "italic")
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=15, pady=(5, 0))

        # Main content area (Left: Canvas, Right: Control Panel)
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG, padx=15, pady=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: Canvas container
        canvas_card = tk.Frame(main_frame, bg=self.COLOR_PANEL, padx=10, pady=10)
        canvas_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_card,
            bg=self.COLOR_WALL,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Canvas event bindings
        self.canvas.bind("<Configure>", lambda e: self._draw_board())
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)

        # Right: Sidebar Controls
        sidebar = tk.Frame(main_frame, bg=self.COLOR_PANEL, width=320, padx=15, pady=10)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))
        sidebar.pack_propagate(False)

        # 1. Preset Maze Selection
        sec1 = ttk.Label(sidebar, text="1. Select Maze", style="Header.TLabel")
        sec1.pack(anchor=tk.W, pady=(0, 4))

        self.preset_combo = ttk.Combobox(
            sidebar,
            values=list(MAZE_PRESETS.keys()) + ["Custom Empty (15x15)", "Random Maze (15x15)"],
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.preset_combo.set(self.current_preset_name)
        self.preset_combo.pack(fill=tk.X, pady=(0, 10))
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_change)

        # 2. Mouse Tool Mode
        sec2 = ttk.Label(sidebar, text="2. Mouse Click Tool", style="Header.TLabel")
        sec2.pack(anchor=tk.W, pady=(5, 4))

        tool_frame = tk.Frame(sidebar, bg=self.COLOR_PANEL)
        tool_frame.pack(fill=tk.X, pady=(0, 10))

        tools = [
            ("🟩 Set Start Point (S)", "start"),
            ("🟥 Set Goal Point (G)", "end"),
            ("⬛ Draw / Toggle Wall (#)", "wall"),
            ("⬜ Erase Wall (.)", "erase")
        ]
        for text, mode in tools:
            rb = ttk.Radiobutton(
                tool_frame,
                text=text,
                value=mode,
                variable=self.interaction_mode
            )
            rb.pack(anchor=tk.W, pady=2)

        # 3. Execution & Animation Controls
        sec3 = ttk.Label(sidebar, text="3. Run Algorithm", style="Header.TLabel")
        sec3.pack(anchor=tk.W, pady=(5, 4))

        btn_run = ttk.Button(sidebar, text="▶ Visualize BFS", style="Action.TButton", command=self.start_animated_bfs)
        btn_run.pack(fill=tk.X, pady=3)

        btn_instant = ttk.Button(sidebar, text="⚡ Instant Solve", style="Instant.TButton", command=self.solve_instant)
        btn_instant.pack(fill=tk.X, pady=3)

        speed_frame = tk.Frame(sidebar, bg=self.COLOR_PANEL)
        speed_frame.pack(fill=tk.X, pady=(6, 8))
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        speed_slider = tk.Scale(
            speed_frame,
            from_=2,
            to=150,
            orient=tk.HORIZONTAL,
            variable=self.step_delay_ms,
            showvalue=0,
            bg=self.COLOR_PANEL,
            troughcolor="#313244",
            highlightthickness=0,
            activebackground="#89b4fa"
        )
        speed_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(8, 0))

        # Reset / Clear Buttons
        btn_box = tk.Frame(sidebar, bg=self.COLOR_PANEL)
        btn_box.pack(fill=tk.X, pady=(0, 10))

        btn_clear_path = ttk.Button(btn_box, text="Clear Path", style="Secondary.TButton", command=self.clear_path_only)
        btn_clear_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))

        btn_reset = ttk.Button(btn_box, text="Reset Maze", style="Danger.TButton", command=self.reset_maze)
        btn_reset.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(3, 0))

        # 4. Status & Statistics Dashboard
        sec4 = ttk.Label(sidebar, text="4. Results & Stats", style="Header.TLabel")
        sec4.pack(anchor=tk.W, pady=(5, 4))

        stats_card = tk.Frame(sidebar, bg="#181825", padx=10, pady=8, relief=tk.FLAT)
        stats_card.pack(fill=tk.X, pady=(0, 10))

        self.lbl_status = tk.Label(
            stats_card,
            text="Status: Ready",
            bg="#181825",
            fg="#89dceb",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_status.pack(anchor=tk.W, pady=1)

        self.lbl_start_pos = tk.Label(
            stats_card,
            text=f"Start (S): {self.start}",
            bg="#181825",
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 9)
        )
        self.lbl_start_pos.pack(anchor=tk.W, pady=1)

        self.lbl_end_pos = tk.Label(
            stats_card,
            text=f"Goal (G): {self.end}",
            bg="#181825",
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 9)
        )
        self.lbl_end_pos.pack(anchor=tk.W, pady=1)

        self.lbl_visited_count = tk.Label(
            stats_card,
            text="Visited Nodes: 0",
            bg="#181825",
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 9)
        )
        self.lbl_visited_count.pack(anchor=tk.W, pady=1)

        self.lbl_path_length = tk.Label(
            stats_card,
            text="Shortest Path Steps: 0",
            bg="#181825",
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 9)
        )
        self.lbl_path_length.pack(anchor=tk.W, pady=1)

        # 5. Legend
        sec5 = ttk.Label(sidebar, text="Legend", style="Header.TLabel")
        sec5.pack(anchor=tk.W, pady=(5, 4))

        legend_box = tk.Frame(sidebar, bg=self.COLOR_PANEL)
        legend_box.pack(fill=tk.X)

        items = [
            (self.COLOR_START, "Start Position (S)"),
            (self.COLOR_END, "Goal Position (G)"),
            (self.COLOR_WALL, "Wall / Obstacle (#)"),
            (self.COLOR_VISITED, "Explored Cells"),
            (self.COLOR_PATH, "Optimal Path (→ ↓ ↑ ←)")
        ]
        for color, desc in items:
            row = tk.Frame(legend_box, bg=self.COLOR_PANEL)
            row.pack(fill=tk.X, pady=2)
            c_box = tk.Canvas(row, width=14, height=14, bg=color, highlightthickness=1, highlightbackground="#45475a")
            c_box.pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(row, text=desc, bg=self.COLOR_PANEL, fg=self.COLOR_SUBTEXT, font=("Segoe UI", 8)).pack(side=tk.LEFT)

    # ==========================================
    # CANVAS DRAWING & COORDINATES
    # ==========================================
    def _get_cell_geometry(self):
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        if c_width <= 1 or c_height <= 1:
            c_width, c_height = 650, 650

        margin = 15
        avail_w = max(50, c_width - 2 * margin)
        avail_h = max(50, c_height - 2 * margin)

        cell_size = min(avail_w // self.cols, avail_h // self.rows)
        cell_size = max(10, cell_size)

        total_grid_w = cell_size * self.cols
        total_grid_h = cell_size * self.rows

        offset_x = (c_width - total_grid_w) // 2
        offset_y = (c_height - total_grid_h) // 2

        return cell_size, offset_x, offset_y

    def _draw_board(self):
        self.canvas.delete("all")
        cell_size, offset_x, offset_y = self._get_cell_geometry()

        path_set = set(self.final_path)

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = offset_x + c * cell_size
                y1 = offset_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Determine cell color
                if (r, c) == self.start:
                    fill_color = self.COLOR_START
                elif (r, c) == self.end:
                    fill_color = self.COLOR_END
                elif (r, c) in path_set:
                    fill_color = self.COLOR_PATH
                elif (r, c) in self.visited_set:
                    fill_color = self.COLOR_VISITED
                elif self.maze[r][c] == 1:
                    fill_color = self.COLOR_WALL
                else:
                    fill_color = self.COLOR_EMPTY

                # Draw cell rectangle
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=self.COLOR_GRID_LINE,
                    width=1,
                    tags=f"cell_{r}_{c}"
                )

                # Draw labels / symbols
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                if (r, c) == self.start:
                    font_size = max(8, int(cell_size * 0.45))
                    self.canvas.create_text(cx, cy, text="S", fill="#11111b", font=("Segoe UI", font_size, "bold"))
                elif (r, c) == self.end:
                    font_size = max(8, int(cell_size * 0.45))
                    self.canvas.create_text(cx, cy, text="G", fill="#11111b", font=("Segoe UI", font_size, "bold"))
                elif (r, c) in path_set and len(self.final_path) > 1:
                    # Draw arrows matching the console output (→, ↓, ↑, ←)
                    idx = self.final_path.index((r, c))
                    if idx < len(self.final_path) - 1:
                        next_r, next_c = self.final_path[idx + 1]
                        arrow = ""
                        if next_c == c + 1:
                            arrow = "→"
                        elif next_r == r + 1:
                            arrow = "↓"
                        elif next_r == r - 1:
                            arrow = "↑"
                        elif next_c == c - 1:
                            arrow = "←"

                        if arrow and cell_size >= 14:
                            arrow_font_size = max(8, int(cell_size * 0.5))
                            self.canvas.create_text(cx, cy, text=arrow, fill=self.COLOR_PATH_ARROW, font=("Segoe UI", arrow_font_size, "bold"))

    def _get_cell_at_pixel(self, px, py):
        cell_size, offset_x, offset_y = self._get_cell_geometry()
        col = (px - offset_x) // cell_size
        row = (py - offset_y) // cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(row), int(col)
        return None

    # ==========================================
    # INTERACTION & EDITING
    # ==========================================
    def _on_canvas_click(self, event):
        if self.is_animating:
            return
        cell = self._get_cell_at_pixel(event.x, event.y)
        if not cell:
            return

        r, c = cell
        mode = self.interaction_mode.get()

        if mode == "start":
            if self.maze[r][c] == 1:
                self.maze[r][c] = 0
            if (r, c) == self.end:
                self.end = self.start
            self.start = (r, c)
            self.lbl_start_pos.config(text=f"Start (S): {self.start}")
            self.clear_path_only()
            self._draw_board()

        elif mode == "end":
            if self.maze[r][c] == 1:
                self.maze[r][c] = 0
            if (r, c) == self.start:
                self.start = self.end
            self.end = (r, c)
            self.lbl_end_pos.config(text=f"Goal (G): {self.end}")
            self.clear_path_only()
            self._draw_board()

        elif mode == "wall":
            if (r, c) != self.start and (r, c) != self.end:
                new_val = 0 if self.maze[r][c] == 1 else 1
                self.paint_value = new_val
                self.maze[r][c] = new_val
                self.clear_path_only()
                self._draw_board()

        elif mode == "erase":
            if (r, c) != self.start and (r, c) != self.end:
                self.maze[r][c] = 0
                self.clear_path_only()
                self._draw_board()

    def _on_canvas_drag(self, event):
        if self.is_animating:
            return
        cell = self._get_cell_at_pixel(event.x, event.y)
        if not cell:
            return

        r, c = cell
        if (r, c) == self.start or (r, c) == self.end:
            return

        mode = self.interaction_mode.get()
        if mode == "wall":
            val = 1 if self.paint_value is None else self.paint_value
            if self.maze[r][c] != val:
                self.maze[r][c] = val
                self.clear_path_only()
                self._draw_board()
        elif mode == "erase":
            if self.maze[r][c] != 0:
                self.maze[r][c] = 0
                self.clear_path_only()
                self._draw_board()

    def _on_canvas_release(self, event):
        self.paint_value = None

    def _on_canvas_right_click(self, event):
        """Right click quickly sets Goal position."""
        if self.is_animating:
            return
        cell = self._get_cell_at_pixel(event.x, event.y)
        if not cell:
            return
        r, c = cell
        if self.maze[r][c] == 1:
            self.maze[r][c] = 0
        self.end = (r, c)
        self.lbl_end_pos.config(text=f"Goal (G): {self.end}")
        self.clear_path_only()
        self._draw_board()

    def _on_preset_change(self, event=None):
        if self.is_animating:
            self._stop_animation()

        selected = self.preset_combo.get()
        if selected in MAZE_PRESETS:
            self.current_preset_name = selected
            self.maze = copy.deepcopy(MAZE_PRESETS[selected])
            self.rows = len(self.maze)
            self.cols = len(self.maze[0])
            self.start = (0, 0)
            self.end = (self.rows - 1, self.cols - 1)
        elif "Custom Empty" in selected:
            self.rows, self.cols = 15, 15
            self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            self.start = (0, 0)
            self.end = (self.rows - 1, self.cols - 1)
        elif "Random Maze" in selected:
            import random
            self.rows, self.cols = 15, 15
            self.maze = [[1 if random.random() < 0.28 else 0 for _ in range(self.cols)] for _ in range(self.rows)]
            self.start = (0, 0)
            self.end = (self.rows - 1, self.cols - 1)
            self.maze[self.start[0]][self.start[1]] = 0
            self.maze[self.end[0]][self.end[1]] = 0

        self._ensure_endpoints_valid()
        self.lbl_start_pos.config(text=f"Start (S): {self.start}")
        self.lbl_end_pos.config(text=f"Goal (G): {self.end}")
        self.clear_path_only()
        self._draw_board()

    def reset_maze(self):
        self._on_preset_change()

    def clear_path_only(self):
        if self.is_animating:
            self._stop_animation()
        self.visited_set.clear()
        self.final_path.clear()
        self.lbl_status.config(text="Status: Ready", fg="#89dceb")
        self.lbl_visited_count.config(text="Visited Nodes: 0")
        self.lbl_path_length.config(text="Shortest Path Steps: 0")
        self._draw_board()

    # ==========================================
    # BFS ALGORITHM ENGINE
    # ==========================================
    def _validate_endpoints(self):
        if self.maze[self.start[0]][self.start[1]] == 1:
            messagebox.showwarning("Invalid Start", "Start position is located inside a wall!")
            return False
        if self.maze[self.end[0]][self.end[1]] == 1:
            messagebox.showwarning("Invalid Goal", "Goal position is located inside a wall!")
            return False
        return True

    def solve_instant(self):
        """Runs the BFS algorithm instantly without animation."""
        if not self._validate_endpoints():
            return
        if self.is_animating:
            self._stop_animation()

        # Pure BFS matching user script
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        found_path = None

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.end:
                found_path = path
                break

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows and
                    0 <= ny < self.cols and
                    self.maze[nx][ny] == 0 and
                    (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        self.visited_set = visited
        self.final_path = found_path if found_path else []

        if found_path:
            self.lbl_status.config(text="Status: Path Found! 🎉", fg="#a6e3a1")
            self.lbl_visited_count.config(text=f"Visited Nodes: {len(visited) - 1}")
            self.lbl_path_length.config(text=f"Shortest Path Steps: {len(found_path) - 1}")
        else:
            self.lbl_status.config(text="Status: No Path Found! ❌", fg="#f38ba8")
            self.lbl_visited_count.config(text=f"Visited Nodes: {len(visited) - 1}")
            self.lbl_path_length.config(text="Shortest Path Steps: N/A")

        self._draw_board()

    def start_animated_bfs(self):
        """Starts step-by-step visual exploration of BFS."""
        if not self._validate_endpoints():
            return
        if self.is_animating:
            self._stop_animation()

        self.clear_path_only()
        self.is_animating = True
        self.lbl_status.config(text="Status: Exploring Maze...", fg="#fab387")

        self.bfs_queue = deque([(self.start, [self.start])])
        self.visited_set = {self.start}
        self.found_path = None

        self._step_bfs_animation()

    def _step_bfs_animation(self):
        if not self.is_animating:
            return

        if not self.bfs_queue:
            # Queue exhausted and end not reached
            self.is_animating = False
            self.lbl_status.config(text="Status: No Path Found! ❌", fg="#f38ba8")
            self.lbl_visited_count.config(text=f"Visited Nodes: {len(self.visited_set) - 1}")
            self.lbl_path_length.config(text="Shortest Path Steps: N/A")
            self._draw_board()
            return

        (x, y), path = self.bfs_queue.popleft()

        if (x, y) == self.end:
            # Reached goal! Animate path reconstruction
            self.found_path = path
            self.lbl_status.config(text="Status: Path Found! Tracing...", fg="#a6e3a1")
            self.lbl_visited_count.config(text=f"Visited Nodes: {len(self.visited_set) - 1}")
            self._animate_path_trace(0)
            return

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.rows and
                0 <= ny < self.cols and
                self.maze[nx][ny] == 0 and
                (nx, ny) not in self.visited_set):
                self.visited_set.add((nx, ny))
                self.bfs_queue.append(((nx, ny), path + [(nx, ny)]))

        self.lbl_visited_count.config(text=f"Visited Nodes: {len(self.visited_set) - 1}")
        self._draw_board()

        delay = max(1, self.step_delay_ms.get())
        self.anim_job = self.root.after(delay, self._step_bfs_animation)

    def _animate_path_trace(self, idx):
        if not self.is_animating:
            return

        if idx <= len(self.found_path):
            self.final_path = self.found_path[:idx]
            self.lbl_path_length.config(text=f"Shortest Path Steps: {max(0, len(self.final_path) - 1)}")
            self._draw_board()
            delay = max(20, self.step_delay_ms.get() * 2)
            self.anim_job = self.root.after(delay, lambda: self._animate_path_trace(idx + 1))
        else:
            self.is_animating = False
            self.lbl_status.config(text="Status: Complete! 🎉", fg="#a6e3a1")
            self.lbl_path_length.config(text=f"Shortest Path Steps: {len(self.found_path) - 1}")

    def _stop_animation(self):
        self.is_animating = False
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None


# ==========================================
# MAIN APPLICATION LAUNCHER
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = BFSMazeApp(root)
    root.mainloop()
