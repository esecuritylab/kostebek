<h1 align="center">
  <br>
  <a href="https://github.com/esecuritylab/kostebek"><img src="https://i.ibb.co/YXHMbkM/logo.jpg"  width=350 height=350 alt="Kostebek"></a>
  <br>
  Kostebek
</h1>
<h4 align="center">Kostebek Reconnaissance Tool</h4>

### Introduction

The Kostebek is a reconnaissance tool which uses firms' trademark information to discover their domains.

[![Kostebek](https://img.youtube.com/vi/OR4YzrgNNcE/0.jpg)](https://www.youtube.com/watch?v=OR4YzrgNNcE)

### Setup

#### Downloading Kostebek
`git clone https://github.com/esecuritylab/kostebek`

#### Requirements

sudo apt-get -y install python3-pip

pip3 -r requirements.txt 

Download latest version of Chromedriver and configure your driver-path
```sudo apt-get install unzip```
```sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/```


Download latest version of Chrome
https://www.google.com/chrome/browser/desktop/
```dpkg -i google-chrome-stable_current_amd64.deb```
```apt-get install -f```
```dpkg -i google-chrome-stable_current_amd64.deb```


### Example Usage

##### Trademark Scan 

```
python3 kostebek.py -u list.txt -n Organization Name
```
##### Get Google Domains
```
python3 kostebek.py -g Organization Name 
```
##### Get Bing Domains
```
python3 kostebek.py -b Organization Name 
```
##### Get Yahoo Domains
```
python3 kostebek.py -y Organization Name 
```
##### Get Company Trademarks
```
python3 kostebek.py -t Organization Name
```

#### Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. You can also suggest a feature, just open an issue.

