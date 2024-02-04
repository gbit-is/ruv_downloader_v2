# ruv_downloader

# About
Hugbúnaður til að sjálfvirkt búa til öryggisafrit af þáttum á rúv og save-ar sem mp4
Ath: Ennþá mjög hrátt, ekkert error handling t.d

# Install

Á linux/wsl:

- Install ffmpeg however you want to
- git clone git@github.com:gbit-is/ruv_downloader.git
- cd ruv_downloader
- python3 -m venv ./venv
- source venv/bin/activate

Á windows:
..... nota wsl bara ?

Á mac:
- eins og á linux bara held ég 


# How to use

./ruv_downloader.py download
Downloadar skjölum, eins og er þá er þetta eini valmöguleikinn

-- config.py

config.py.example

# Stuff sem ég bæti kannski við, ef ég nenni
.... eða eins og sumir kalla "to do"

- hafa eitthvað error handling
- gera basic search function fyrir þætti
- breyta path handling úr string cat yfir í os.path.join functions 


# Credits:
Hefði aldrei nennt að henda þessu saman ef ég hefði ekki haft hinn fínt kommentaða kóða [ruvsarpur](https://github.com/sverrirs/ruvsarpur) eftir [sverrirs](https://github.com/sverrirs) til að renna yfir og byggja API köllin á 

  
