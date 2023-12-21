from youtube_transcript_api import YouTubeTranscriptApi
import validators

# Read and validate links from the file
links = []
with open('links.txt', 'r') as file:
    for line in file:
        link = line.strip()
        if validators.url(link):
            links.append(link)
        else:
            print(f"Invalid link: {link}")

# Get user input for search term
print("What are we looking for? -> ", end='')
search = input().lower()

# Process each link
final_data = []
for link in links:
    video_id = link[-11:]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        timestamps = [entry['start'] for entry in transcript if search in entry['text'].lower()]
        final_data.append((link, timestamps))
    except Exception as e:
        print(f"Error fetching transcript for {link}: {e}")

# Print results
for link, timestamps in final_data:
    print(f"\n{link}")
    for timestamp in timestamps:
        formatted_time = f"{int(timestamp // 3600):02d}:{int(timestamp % 3600 // 60):02d}:{int(timestamp % 60):02d}"
        print(f"     {formatted_time} -> {link}&t={int(timestamp)}s")
