"""闲鱼AI客服 - 可视化仪表板"""

from flask import Flask, jsonify, render_template, request
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

# 由 main.py 注入
_context_manager = None
_bot_status = {"running": False, "start_time": None, "ws_connected": False}


def init_dashboard(context_manager):
    """注入上下文管理器"""
    global _context_manager
    _context_manager = context_manager


def get_bot_status():
    """获取机器人状态"""
    return _bot_status

def set_bot_status(**kwargs):
    """更新机器人状态"""
    _bot_status.update(kwargs)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def api_stats():
    if not _context_manager:
        return jsonify({"error": "not initialized"}), 500
    stats = _context_manager.get_dashboard_stats()
    import time
    runtime = int(time.time() - _bot_status["start_time"]) if _bot_status["start_time"] else 0
    stats.update({
        "running": _bot_status["running"],
        "runtime": runtime,
        "ws_connected": _bot_status["ws_connected"]
    })
    return jsonify(stats)


@app.route('/api/chats')
def api_chats():
    if not _context_manager:
        return jsonify([])
    return jsonify(_context_manager.get_chat_list())


@app.route('/api/chat/<chat_id>')
def api_chat_detail(chat_id):
    if not _context_manager:
        return jsonify([])
    return jsonify(_context_manager.get_chat_detail(chat_id))


@app.route('/api/intents')
def api_intents():
    if not _context_manager:
        return jsonify({})
    return jsonify(_context_manager.get_intent_stats())


def run_dashboard(host='0.0.0.0', port=8899):
    """启动仪表板服务器"""
    app.run(host=host, port=port, debug=False, use_reloader=False)


@app.route("/api/account")
def api_account():
    """获取当前账号信息"""
    return jsonify({
        "user_id": _bot_status.get("user_id", ""),
        "nickname": _bot_status.get("nickname", ""),
        "ws_connected": _bot_status.get("ws_connected", False)
    })


@app.route("/api/switch_account", methods=["POST"])
def api_switch_account():
    """切换账号 - 接收新Cookie并触发重连"""
    data = request.get_json()
    new_cookies = data.get("cookies", "").strip()
    if not new_cookies:
        return jsonify({"ok": False, "error": "Cookie不能为空"}), 400
    # 保存到.env
    import re
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            env_content = f.read()
        env_content = re.sub(r"COOKIES_STR=.*", f"COOKIES_STR={new_cookies}", env_content)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        logger.info("Cookie已更新，触发重连...")
        _bot_status["reconnect"] = True
        _bot_status["new_cookies"] = new_cookies
        return jsonify({"ok": True, "message": "Cookie已更新，正在重连..."})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
