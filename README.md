# ruv_downloader

# About
Hugbúnaður til að sjálfvirkt búa til öryggisafrit af þáttum á rúv og save-ar sem mp4
Ath: Ennþá mjög hrátt, ekkert error handling t.d

Kemur í staðinn fyrir [gömlu útgáfuna](https://github.com/gbit-is/ruv_downloader) sem hætti að virka í byrjun 2024

# Install

Á linux/wsl:

- Install ffmpeg however you want to
- git clone git@github.com:gbit-is/ruv_downloader_v2.git eða git clone https://github.com/gbit-is/ruv_downloader_v2.git
- cd ruv_downloader_v2
- chmod +x ruv_downloader.py
- python3 -m venv ./venv
- source venv/bin/activate
- pip install -r requirements.txt

Á windows:
..... nota wsl bara ?

Á mac:
- eins og á linux bara held ég 


# How to use

./ruv_downloader.py download
Downloadar skjölum, eins og er þá er þetta eini valmöguleikinn

-- config.py

config.py.example inniheldur allar útskýringar á hvernig þetta virkar

# Credits:
Endursmíðun frá grunni með nýrri aðferð, notandi GQL interface-ið á rúv síðunni, fékk nokkrar ágætis hugmyndir frá "Forritarar á Íslandi" á facebook 

Hefði aldrei nennt að henda þessu saman upprunalegu útgáfunni ef ég hefði ekki haft hinn fínt kommentaða kóða [ruvsarpur](https://github.com/sverrirs/ruvsarpur) eftir [sverrirs](https://github.com/sverrirs) til að renna yfir og byggja API köllin á, held ég sé ekki lengur að nota neitt af hans kóða eða vinnuí þessari útgáfu, en hann fær samt shout-out hér :) 

  
