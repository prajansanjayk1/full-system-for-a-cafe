#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON:-python3}"
venv_dir="${VENV_DIR:-.venv}"

if [ ! -d "$venv_dir" ]; then
  "$python_bin" -m venv "$venv_dir"
fi

# shellcheck disable=SC1091
source "$venv_dir/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.local.example .env
fi

export DJANGO_SETTINGS_MODULE=config.settings.local
python manage.py migrate --noinput
python manage.py seed_demo

cat <<MSG

Local setup complete.
Run the app with:
  source $venv_dir/bin/activate
  ./scripts/run_local.sh

Open: http://localhost:8000/healthz/
MSG
