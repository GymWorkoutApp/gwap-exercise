#!/bin/sh

#   Author: Guilherme Dalmarco
#   Email : dalmarco.gd@gmail.com

#   This script is used to start applications on docker
#   You need environments variable GWA_ENVIRONMENT set for production/homolog


#   By default (without GWA_ENVIRONMENT set) we run as "dev"
if [ -z "${GWA_ENVIRONMENT}" ]
then
	GWA_ENVIRONMENT="hml"
fi

# DOCKER ENTRYPOINT GIVE US THE EXECUTION FILE AS PARAMETER
APP="gunicorn -c ${1} ${2}:app"


#
# PRODUCTION ENVIRONMENT RULES
#
f_run_prd() {
    for DOTENV_VAR in $(cat environments/prd.env)
    do
        export ${DOTENV_VAR}
        echo "${DOTENV_VAR}"
    done

    export PYTHONPATH=$(pwd)
    make db_upgrade

    # RUN APP
    echo "RUNNING APP WITH:"
    echo "${APP}"
    ${APP}
}

#
# HOMOLOG ENVIRONMENT RULES
#
f_run_hml() {
    for DOTENV_VAR in $(cat environments/hml.env)
    do
        export ${DOTENV_VAR}
        echo "${DOTENV_VAR}"
    done

    export PYTHONPATH=$(pwd)
    make db_upgrade

    # RUN APP
    echo "RUNNING APP WITH:"
    echo "${APP}"
    ${APP}

}

#
# LOCAL TESTES AND DEVELOPERS: YOU CAN CHANGE THIS FUNCTION AS YOU WISH
#
f_run_local() {
    # AWS ESS Parameter Store
    echo -ne "\n#\n# DOCKER INIT SCRIPT: RUNNING ${GWA_ENVIRONMENT}.${GWA_ENVIRONMENT} \n#\n"

    for DOTENV_VAR in $(cat environments/hml.env)
    do
        #JAR_PARAMS="${JAR_PARAMS} -D${DOTENV_VAR} "
        export ${DOTENV_VAR}
    done

    export PYTHONPATH=$(pwd)
    make db_upgrade

    # RUN APP
    echo "RUNNING APP WITH:"
    echo "${APP}"
    ${APP}

}


#
# DO NOT CHANGE THE CODE BELOW
#
echo -ne "\n\n##\n##\tRUNNING WITH GWA_ENVIRONMENT=\"${GWA_ENVIRONMENT}\"\n##\n\n"
if [ "${GWA_ENVIRONMENT}" == "prd" ]
then
	f_run_prd
fi

if [ "${GWA_ENVIRONMENT}" == "hml" ]
then
    f_run_hml
fi

if [ "${GWA_ENVIRONMENT}" == "dev" ]
then
	f_run_local
fi
