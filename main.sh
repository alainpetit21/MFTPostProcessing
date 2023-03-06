echo "Taking input from ./data/mft.raw.out.csv"
echo "You have to edit the times in main.py"


source ./venv/bin/activate
python3 ./src/main.py

echo "Writing results in ./data/mft.raw.out.csv.json"
echo "User Firefox to display the output JSON"

