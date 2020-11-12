PORTAL_FWNAME="$(id -un | tr '[A-Z]' '[a-z]')-server"
PORTAL_FWFILE="/home/gridsan/portal-url-fw/${PORTAL_FWNAME}"
echo "Portal URL is: https://${PORTAL_FWNAME}.fn.txe1-portal.mit.edu/"
echo "http://$(hostname -s):${SLURM_STEP_RESV_PORTS}/" > $PORTAL_FWFILE
chmod u+x ${PORTAL_FWFILE}
server_root=$U/server
node $server_root/server.js --port ${SLURM_STEP_RESV_PORTS}