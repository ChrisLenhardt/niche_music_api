import json
import musicbrainzngs
import requests


def searchForCoverArt(artist: str, release: str):
    try:
        # release_group = musicbrainzngs.search_release_groups(artist=artist, release=release, strict=True)
        url=f"https://musicbrainz.org/ws/2/release-group/?query=artist:{artist}ANDrelease:{release}&fmt=json"
        response = requests.get(url, timeout=5.0)
        release_group = {}
        if response.status_code == 200:
            release_group = response.json()
        
    except:
        return "Error Occurred1"
    release_id=0
    
    if release_group != {}:
        try:
            release_id = release_group["release-groups"][0]["id"]
            print(release_id)
        except:
            return "Error Occurred2"
        
        
        # for release in release_list:
        #     if "status" in release:
        #         if release["status"] == "Official":
        #             release_id = release["id"]
        #             break
        
        try:
            getImageURL = f"https://coverartarchive.org/release-group/{release_id}"
            print(getImageURL)
            imageResponse = requests.get(getImageURL, timeout=5.0, allow_redirects=True)
            followThrough = requests.get(imageResponse.url, timeout=5.0)
            
            image_list = followThrough.json()
            print(image_list)
                
        except:
            return "Error occurred fetching image list"
        
        try:
            image_url = image_list["images"][0]["image"]
            return image_url
        except:
            return "Error Occurred3"
    
    return "Nothing found!"
    
def searchForProjectLink(release_name: str):
    search_result = musicbrainzngs.search_releases(release_name)
    if len(search_result['release-list']) > 0:
        res = search_result['release-list'][0]['id']
        return f"https://musicbrainz.org/release/{res}"
    
def pp_album(data):    
    results = data.data
    supplemental = {}
    for album in results:
        supplemental[album['release_name']] = {
            "img": searchForCoverArt(album["artist_name"], album['release_name']),
            "link": searchForProjectLink(album["artist_name"])
        }
    print(supplemental)
    print('---------------------------------------------------------------------------------------------------------------------')
    return json.dumps(supplemental)
#  album['release_name']