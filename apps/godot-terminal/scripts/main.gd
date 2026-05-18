extends Control

@export var nerd_font_path: String = "res://assets/fonts/JetBrainsMonoNerdFontMono-Regular.ttf"
@export var font_size: int = 20
@export var default_fg: Color = Color(0.86, 0.86, 0.86)
@export var default_bg: Color = Color(0.04, 0.04, 0.04)

var bridge: TerminalBridgeClient = null

var _font: Font
var _cell_w: float = 12.0
var _cell_h: float = 20.0
var _baseline: float = 14.0

var _cols: int = 400
var _rows: int = 100
var _cursor: Vector2i = Vector2i(0, 0)
var _cells: Array = []


func _ready() -> void:
	focus_mode = FOCUS_ALL
	mouse_filter = MOUSE_FILTER_STOP
	grab_focus()

	var bridge_node: Node = get_node_or_null("Bridge")
	if bridge_node == null:
		push_error("Bridge node is missing from the scene")
	else:
		bridge = bridge_node as TerminalBridgeClient
		if bridge == null:
			push_error("Bridge node script is not TerminalBridgeClient (or failed to load)")

	_load_font()
	_recompute_metrics()

	if bridge != null:
		bridge.frame_received.connect(_on_frame_received)
		bridge.bridge_connected.connect(_on_bridge_connected)

	_send_current_size()


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		_send_current_size()
		queue_redraw()


func _on_bridge_connected() -> void:
	_send_current_size()


func _load_font() -> void:
	if ResourceLoader.exists(nerd_font_path):
		_font = load(nerd_font_path)
	else:
		_font = ThemeDB.fallback_font


func _recompute_metrics() -> void:
	var sample: Vector2 = _font.get_string_size("M", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
	_cell_w = max(1.0, ceil(sample.x))
	var ascent: float = _font.get_ascent(font_size)
	var descent: float = _font.get_descent(font_size)
	_cell_h = max(1.0, ceil(ascent + descent))
	_baseline = ascent


func _send_current_size() -> void:
	if bridge == null:
		return
	var cols: int = max(3, int(floor(size.x / _cell_w)))
	var rows: int = max(1, int(floor(size.y / _cell_h)))
	bridge.send_resize(cols, rows)


func _on_frame_received(frame: Dictionary) -> void:
	_cols = int(frame.get("cols", _cols))
	_rows = int(frame.get("rows", _rows))

	var cursor_data: Array = frame.get("cursor", [0, 0])
	if cursor_data.size() >= 2:
		_cursor = Vector2i(int(cursor_data[0]), int(cursor_data[1]))

	_cells = frame.get("cells", [])
	queue_redraw()


func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), default_bg, true)

	if _cells.is_empty():
		draw_string(_font, Vector2(8, _baseline + 8), "Waiting for bridge...", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, default_fg)
		return

	var draw_rows: int = min(_rows, _cells.size())
	for y in range(draw_rows):
		var row: Array = _cells[y]
		var draw_cols: int = min(_cols, row.size())
		for x in range(draw_cols):
			var cell: Array = row[x]
			if cell.size() < 8:
				continue

			var ch: String = str(cell[0])
			if ch.is_empty():
				ch = " "

			var fg: Color = Color8(int(cell[1]), int(cell[2]), int(cell[3]))
			var bg: Color = Color8(int(cell[4]), int(cell[5]), int(cell[6]))

			var px: float = x * _cell_w
			var py: float = y * _cell_h
			draw_rect(Rect2(px, py, _cell_w, _cell_h), bg, true)
			draw_string(_font, Vector2(px, py + _baseline), ch, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, fg)

	# Cursor overlay
	if _cursor.y >= 0 and _cursor.y < _rows and _cursor.x >= 0 and _cursor.x < _cols:
		var cpx: float = _cursor.x * _cell_w
		var cpy: float = _cursor.y * _cell_h
		draw_rect(Rect2(cpx, cpy + _cell_h - 2.0, _cell_w, 2.0), Color(1, 1, 1, 0.85), true)


func _gui_input(event: InputEvent) -> void:
	if event is InputEventKey:
		var key_event: InputEventKey = event
		if not key_event.pressed:
			return

		var bytes: PackedByteArray = _key_event_to_bytes(key_event)
		if bridge != null and bytes.size() > 0:
			bridge.send_bytes(bytes)
			accept_event()


func _key_event_to_bytes(event: InputEventKey) -> PackedByteArray:
	if event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER:
		return "\n".to_utf8_buffer()
	if event.keycode == KEY_BACKSPACE:
		return PackedByteArray([127])
	if event.keycode == KEY_TAB:
		return "\t".to_utf8_buffer()
	if event.keycode == KEY_ESCAPE:
		return PackedByteArray([27])

	if event.keycode == KEY_UP:
		return "\u001b[A".to_utf8_buffer()
	if event.keycode == KEY_DOWN:
		return "\u001b[B".to_utf8_buffer()
	if event.keycode == KEY_RIGHT:
		return "\u001b[C".to_utf8_buffer()
	if event.keycode == KEY_LEFT:
		return "\u001b[D".to_utf8_buffer()
	if event.keycode == KEY_HOME:
		return "\u001b[H".to_utf8_buffer()
	if event.keycode == KEY_END:
		return "\u001b[F".to_utf8_buffer()
	if event.keycode == KEY_DELETE:
		return "\u001b[3~".to_utf8_buffer()
	if event.keycode == KEY_PAGEUP:
		return "\u001b[5~".to_utf8_buffer()
	if event.keycode == KEY_PAGEDOWN:
		return "\u001b[6~".to_utf8_buffer()

	if event.ctrl_pressed and event.unicode > 0:
		var cp: int = event.unicode
		if cp >= 64 and cp <= 95:
			return PackedByteArray([cp - 64])
		if cp >= 97 and cp <= 122:
			return PackedByteArray([cp - 96])

	if event.alt_pressed and event.unicode > 0:
		var alt_bytes: PackedByteArray = PackedByteArray([27])
		alt_bytes.append_array(char(event.unicode).to_utf8_buffer())
		return alt_bytes

	if event.unicode > 0 and not event.ctrl_pressed and not event.meta_pressed:
		return char(event.unicode).to_utf8_buffer()

	return PackedByteArray()
