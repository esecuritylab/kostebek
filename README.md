<h1 align="center">
  <br>
  <a href="https://github.com/esecuritylab/kostebek"><img src="https://github.com/xsuperbug/kostebekpriv/blob/master/kostebek.png?raw=true" alt="Kostebek"></a>
</h1>
<h4 align="center">Reconnaissance Tool</h4>


### Introduction
The Kostebek is a reconnaissance tool which uses firms' trademark information to discover their domains.

#### Reference :
https://evren.ninja/en/post/recon-is-everywhere/

#### Demo video :

[![Kostebek](https://img.youtube.com/vi/OR4YzrgNNcE/0.jpg)](https://www.youtube.com/watch?v=OR4YzrgNNcE)

### Setup

#### Downloading Kostebek
`git clone https://github.com/esecuritylab/kostebek`

#### Requirements

```
sudo pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```
Download latest version of Chrome
https://www.google.com/chrome/browser/desktop/

dpkg -i google-chrome-stable_current_amd64.deb

```

### Example Usage

##### Trademark Scan 

```
python3 kostebek.py -u list.txt -n Organization Name
```

##### Yearmode (between the years Copyright-1990 and Copyright-2020)

```
python3 kostebek.py -u list.txt -n Organization Name -yearmode yes
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

#### Contributors
Ahmet Burak Gökalp - @A_Burak_Gokalp

