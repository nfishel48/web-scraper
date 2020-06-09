#import nessary libraries
import csv
import json
import requests
import key #key contains the api url and my personal api key


#make the API call using the API stored in a differnt file.
api_url = key.url

#check the API response
api_response = requests.get(api_url)

#API worked 
if api_response.status_code == 200:
    videos = json.loads(api_response.text)
    #create the spreadsheet collom lables
    with open("youtube_videos.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["publishedAt",
                            "title",
                            "description",
                            "thumbnailurl"])
        has_another_page = True
        while has_another_page:
        #fill in the rows with the data
            if videos.get("items") is not None:
                for video in videos.get("items"):
                    video_data_row = [
                        video["snippet"]["publishedAt"],
                        video["snippet"]["title"],
                        video["snippet"]["description"],
                        video["snippet"]["thumbnails"]["default"]["url"]
                    ]
                    csv_writer.writerow(video_data_row)
            #check if another page exists
            if "nextPageToken" in videos.keys():
                next_page_url = api_url + "&pageToken="+videos["nextPageToken"]
                next_page_posts = requests.get(next_page_url)
                videos = json.loads(next_page_posts.text)
            else:
                print("no more videos") 
                has_another_page = False

        

#API did not work
else:
    print("Error 404 or other bad URL repsonse")