import requests 
import json
import pandas as pd


key = 'acb874bd'
film = "Game of Thrones"
url_base =f"http://www.omdbapi.com/?apikey={key}"

def generate_url(url_base, tv_show, season, episode):
    url = url_base + f"&t={tv_show}" + f"&Season={season}" + f"&Episode={episode}"
    return url 


fields = ['Season','Episode','Title','Genre','imdbRating','imdbVotes']
seasons = range(1,2)
episodes = range(1,12)

data = []
for season in seasons:
    for episode in episodes:
        url = generate_url(url_base, film, season, episode)

        print('URL Gerada: ', url)
        response = requests.get(url)

        if response.status_code == 200:
            content = json.loads(response.text)
            if content.get('Error') is None: # sem dados, portanto skipar 
                # Season = content.get('Season')
                # Episode = content.get('Episode')
                # Title = content.get('Title')
                # Genre = content.get('Genre')
                # imdbRating = content.get('imdbRating')
                # imdbVotes = content.get('imdbVotes')

                # cell_data = [Season , Episode, Title, Genre, imdbRating, imdbVotes] 

                cell_data = [content.get(field) for field in fields]
                data.append(cell_data)
        else:
            print(f'Request falhou com status {response.status_code}')

dataframe = pd.DataFrame(data, columns=fields)
dataframe['imdbRating'] = dataframe['imdbRating'].replace(to_replace='.', value=',')
dataframe['imdbRating'] = dataframe['imdbRating'].astype('float')
dataframe['above_nine'] = np.where(dataframe['imdbRating'] >= 9, True, False)

dataframe.to_excel(f"{film}.xlsx")