# read address of remote from file 
scriptdir=$(dirname "$0")
address_file=$scriptdir"/remote_address.txt"
remote_address=$(cat $address_file) 

ssh -v -i $scriptdir"/ssh.key" $remote_address
