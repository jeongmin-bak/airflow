#!/bin/bash

set -u
set -o pipefail

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error_exit() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
    exit 1
}

# 환경변수 / 설정
API_AGENT_NAME="api_collector-3.3.2.jar"
AGENT_FILE_PATH="/Users/bagjeongmin/Desktop/SpringBoot/api_collector/target"
AGENT_FULL_PATH="${AGENT_FILE_PATH}/${API_AGENT_NAME}"

# 필수 명령어 체크
command -v java >/dev/null 2>&1 || error_exit "java is not installed."

# 파라미터 체크
if [ $# -lt 2 ]; then
    error_exit "Usage: $0 API_META_ID BSDT"
fi

# 파라미터 설정
API_META_ID="$1"
BSDT="$2"

# jar 파일 체크
if [ ! -f "${AGENT_FULL_PATH}" ]; then
    error_exit "Jar file not found: ${AGENT_FULL_PATH}"
fi

# 실행 로그
log "API_AGENT_NAME=${API_AGENT_NAME}"
log "AGENT_FILE_PATH=${AGENT_FILE_PATH}"
log "API_META_ID=${API_META_ID}, BSDT=${BSDT}"

# Agent 실행
log "Running: java -jar \"${AGENT_FULL_PATH}\" \"${API_META_ID}\" \"${BSDT}\""

java -jar "${AGENT_FULL_PATH}" "${API_META_ID}" "${BSDT}"
JAVA_EXIT_CODE=$?

if [ "${JAVA_EXIT_CODE}" -ne 0 ]; then
    error_exit "Jar execution failed with exit code ${JAVA_EXIT_CODE}"
fi

log "Jar execution completed successfully."
exit 0



