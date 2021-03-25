#!/usr/bin/env bash


python_ch_1="python3.6"
python_ch_2="python2.7"
ansible_ch_1="ansible2.9"
ansible_ch_2="ansible2.10"
repo='https://github.com/dell/python-vplex.git'
vplex_mg_server_dir='/var/log/VPlex/cli'
cmd_ver='--version'

root_dir=$( dirname "$PWD" )


error()
{
	echo "Error: ${*}"
}

info()
{
	echo "Info: ${*}"
}


get_install_method()
{

	methods="use_collections skip_collections quit"
	echo "Please choose the installation method: (recommended: 1)"
	select method in $methods;
	do
		case $method in
			"use_collections")
				method=1
				break
				;;
			"skip_collections")
				if [[ $ans_ver == *"2.9"* ]]; then
					method=2
				else
					error "copying modules is only supported for ansible 2.9"
					error "Selected Ansible version $ans_ver"
					exit 1
				fi
				break
				;;
			"quit")
				exit 1
				;;
			*) echo "invalid option $REPLY";;
		esac
	done
}


get_vplex_sdk()
{
	sdks="sdk_7.0 sdk_6.2 quit"
	echo "Please choose VPLEX python sdk: (recommended: 1)"
	select sdk in $sdks;
	do
		case $sdk in
			"sdk_7.0")
				sdk='7.0'
				break
				;;
			"sdk_6.2")
				sdk='6.2'
				break
				;;
			"quit")
				exit 1
				;;
			*) echo "invalid option $REPLY";;
		esac
	done
}


install_collections()
{
	info "Installing collections...."
	ansible-galaxy collection install "$root_dir/"dellemc-vplex-* -p "$env_path/collections" &>> /dev/null
}


verify_setup()
{
	echo
	info "Verifying if all modules are accessible..."

	if [ $method -eq 1 ];then
		verify_prefix='dellemc.vplex.'
		export ANSIBLE_COLLECTIONS_PATHS=$env_path/collections
	fi

	for each in "$root_dir/plugins/modules/"*; do
		each=$( basename "$each" .py )
		data=$(ansible-doc "$verify_prefix$each" | grep "EXAMPLES")
		if [ -z "$data" ];then
			echo "$each Not OK"
		else
			echo "$each OK"
		fi
	done
}


