#!/usr/bin/env bash

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

act_file="${script_dir}/venv/bin/activate"
script="${script_dir}/ruv_downloader.py"

if [ -f $act_file ];then
	source $act_file
else
	echo "can't find venv"
	exit
fi

$script $@
