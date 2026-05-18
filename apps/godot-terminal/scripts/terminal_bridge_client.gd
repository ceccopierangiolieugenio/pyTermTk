extends Node
class_name TerminalBridgeClient

signal bridge_connected
signal bridge_disconnected
signal frame_received(frame: Dictionary)

@export var host: String = "127.0.0.1"
@export var port: int = 18081

var _tcp: StreamPeerTCP = StreamPeerTCP.new()
var _rx_buffer: String = ""
var _last_status: int = StreamPeerTCP.STATUS_NONE


func _ready() -> void:
	connect_to_bridge()
	set_process(true)


func connect_to_bridge() -> void:
	if _tcp.get_status() != StreamPeerTCP.STATUS_NONE:
		_tcp.disconnect_from_host()

	var err: int = _tcp.connect_to_host(host, port)
	if err != OK:
		push_error("Bridge connect failed: %s" % err)


func _process(_delta: float) -> void:
	_tcp.poll()
	var status: int = _tcp.get_status()

	if status != _last_status:
		if status == StreamPeerTCP.STATUS_CONNECTED:
			bridge_connected.emit()
		elif _last_status == StreamPeerTCP.STATUS_CONNECTED:
			bridge_disconnected.emit()
		_last_status = status

	if status == StreamPeerTCP.STATUS_CONNECTED:
		_read_available()


func _read_available() -> void:
	while _tcp.get_available_bytes() > 0:
		var chunk_size: int = min(_tcp.get_available_bytes(), 65536)
		var read_result: Array = _tcp.get_data(chunk_size)
		var err: int = read_result[0]
		var data: PackedByteArray = read_result[1]
		if err != OK:
			return

		_rx_buffer += data.get_string_from_utf8()
		_process_lines()


func _process_lines() -> void:
	while true:
		var newline_index: int = _rx_buffer.find("\n")
		if newline_index < 0:
			return

		var line: String = _rx_buffer.substr(0, newline_index).strip_edges()
		_rx_buffer = _rx_buffer.substr(newline_index + 1)
		if line.is_empty():
			continue

		var parsed: Variant = JSON.parse_string(line)
		if parsed is Dictionary:
			var message: Dictionary = parsed
			if message.get("type", "") == "frame":
				frame_received.emit(message)


func send_resize(cols: int, rows: int) -> void:
	send_json({"type": "resize", "cols": cols, "rows": rows})


func send_text(text: String) -> void:
	send_json({"type": "text", "text": text})


func send_bytes(data: PackedByteArray) -> void:
	send_json({"type": "input", "data": Marshalls.raw_to_base64(data)})


func send_ping() -> void:
	send_json({"type": "ping"})


func send_json(message: Dictionary) -> void:
	if _tcp.get_status() != StreamPeerTCP.STATUS_CONNECTED:
		return

	var payload: String = JSON.stringify(message) + "\n"
	_tcp.put_data(payload.to_utf8_buffer())
