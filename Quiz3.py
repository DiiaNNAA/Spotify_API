import requests
import json
import sqlite3

# 1
url = 'https://spotify23.p.rapidapi.com/charts/'
headers = {"X-RapidAPI-Host": "spotify23.p.rapidapi.com", "X-RapidAPI-Key": "9b256a3041msh22628cafc8f4678p159d28jsn55238a87b0c2"}
payload = {"type": "regional", "country": "global", "recurrence": "daily", "date": "latest"}
r = requests.get(url, headers=headers, params=payload)
# print(r.status_code)
# print(r.text)
# print(r.headers)

# 2
res = r.json()
with open('spotify.json', 'w') as file:
    json.dump(res, file, indent=4)

# 3
# მოხმარებელს შეჰყავს სიმღერის სახელწოდება და ბრუნდება შედეგი, თუ ვისი არის ეს სიმღერა, რამდენჯერ არის 'გასტრიმული'
# (მოსმენილი) და ჩარტში რომელ პოზიციას იკავებს.

song_title = input("Enter the song title: ")
pos = -1
while True:
    try:
        pos += 1
        if res['content'][pos]['track_title'] == song_title:
            print('This song by', res['content'][pos]['artists'], 'has been streamed for', res['content'][pos]['streams'],
                  'times. Position in charts:', res['content'][pos]['position'])
            break
    except IndexError:
        print("This song is not in the chart")
        break

# მოხმარებელს შეჰყავს რიცხვი, ხოლო შედეგად ბრუნდება ამ პოზიციაზე მყოფი სიმღერის შესახებ მონაცემები.

try:
    song_position = int(input("Enter the number between 1-200 to find out which song is on that position: "))
    if song_position <= 200:
        song = res['content'][song_position]
        print(f'Song on position {song_position} is', song['track_title'], 'by', song['artists'])
    else:
        print("Integer out of index. Please, choose number between 1-200.")
except ValueError:
    print("Enter the valid value!")

# 4
# ცხრილი, რომელშიც ასახულია ამჟამინდელი მონაცემების მიხედვით Spotify-ზე რომელი სიმღერები ლიდერობენ(top 200) და მოცემულია
# მათ შესახებ ინფორმაცია, თუ ვინ ასრულებს და სულ რამდენჯერ "გასტრიმეს", ასევე trend სვეტი გვეუბნება,chart-ში ზევიდან
# ქვევით გადაინაცვლა, თუ პირიქით (down, up) ან თუ ახალ გამოსულია და ახლა დაიწყო დატრენდვა (new).

with open('spotify.json') as file:
    res_dict = json.load(file)

conn = sqlite3.connect("spotify_db.sqlite")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS chart
                 (track_position INTEGER PRIMARY KEY,
                  track_title VARCHAR(70),
                  main_artist VARCHAR(50),
                  trend VARCHAR(20),
                  streams INTEGER)
                 ''')

chart_list = res_dict['content']
chart_list_to_insert = []
sliced_chart_list = []

for each in chart_list:
    chart_list_to_insert.extend([each['position'], each['track_title'], each['artists'][0], each['trend'], each['streams']])
# print(chart_list_to_insert)

# # for each in chart_list:
# #     chart_list_to_insert.append(each['position'])
# #     chart_list_to_insert.append(each['track_title'])
# #     chart_list_to_insert.append(each['artists'][0])
# #     chart_list_to_insert.append(each['trend'])
# #     chart_list_to_insert.append(each['streams'])

for i in range(0, len(chart_list_to_insert), 5):
    sliced_chart_list.append(tuple(chart_list_to_insert[i:i+5]))
# print(sliced_chart_list)

# cursor.executemany("INSERT INTO chart (track_position, track_title, main_artist, trend, streams) VALUES (?, ?, ?, ?, ?)", sliced_chart_list)
# conn.commit()

conn.close()


































