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

# 필수 명령어 체크
command -v curl >/dev/null 2>&1 || error_exit "curl is not installed."
command -v jq >/dev/null 2>&1 || error_exit "jq is not installed."

# 환경변수 
API_AGENT_NAME="api_collector-3.3.2.jar"

# 파라미터 체크
if [ $# -lt 2 ]; then
    error_exit "Usage: $0 API_META_ID BSDT"
fi

# 파라미터 설정
API_META_ID="$1"
BSDT="$2"

# 실행 옵션
RETRY_INTERVAL="${RETRY_INTERVAL:-3}"
MAX_RETRY="${MAX_RETRY:-200}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-10}"
MAX_TIME="${MAX_TIME:-30}"
ENABLE_KILL_ON_TIMEOUT="${ENABLE_KILL_ON_TIMEOUT:-Y}"

log "API_AGENT_NAME=${API_AGENT_NAME}"
log "API_META_ID=${API_META_ID}, BSDT=${BSDT}"


# JSON 데이터 구성
PARAM="{\"API_META_ID\":\"${API_META_ID}\", \"BSDT\":\"${BSDT}\"}"
echo "Sending JSON: $PARAM"

# Agent 실행 
log "Running: java -jar ${API_AGENT_NAME} ${API_META_ID} ${BSDT}"
java -jar "${API_AGENT_NAME}" "${API_META_ID}" "${BSDT}"



