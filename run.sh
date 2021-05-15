# Requires BBS_TOOLS setup (https://github.com/arshadkazmi42/bbs)

SUBDOMAINS_PATH=$BBS_PATH/subdomains

echo "Running for "$1

# Get domains if not exists
sh $SUBDOMAINS_PATH/subdomains.sh $1

# Run crawler
cat $SUBDOMAINS_PATH/subdomains/$1.txt | xargs -I {} python3 scan.py {}

