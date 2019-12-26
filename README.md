```
 | |/ / (_) (_)       | |          | |            | |   
 | ' /    ___    ___  | |_    ___  | |__     ___  | | __
 |  <    / _ \  / __| | __|  / _ \ | '_ \   / _ \ | |/ /
 | . \  | (_) | \__ \ | |_  |  __/ | |_) | |  __/ |   < 
 |_|\_\  \___/  |___/  \__|  \___| |_.__/   \___| |_|\_	
 ```

The Kostebek is a reconnaissance tool which uses firms' trademark information to discover their domains.



**Installation**

```
Tested on Kali Linux 2018.2, Ubuntu 16.04 

sudo apt-get -y install python3-pip

pip3 -r requirements.txt  


download latest version of Chromedriver and configure your driver-path
#sudo apt-get install unzip
#sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


download latest version of Chrome
https://www.google.com/chrome/browser/desktop/
#dpkg -i google-chrome-stable_current_amd64.deb
#apt-get install -f
#dpkg -i google-chrome-stable_current_amd64.deb
```

**Example**

 Trademark Scan :  python3 kostebek.py -u list.txt -n Organization Name
 
 Get Google Domains  : python3 kostebek.py -g Organization Name 
 
 Get Company Trademarks : python3 kostebek.py -t Organization Name

 ***Demo***

[![Kostebek](https://img.youtube.com/vi/OR4YzrgNNcE/0.jpg)](https://www.youtube.com/watch?v=OR4YzrgNNcE)


***Contributing***

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. You can also suggest a feature, just open an issue.

