PORTAL_FWNAME="$(id -un | tr '[A-Z]' '[a-z]')-server"
PORTAL_FWFILE="/home/gridsan/portal-url-fw/${PORTAL_FWNAME}"
echo "Portal URL is: https://${PORTAL_FWNAME}.fn.txe1-portal.mit.edu/"
echo "http://$(hostname -s):${SLURM_STEP_RESV_PORTS}/" > $PORTAL_FWFILE
chmod u+x ${PORTAL_FWFILE}
server_root=$U/server
nodemon $server_root/server.js --port ${SLURM_STEP_RESV_PORTS} --exp /home/gridsan/zxyan/flow/all_results/20_11_06_factorized_value_function_g1x1_lambda0/small_flow800/sf800_fuel0_rmsprop_vwarm20_4
