import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors

#Requisição da API

api_service_name = 'youtube'
api_version = 'v3'

API_KEY = 'API_KEY'

youtube = googleapiclient.discovery.build( api_service_name, 
                                           api_version,
                                           developerKey= API_KEY
                                            )



requests = youtube.commentThreads().list(part = 'snippet',
                                         videoId = 'VWxRO6YIeBU', 
                                         maxResults = 100
                                         )

response = requests.execute()


all_comments = []

next_page_token = None
while True:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId='VWxRO6YIeBU',
        maxResults=100,  # O máximo permitido é 100 por página
        pageToken=next_page_token
    )
    response = request.execute()
    
 
#Agrupamento dos resultados da API
    for row in response['items']:
        comment = row['snippet']['topLevelComment']['snippet']
        comments = {'Usuarios':comment['authorDisplayName'],
                    'Comentarios': comment['textDisplay'], 
                    'Curtidas': comment['likeCount'],
                    'Data':comment['publishedAt'],
                    'Source': 'Youtube'}
        
        all_comments.append(comments)

    
    # Verifica se há mais páginas de resultados
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break  # Se não houver mais páginas, saia do loop

data = pd.DataFrame(all_comments)

data.to_csv('youtube_extract.csv')
