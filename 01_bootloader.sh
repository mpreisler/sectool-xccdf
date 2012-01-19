#!/usr/bin/env bash

# ----------------------------------------------------------- #
# Copyright (C) 2008 Red Hat, Inc.                            #
# Written by Michel Samia <msamia@redhat.com>                 #
# Adapted for SCE by Martin Preisler <mpreisle@redhat.com>    #
# bootloader.sh                                               #
# ----------------------------------------------------------- #

# should be XCCDF bound variable, TODO
GRUBCONF=/boot/grub/grub.conf

# TODO
#check_file_perm ${GRUBCONF} 600 root:root 1 $E_BAD_PERMISSIONS "Bootloader configuration file"

if [[ "`egrep '^password' ${GRUBCONF} | wc -l`" == "0" ]]
then
	echo "${GRUBCONF} does not contain a password"
	echo "Please add the line 'password --md5 hash' to ${GRUBCONF}, where hash is output of grub-md5-crypt"	

	exit $XCCDF_RESULT_FAIL
fi

exit $XCCDF_RESULT_PASS

