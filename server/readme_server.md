This folder contains several scripts that are useful to run Notifier on a
server (from a Jupyter Notebook) while controlling it from a local machine. 

* `ssh.sh`:             ssh into remote machine (e.g. an oracle cloud server) 
* `open_tunnel.sh` :    open a tunnel to remote, see below. 
* `launch_jupyter.sh` : run notifier.ipynb via jupyter notebook on the server  

Instructions for running code on server via jupyter on desktop: 
1. Run launch_jupyter.sh on server (from project root). This displays a url containing a token.
1. Run open_tunnel.sh on the local machine
3. Paste the url from step 1. into a browser on the local machine, replacing 8086 by 8081
