#!/usr/bin/env bash
# =============================================================================
# setup.sh — Bootstrap the data platform on Ubuntu
#
# Run this script once after cloning the repository on the Linux server:
#   chmod +x setup.sh
#   ./setup.sh
#
# What it does:
#   1. Detects or installs Python (>= 3.10), pip, git
#   2. Creates a Python virtual environment
#   3. Installs all Python dependencies
#   4. Installs DuckDB extensions (azure, delta)
#   5. Installs dbt packages
#   6. Creates required data directories
#   7. Copies .env.example → .env (if .env does not already exist)
#   8. Copies dagster.yaml to DAGSTER_HOME
#   9. Installs and enables systemd services
#
# After running this script:
#   - Edit /opt/my_data_platform/.env and fill in all required values
#   - Run: sudo systemctl start dagster-webserver dagster-daemon
# =============================================================================

set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/.venv"
DATA_DIR="$APP_DIR/data"
DAGSTER_HOME_DIR="$APP_DIR/dagster_home"

# ── Colour helpers ────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warning() { echo -e "${YELLOW}[WARN]${NC}  $*"; }

# ── 1. System packages ────────────────────────────────────────────────────────
# Detect a suitable Python (>= 3.10) already on the system
PYTHON_BIN=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" &>/dev/null; then
        if "$candidate" -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" 2>/dev/null; then
            version=$("$candidate" -c "import sys; print('.'.join(map(str,sys.version_info[:3])))")
            info "Found suitable Python: $candidate ($version)"
            PYTHON_BIN="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    info "No suitable Python found — installing python3.12 via apt..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        python3.12 \
        python3.12-venv \
        python3.12-dev
    PYTHON_BIN="python3.12"
fi

# Install pip, git, curl only if missing
APT_MISSING=()
command -v git  &>/dev/null || APT_MISSING+=(git)
command -v curl &>/dev/null || APT_MISSING+=(curl)
command -v pip3 &>/dev/null || APT_MISSING+=(python3-pip)

if [ ${#APT_MISSING[@]} -gt 0 ]; then
    info "Installing missing system packages: ${APT_MISSING[*]}"
    sudo apt-get update -qq
    sudo apt-get install -y -qq "${APT_MISSING[@]}"
else
    info "git, curl, and pip already installed — skipping apt."
fi

# ── 2. Virtual environment ────────────────────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    info "Creating Python virtual environment at $VENV_DIR ..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    info "Virtual environment already exists, skipping creation."
fi

# Activate venv for remainder of script
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# ── 3. Python dependencies ────────────────────────────────────────────────────
info "Installing Python dependencies (this may take a few minutes)..."
pip install --quiet --upgrade pip
pip install --quiet -e "$APP_DIR"

# ── 4. DuckDB extensions ──────────────────────────────────────────────────────
info "Installing DuckDB extensions (azure, delta)..."
python "$APP_DIR/scripts/install_duckdb_extensions.py"

# ── 5. dbt packages ───────────────────────────────────────────────────────────
info "Installing dbt packages..."
cd "$APP_DIR/dbt_project"
"$VENV_DIR/bin/dbt" deps --profiles-dir . --project-dir .
cd "$APP_DIR"

# ── 6. Data directories ───────────────────────────────────────────────────────
info "Creating data directories..."
mkdir -p "$DATA_DIR/csv"
mkdir -p "$DAGSTER_HOME_DIR"

# ── 7. Environment file ───────────────────────────────────────────────────────
if [ ! -f "$APP_DIR/.env" ]; then
    info "Copying .env.example → .env"
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    # Set the paths that we already know
    sed -i "s|DAGSTER_HOME=.*|DAGSTER_HOME=$DAGSTER_HOME_DIR|" "$APP_DIR/.env"
    sed -i "s|DUCKDB_PATH=.*|DUCKDB_PATH=$DATA_DIR/platform.duckdb|" "$APP_DIR/.env"
    warning "Please edit $APP_DIR/.env and fill in all credentials before starting the services."
else
    info ".env already exists, skipping."
fi

# ── 8. Dagster home configuration ─────────────────────────────────────────────
info "Copying dagster.yaml to DAGSTER_HOME..."
cp "$APP_DIR/dagster.yaml" "$DAGSTER_HOME_DIR/dagster.yaml"

# ── 9. systemd services ───────────────────────────────────────────────────────
info "Installing systemd service files..."

# Replace the placeholder user with the current user in the service files
CURRENT_USER="$(whoami)"
for SERVICE in dagster-webserver dagster-daemon; do
    SERVICE_FILE="$APP_DIR/systemd/$SERVICE.service"
    DEST="/etc/systemd/system/$SERVICE.service"
    # Replace hardcoded paths and user in the service file
    sudo sed \
        -e "s|User=ubuntu|User=$CURRENT_USER|g" \
        -e "s|Group=ubuntu|Group=$CURRENT_USER|g" \
        -e "s|/opt/my_data_platform|$APP_DIR|g" \
        "$SERVICE_FILE" | sudo tee "$DEST" > /dev/null
    info "  Installed $DEST"
done

sudo systemctl daemon-reload
sudo systemctl enable dagster-webserver dagster-daemon

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
info "Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. Edit your credentials:  nano $APP_DIR/.env"
echo "  2. Start the services:     sudo systemctl start dagster-webserver dagster-daemon"
echo "  3. Check service status:   sudo systemctl status dagster-webserver dagster-daemon"
echo "  4. View logs:              journalctl -u dagster-webserver -f"
echo "  5. Open Dagster UI:        http://localhost:3000  (or use SSH tunnel)"
echo ""
echo "  SSH tunnel from your local machine to access the Dagster UI:"
echo "    ssh -L 3000:localhost:3000 <your-server-user>@<your-server-ip>"
echo ""