non_vplex_host()
{
	get_os()
	{
		os=$( grep '^NAME' /etc/os-release )
		if [[ $os == *Red* ]];then
			pkg_tool="yum"
		elif [[ $os == *SLES* ]];then
			pkg_tool="zypper"
		else
			pkg_tool="apt-get"
		fi
	}

	suggest_cmd()
	{

		info "Below commands can be used for same."
		echo "
	$pkg_tool install python2
	$pkg_tool install python3 python3-pip
		"
	}

	create_virtual_env()
	{
		if ! command -v virtualenv &> /dev/null
		then
			if ! command -v pip &> /dev/null
			then
				if ! command -v pip2 &> /dev/null
				then
					if ! command -v pip3 &> /dev/null
					then
						error "Please install virtualenv or install pip and try again."
						info 'pip install virtualenv'
						suggest_cmd
						exit
					else
						alias pip=pip3
					fi
				else
					alias pip=pip2
				fi
			fi

			info "Upgrading pip...."
			$python_path -m pip install --upgrade pip &>> /dev/null
			# shellcheck disable=SC2181
			if [ $? -ne 0 ]; then
				error "Upgrading pip failed. Please upgrade with appropriate access and try again."
				exit 1
			fi
			info "Installing virtualenv using pip"
			pip install virtualenv >> /dev/null
			if ! command -v virtualenv &> /dev/null
			then
				exit 1
			fi
		fi

		echo "Creating virtualenv $env_name from $python_path...."
		virtualenv -p "$python_path" "$env_path" >> /dev/null
		if [ ! -d "$env_path" ]; then
			error "Virtualenv did not get installed properly."
			info "Please try to uninstall pip and install again, or try using sudo privileged user."
			exit 1
		fi

	}


	get_virtualenv_name()
	{
		versions="$python_ch_1 $python_ch_2 quit"
		echo "please choose the python version:  (recommended: 1)"
		select  py_ver in $versions;
		do
			case $py_ver in
				"$python_ch_1")
					python_path=$( command -v "$py_ver" ) 2>> /dev/null
					if ! command -v "$py_ver" &>> /dev/null
					then
						error "Python $py_ver is not installed in system. Please install and try again."
						suggest_cmd
						exit
					else
						break
					fi
					;;
				"$python_ch_2")
					python_path=$( command -v "$py_ver" ) 2>> /dev/null
					if ! command -v "$py_ver" &>> /dev/null
					then
						error "Python $py_ver is not installed in system. Please install and try again."
						suggest_cmd
						exit
					else
						break
					fi
					;;
				"quit")
					exit 1
					;;
				*) error "Invalid option $REPLY";;
			esac
		done


		if [ "$REPLY" -eq 1 ]; then
			env_name='py3.6'
		elif [ "$REPLY" -eq 2 ]; then
			env_name='py2.7'
		fi

		versions="$ansible_ch_1 $ansible_ch_2 quit"
		echo "please choose the ansible version: (recommended: 1)"
		select ans_ver in $versions;
		do
			case $ans_ver in
				"$ansible_ch_1")
					env_name=$env_name'_ans2.9'
					ans_ver='2.9'
					break
					;;
				"$ansible_ch_2")
					env_name=$env_name'_ans2.10'
					ans_ver='2.10'
					break
					;;
				"quit")
					exit 1
					;;
				*) echo "Invalid option $REPLY";;
			esac
		done
	

	}

	install_packages()
	{
		
		mkdir -p "$HOME/Downloads"
		if [ ! -d "$HOME/Downloads/python-vplex" ]; then
			if ! command -v git &> /dev/null
			then
				error "Please install git and try again."
				echo "Below command can be used to install git 
		$pkg_tool install git
			OR
		clone python-vplex repo and place in $HOME/Downloads

		git clone $repo"
					echo
				exit 1
			fi
			info "Cloning vplexapi..."
			git -C "$HOME/Downloads/" clone -q $repo >> /dev/null
		fi

		if [ ! -d "$HOME/Downloads/python-vplex" ]; then
			error "Please upgrade git to latest version, and try again.
		OR
	clone python-vplex repo and place in $HOME/Downloads

	git clone $repo"
		echo
			exit 1
		fi

		activate_venv

		info "Installing required packages..."
		{
			pip install --upgrade pip
			pip install ansible==$ans_ver
			pip install certifi==2020.12.5
			pip install urllib3==1.26.3
			pip install six 
		} >> /dev/null

		# for python2.7 warning msg
		if [[ $py_ver == *"2.7"* ]]; then
			pip install cryptography==2.2.2 >> /dev/null
		fi

	}

	copy_modules()
	{
		activate_venv

		ver=$( ansible $cmd_ver | head -n 1 | cut -d' ' -f2 )
		# info Ansible version: $ver
		if [[ $ver == *"2.9"* ]]; then
			lib_path=$env_path/lib/$py_ver/site-packages/ansible

			info "Creating required directories in python library... "
			mkdir -p "$lib_path/modules/storage/dellemc/"
			mkdir -p "$lib_path/module_utils/storage/dell/"

			# copy modules, utils and doc fragments
			info "coping modules, utils and doc fragments in python library... "
			cp "$root_dir/plugins/modules/"* "$lib_path/modules/storage/dellemc/"
			cp "$root_dir/plugins/module_utils/storage/dell/"* "$lib_path/module_utils/storage/dell/"
			cp "$root_dir/plugins/doc_fragments/dellemc_vplex.py" "$lib_path/plugins/doc_fragments/"

			# update modules
			# for module in "$lib_path/modules/storage/dellemc/"*;
			# do
			# 	# module_path=$lib_path/modules/storage/dellemc/$module
			# 	# echo "Module: $module_path"
			# 	sed -i 's/dellemc.vplex.dellemc_vplex.vplex/dellemc_vplex.vplex/g' "$module_path"
			# 	sed -i 's/from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell/from ansible.module_utils.storage.dell import/g' "$module_path"
			# 	sed -i 's/import dellemc_ansible_vplex_utils as utils/dellemc_ansible_vplex_utils as utils/g' "$module_path"
			# done

			for module in "$lib_path/modules/storage/dellemc/"*;
			do
				sed -i 's/dellemc.vplex.dellemc_vplex.vplex/dellemc_vplex.vplex/g' "$module"
				sed -i 's/from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell/from ansible.module_utils.storage.dell import/g' "$module"
				sed -i 's/import dellemc_ansible_vplex_utils as utils/dellemc_ansible_vplex_utils as utils/g' "$module"
			done
		else
			# info Method: $method
			error "copying modules is only supported for ansible 2.9"
			error "Selected Ansible version $ans_ver"
			exit 1
		fi

	}

	activate_venv()
	{
		cwd=$PWD
		cd "$env_path"
		source bin/activate
		cd "$cwd"
	}


	get_os

	get_virtualenv_name	

	get_install_method
	get_vplex_sdk

	env_path=$HOME/.$env_name

	create_virtual_env

	install_packages

	activate_venv
	if [ $method -eq 1 ];then
		install_collections
	elif [ $method -eq 2 ];then
		copy_modules
	fi

	activate_venv
	verify_setup


	if [ $method -eq 1 ];then
		echo
		info "Installed collections can be found in $env_path/collections"
		info "Sample playbooks can be found in $root_dir/docs/"
	elif [ $method -eq 2 ];then
		echo
		info "Copied modules can be found in $env_path/ python library path."
		info "Sample playbooks can be found in $root_dir/docs/"
		info "In order to use sample roles, please copy $root_dir/roles to  $root_dir/docs/samples"
	fi

	echo
	info "Run below command to activate virtualenv and run playbooks..."
	echo "
	source $env_path/bin/activate"


	# info "Please export below paths"
	if [ $method -eq 1 ];then
		echo "\
	export ANSIBLE_COLLECTIONS_PATHS=$env_path/collections"
	fi

	python_path=''
	for each in "$HOME/Downloads/python-vplex/"vplexapi-*;do 
		if [[ $each == *$sdk* ]]; then
			python_path=$each
			break
		fi
	done
	if [[ $python_path == '' ]]; then
		echo
		error "VPLEX python sdk version $sdk is not available"
		info "You can download a tarball from vplex setup https://<IP>/apipackages/python/vplexapi.tgz
	Untar the file with the below command that creates a directory called 'vplexapi'
		tar -xzvf vplexapi.tgz
	Export PYTHONPATH with vplexapi path
		export PYTHONPATH=<path of above untar vplexapi>
	"
		info "Or you can use below export PYTHONPATH command to use available sdk"
		python_path=$each
	fi
	echo "\
	export PYTHONPATH=$python_path"

}


