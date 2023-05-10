#!/bin/bash

set -Eeu -o pipefail -o posix
shopt -s nullglob inherit_errexit

ROOT="$(git rev-parse --show-toplevel)"
CHAMPSIM_DIR="${ROOT}/champ-sim"
TRACES_DIR="${ROOT}/traces"
HW_DIR="${ROOT}/hw2"

log() {
    echo "[LOG]: " "$@"
}

checkout_cur_hw() {
    local BRANCH

    BRANCH="hw2"

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
    local POLICY

    POLICY="${1}"

    log "building champsim for ${POLICY}"

    checkout_cur_hw

    rm -rf "${CHAMPSIM_DIR}/.csconfig"
    rm -rf "${CHAMPSIM_DIR}/.bin"
    rm -rf "${CHAMPSIM_DIR}/_configuration.mk"
    rm -rf "${CHAMPSIM_DIR}/config/__pycache__"

    "${CHAMPSIM_DIR}/config.sh" "$(get_config_json "${POLICY}")"

    cd "${CHAMPSIM_DIR}"
    make >/dev/null

    log "built champsim for ${POLICY}"
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

    "${CHAMPSIM_EXE}" --warmup_instructions "${N_WARMUP}" --simulation_instructions "${N_SIMULATION}" "${TRACE}" &>"${TRACE_OUT_FILE}"

    log "processed ${TRACE_NAME}"
}

extract_metrics() {
    local OUT
    local REGEX_EXTRACT_IPC
    local IPC
    local REGEX_EXTRACT_LLC_ACCESS
    local LLC_ACCESS
    local REGEX_EXTRACT_L2_ACCESS
    local L2_ACCESS
    local REGEX_EXTRACT_L1D_ACCESS
    local L1D_ACCESS
    local REGEX_EXTRACT_STLB_ACCESS
    local STLB_ACCESS
    local REGEX_EXTRACT_DTLB_ACCESS
    local DTLB_ACCESS
    local TRACE_NAME

    OUT="${1:?}"

    REGEX_EXTRACT_IPC=".*CPU 0 cumulative IPC: (.*) instructions:.*"
    IPC=$(grep -oP "${REGEX_EXTRACT_IPC}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_IPC}@\1@")

    REGEX_EXTRACT_L2_ACCESS="cpu0_L2C\s+TOTAL\s+ACCESS:\s+([0-9]+)\s+HIT:\s+([0-9]+)\s+MISS:\s+([0-9]+)"
    L2_ACCESS=$(grep -oP "${REGEX_EXTRACT_L2_ACCESS}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_L2_ACCESS}@\1,\2,\3@")

    REGEX_EXTRACT_L1D_ACCESS="cpu0_L1D\s+TOTAL\s+ACCESS:\s+([0-9]+)\s+HIT:\s+([0-9]+)\s+MISS:\s+([0-9]+)"
    L1D_ACCESS=$(grep -oP "${REGEX_EXTRACT_L1D_ACCESS}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_L1D_ACCESS}@\1,\2,\3@")

    REGEX_EXTRACT_STLB_ACCESS="cpu0_STLB\s+TOTAL\s+ACCESS:\s+([0-9]+)\s+HIT:\s+([0-9]+)\s+MISS:\s+([0-9]+)"
    STLB_ACCESS=$(grep -oP "${REGEX_EXTRACT_STLB_ACCESS}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_STLB_ACCESS}@\1,\2,\3@")

    REGEX_EXTRACT_DTLB_ACCESS="cpu0_DTLB\s+TOTAL\s+ACCESS:\s+([0-9]+)\s+HIT:\s+([0-9]+)\s+MISS:\s+([0-9]+)"
    DTLB_ACCESS=$(grep -oP "${REGEX_EXTRACT_DTLB_ACCESS}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_DTLB_ACCESS}@\1,\2,\3@")

    REGEX_EXTRACT_LLC_ACCESS="LLC\s+TOTAL\s+ACCESS:\s+([0-9]+)\s+HIT:\s+([0-9]+)\s+MISS:\s+([0-9]+)"
    LLC_ACCESS=$(grep -oP "${REGEX_EXTRACT_LLC_ACCESS}" <"${OUT}" | sed -re "s@${REGEX_EXTRACT_LLC_ACCESS}@\1,\2,\3@")

    TRACE_NAME=$(extract_file_name "${OUT}")

    echo "${TRACE_NAME},${IPC},${L2_ACCESS},${L1D_ACCESS},${STLB_ACCESS},${DTLB_ACCESS},${LLC_ACCESS}"
}

run_policy() {
    local POLICY
    local POLICY_OUT_DIR
    local OUT_CSV

    POLICY="${1:?}"
    POLICY_OUT_DIR="${HW_DIR}/out/${POLICY}"

    clear_dir "${POLICY_OUT_DIR}"

    rebuild_champsim "${POLICY}"

    for TRACE in "${TRACES_DIR}"/*.xz; do
        process_trace "${TRACE}" "${POLICY_OUT_DIR}" &
    done

    wait $(jobs -p)

    OUT_CSV="${POLICY_OUT_DIR}/out.csv"
    clear_file "${OUT_CSV}"

    for OUT in "${POLICY_OUT_DIR}"/*.out; do
        extract_metrics "${OUT}" >>"${OUT_CSV}"

        log "extracted data from ${OUT}"
    done
}

collect_data() {
    local POLICIES=("lfu" "lru")

    for POLICY in "${POLICIES[@]}"; do
        run_policy "${POLICY}"

        log "collected data for ${POLICY} policy"
    done
}

collect_data
