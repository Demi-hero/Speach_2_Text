# Speach_2_Text
A rudementry Speach to Text System running off of Google APIs


Is split in to two parts. 

Local Code: 
Code in the Ref Folder is for running on a local machine. This script will read all valid audio files in the Audio folder.
It will then feed each on to the Speach Recognition Library which is a lovely wrapper for the major Speach to Text librarires. 
This uses the Google Library. It will require you having a GCP account with Speach to Text activated as well as a JSON to prove authentication.
This will then write each transcription to a txt file in the Transcription folder.

Run on Server: 
When main is Run the code will provide a website where users can upload audio files to google cloud storage. Once all your files are uploaded
you can transcribe them using Google Speach to Text. These transcriptions can then be accessed clicking on the Transcription Link. 


TO-DO:
Add a download function
Remove Transcription when there are no transcription link