vplex_host()
{
	copy_modules()
	{
		info "Creating required worksapce directory... "
		mkdir -p "$env_path/ansible_modules/"
		info "coping modules, utils and doc fragments in worksapce directory... "
		cp -rf "$root_dir/plugins/"* "$env_path/ansible_modules/"
		
		# update modules
		for module in "$env_path/ansible_modules/modules/"*;
		do
			sed -i 's/dellemc.vplex.dellemc_vplex.vplex/dellemc_vplex.vplex/g' "$module"
			sed -i 's/from ansible_collections.dellemc.vplex.plugins.module_utils.storage.dell/from ansible.module_utils.storage.dell import/g' "$module"
			sed -i 's/import dellemc_ansible_vplex_utils as utils/dellemc_ansible_vplex_utils as utils/g' "$module"
		done
	}

	if ! command -v ansible &>> /dev/null
	then
		error "Ansible is not installed in vplex management server."
		info "Please install required ansible version and try again."
		exit 1
	fi

	env_path="$HOME/.ansible_vplex_modules"
	ans_ver=$( ansible $cmd_ver | head -n 1 | cut -d' ' -f2 )
	get_install_method

	
	if [ $method -eq 1 ];then
		install_collections
	elif [ $method -eq 2 ];then
		copy_modules	
		export ANSIBLE_LIBRARY=$env_path/ansible_modules/modules
		export ANSIBLE_MODULE_UTILS=$env_path/ansible_modules/module_utils
		export ANSIBLE_DOC_FRAGMENT_PLUGINS=$env_path/ansible_modules/doc_fragments
	fi
	

	verify_setup
	echo
	info "Sample playbooks can be found in $root_dir/docs/"
	info "In order to use sample roles, please copy $root_dir/roles to  $root_dir/docs/samples"
	
	echo
	info "Run below command to export environment variables and run playbooks..."
	echo


	if [ $method -eq 1 ];then
		echo "\
	export ANSIBLE_COLLECTIONS_PATHS=$env_path/collections"
	elif [ $method -eq 2 ];then
		echo "\
	export ANSIBLE_LIBRARY=$env_path/ansible_modules/modules
	export ANSIBLE_MODULE_UTILS=$env_path/ansible_modules/module_utils
	export ANSIBLE_DOC_FRAGMENT_PLUGINS=$env_path/ansible_modules/doc_fragments"
	fi

	echo
}

if [ -d $vplex_mg_server_dir ];then
	# install in vplex setup
	vplex_host
else
	non_vplex_host
	deactivate
	echo
	info "To deactivate virtualenv run command: deactivate
	"

fi
