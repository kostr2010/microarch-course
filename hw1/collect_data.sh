#!/bin/bash

set -Eeu -o pipefail -o posix
shopt -s nullglob inherit_errexit

ROOT="$(git rev-parse --show-toplevel)"
CHAMPSIM_DIR="${ROOT}/champ-sim"
TRACES_DIR="${ROOT}/traces"
HW_DIR="${ROOT}/hw1"
OUTPUT_DIR="${HW_DIR}/out/"

log() {
    echo "[LOG]: " "$@"
}

checkout_cur_hw() {
    local BRANCH

    BRANCH="hw1"

    cd "${CHAMPSIM_DIR}"
    git checkout "${BRANCH}"
}

get_config_json() {
    echo "${HW_DIR}/config_${1:?}.json"
}

clear_file() {
    true >"${1:?}"
}

clear_dir() {
    mkdir -p "${1:?}"
    rm -rf "${1:?}"/*
    rm -rf "${1:?}"/.[a-zA-Z0-9]*
}

extract_file_name() {
    local FILE

    FILE="${1:?}"
    FILE="${FILE##*/}"
    FILE="${FILE%.*}"

    echo "${FILE}"
}

rebuild_champsim() {
    local PREDICTOR

    PREDICTOR="${1:?}"

    log "building champsim for ${PREDICTOR}"

    checkout_cur_hw

    rm -rf "${CHAMPSIM_DIR}/.csconfig"
    rm -rf "${CHAMPSIM_DIR}/.bin"
    rm -rf "${CHAMPSIM_DIR}/_configuration.mk"
    rm -rf "${CHAMPSIM_DIR}/config/__pycache__"

    "${CHAMPSIM_DIR}/config.sh" "$(get_config_json "${PREDICTOR}")"

    cd "${CHAMPSIM_DIR}"
    make >/dev/null

    log "built champsim for ${PREDICTOR}"
}

process_trace() {
    local TRACE
    local OUT_DIR
    local TRACE_NAME
    local TRACE_OUT_FILE
    local CHAMPSIM_EXE
    local N_WARMUP
    local N_SIMULATION

    TRACE="${1:?}"
    OUT_DIR="${2:?}"
    TRACE_NAME=$(extract_file_name "${TRACE}")
    TRACE_OUT_FILE="${OUT_DIR}/${TRACE_NAME}.out"
    CHAMPSIM_EXE="${CHAMPSIM_DIR}/bin/champsim"
    N_WARMUP=10000000
    N_SIMULATION=50000000

    log "processing ${TRACE_NAME}..."

    clear_file "${TRACE_OUT_FILE}"

    "${CHAMPSIM_EXE}" --warmup_instructions "${N_WARMUP}" --simulation_instructions "${N_SIMULATION}" --log "${OUTPUT_DIR}/${TRACE_NAME}.log" "${TRACE}" &>"${TRACE_OUT_FILE}"

    log "processed ${TRACE_NAME}"
}

extract_metrics() {
    local OUT
    local REGEX_EXTRACT_CONDITIONAL_MPKI
    local CONDITIONAL_MPKI
    local TRACE_NAME

    OUT="${1:?}"

    REGEX_EXTRACT_CONDITIONAL_MPKI="^BRANCH_CONDITIONAL: (.*)$"
    CONDITIONAL_MPKI=$(grep -oP "${REGEX_EXTRACT_CONDITIONAL_MPKI}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_CONDITIONAL_MPKI}@\1@")

    TRACE_NAME=$(extract_file_name "${OUT}")

    echo "${TRACE_NAME},${CONDITIONAL_MPKI}"
}

run_predictor() {
    local PREDICTOR
    local PREDICTOR_OUT_DIR
    local OUT_CSV

    PREDICTOR="${1:?}"
    PREDICTOR_OUT_DIR="${OUTPUT_DIR}/${PREDICTOR}"

    clear_dir "${PREDICTOR_OUT_DIR}"

    rebuild_champsim "${PREDICTOR}"

    for TRACE in "${TRACES_DIR}"/*.xz; do
        process_trace "${TRACE}" "${PREDICTOR_OUT_DIR}" &
    done

    wait $(jobs -p)

    OUT_CSV="${PREDICTOR_OUT_DIR}/out.csv"
    clear_file "${OUT_CSV}"

    for OUT in "${PREDICTOR_OUT_DIR}"/*.out; do
        extract_metrics "${OUT}" >>"${OUT_CSV}"

        log "extracted IPC from ${OUT}"
    done
}

collect_data() {
    local PREDICTORS=("oracle")

    for PREDICTOR in "${PREDICTORS[@]}"; do
        run_predictor "${PREDICTOR}"

        log "collected data for ${PREDICTOR} predictor"
    done
}

collect_data
