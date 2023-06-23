#!/bin/bash

HC_PATH="hashcat-6.2.6"
HC_CMD=${HC_PATH}/hashcat.bin
HC_OPT="--workload-profile 4 --optimized-kernel-enable --hash-type 1000 --username --outfile-format 1,2,3,4,5,6"
HASH_FILE="test.ntlm"
OUTPUT="out/"
DICT="words/collected.txt"

### Time estimates assume a single Tesla T4 on an AWS EC2 g4dn.xlarge instance using an optimzed kernel and the full 16GB crackstation 
### and NTLM 

### Crackstation with OneRuletoRuleThemAll (3 hours on a Tesla T4)
HC_SESS="onerule"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 0 --loopback --rules-file ${RULE} ${HASH_FILE} ${DICT}

### Crack everything up to 6 positions in length (mask attack) (2 hours)
HC_SESS="b6-mask"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 3 --increment ${HASH_FILE} "?b?b?b?b?b?b"

### Crack all ASCII character up to 7 characters (mask attack) (0.5 hours)
HC_SESS="a7-mask"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 3 ${HASH_FILE} "?a?a?a?a?a?a?a"

### Crack all numbers from 8-14 (3 hours)
HC_SESS="d14-mask"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 3 --increment --increment-min 8 --increment-max 14 ${HASH_FILE} "?d?d?d?d?d?d?d?d?d?d?d?d?d?d"

### Straight dictionary attack 
HC_SESS="dict"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 0 ${HASH_FILE} ${DICT}

### Markov (let it run until done)
HC_SESS="markov"
${HC_CMD} ${HC_OPT} --outfile "${OUTPUT}/${HC_SESS}" --session "${HC_SESS}" --attack-mode 0 ${HASH_FILE}