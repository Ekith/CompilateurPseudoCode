#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

display_info() {
    if [[ " $@ " =~ " -v " ]]; then
        echo "$1"
    fi
}




# Check if the directory venv is provided
if [ -e "$SCRIPT_DIR/.venv" ]; then
    display_info "Virtual environment already exists. Activating..." $@
    source $SCRIPT_DIR/.venv/bin/activate
    display_info "Virtual environment activated." $@
else
    display_info "Creating a new virtual environment..." $@
    python3 -m venv $SCRIPT_DIR/.venv
    display_info "Virtual environment created at $SCRIPT_DIR/.venv" $@
    display_info "" $@
    display_info "Activating the virtual environment..." $@
    source $SCRIPT_DIR/.venv/bin/activate
    display_info "Virtual environment activated." $@
    display_info "" $@
    display_info "Installing required packages..." $@
    pip install -r $SCRIPT_DIR/requirements.txt
    display_info "Required packages installed." $@
fi


MAIN_PATH="$SCRIPT_DIR/main.py"


python3 $MAIN_PATH $@
