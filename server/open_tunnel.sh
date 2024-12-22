# read address of remote from file 
scriptdir=$(dirname "$0")
address_file=$scriptdir"/remote_address.txt"
remote_address=$(cat $address_file) 

ssh -i $scriptdir'/ssh.key' -N -L 8081:localhost:8086 $remote_address 
