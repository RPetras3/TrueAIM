# Define the paths to the two folders
$Folder2 = "images"
$Folder1 = "labels"

# Get all files from both folders recursively
$Folder1_Files = Get-ChildItem -Path $Folder1 -File -Recurse -Force
$Folder2_Files = Get-ChildItem -Path $Folder2 -File -Recurse -Force

# Iterate through files in the second folder
Foreach ($File in $Folder2_Files) {
    # Check if the BaseName of the current file in Folder2 exists in Folder1
    If (-not($File.BaseName -in $Folder1_Files.BaseName)) {
        # Delete the file in Folder2
        # Remove -WhatIf to actually execute the deletion
        Remove-Item -Path $File.FullName -Verbose
    }
}