# "From IMDb to Telegram" bot 

---
## Intro
This bot was implemented as part of a student's coursework. A detailed description of the functionality and operating 
principles of the bot can be found in the explanatory note to the course work 
[in this doc](https://docs.google.com/document/d/11mslPQ10n_FOH9sNZ62VB8QqIjQbTuj-/edit?usp=sharing&ouid=106533504356579286687&rtpof=true&sd=true) (rus).


I will be grateful for your advice and recommendations on possible improvements to the project.
> - e-mail: [ilya.s.shutov@gmail.com](mailto:ilya.s.shutov@gmail.com)
> - tg:  [@ilya_s_shutov](https://t.me/ilya_s_shutov)

---
## Description
 The project uses API from [rapidapi.com](https://rapidapi.com/) ([IMDb API by Api Dojo](https://rapidapi.com/apidojo/api/imdb8)).

- You need to register on the site and subscribe to the specified API. 
- Get your API-HOST and API-KEY from API
- [Get the token of your future bot](https://core.telegram.org/bots/tutorial#introduction)
- Save the project on your computer
- Create virtual environment
```commandline
python  -m venv <name_of_youre_venv_folder>
```
- Install dependencies
```commandline
pip install -r requiriments.txt
```
- Input your token, API-HOST, API-KEY and path to your log file in file .env (look at .env-example)
- Run main.py