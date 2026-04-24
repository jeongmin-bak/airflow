#!/bin/bash

API_AGENT_NAME="api_collector-3.3.2.jar"

# 필수 환경 변수 체크
if [ -z "${DIMDM_API_URL}" ]; then
    echo "Error: DIMDM_API_URL is not set."
    echo "Please set the environment variable using"
    exit 1
fi

# API URL 생성
API_RUN_URL="${DIMDM_API_URL}/dp/external/ezRun"
API_STATUS_URL="${DIMDM_API_URL}/dp/external/ezStatus"
API_KILL_URL="${DIMDM_API_URL}/dp/external/ezKill"

# 파라미터 설정
API_META_ID="$1"
BSDT="$2"
CD_GRP_ID="$3"
CD_BAS="$4"
CD_KEY="$5"

# JSON 데이터 구성
PARAM="{\"API_META_ID\":\"${API_META_ID}\", \"BSDT\":\"${BSDT}\", \"CD_GRP_ID\":\"${CD_GRP_ID}\", \"CD_BAS\":\"${CD_BAS}\"}"

echo "Sending JSON: $PARAM"

# ezRun 실행
echo "Executing ezRun..."
RESPONSE=$(curl -s -X POST "${API_RUN_URL}" \
  -H "Content-Type: application/json" \
  -d "${PARAM}")

# JSON에서 JB_ID 추출
JB_ID=$(echo "${RESPONSE}" | jq -r '.JB_ID')

echo "ezRun executed. JB_ID: ${JB_ID}"

# 상태 체크 설정
JOB_STATUS="00"
RETRY_INTERVAL=3

echo "Job Status 조회 시작..."

while true; do
  RESPONSE=$(curl -s -X POST "${API_STATUS_URL}" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "jbId=${JB_ID}")

  JOB_STATUS=$(echo "${RESPONSE}" | jq -r '.STATUS')
  ERR_LOG=$(echo "${RESPONSE}" | jq -r '.ERR_LOG')

  echo "Current Job Status: ${JOB_STATUS}"

  if [ "${JOB_STATUS}" != "00" ] && [ "${JOB_STATUS}" != "01" ]; then
    if [ "${JOB_STATUS}" == "10" ]; then
      echo "Job Finished"
      echo "JOB_STATUS=${JOB_STATUS}"
      exit 0
    else
      echo "Error occurred"
      echo "JOB_STATUS=${JOB_STATUS}"
      echo "ERR_LOG=${ERR_LOG}"
      exit 1
    fi
  fi

  sleep ${RETRY_INTERVAL}
done