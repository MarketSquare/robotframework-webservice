#!/bin/sh

if [ -n "${VARIABLE_FILES}" ]; then
  variablefiles="--variablefiles ${VARIABLE_FILES}"
else
  variablefiles=""
fi

exec python -m RobotFrameworkService.main --port "${PORT}" --taskfolder "${SUITE_FOLDER}" ${variablefiles}