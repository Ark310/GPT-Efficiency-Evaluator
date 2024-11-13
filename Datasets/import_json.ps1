# Define the directory containing JSON files
$Directory = "C:\Users\abdul\Desktop\ITEC 4020\Assignment 1\Datasets\output_json"

# MongoDB connection URI
$Uri = "mongodb+srv://admin:admin@gpt-evaluation-cluster.ke3np.mongodb.net/Chat_GPT_Datasets"

# MongoDB collection name
$Collection = "Computer_Security"

# Get all JSON files in the directory
$Files = Get-ChildItem -Path $Directory -Filter *.json

# Loop through each JSON file and import it
foreach ($File in $Files) {
    Write-Host "Importing $($File.FullName)"
    & mongoimport --uri $Uri --collection $Collection --file $($File.FullName)
}

Write-Host "Import complete!"