# Run on C9

```bash
sudo apt-get install python3.5 python3.5-dev
sudo mv /usr/bin/python /usr/bin/python2
sudo ln -s /usr/bin/python3.5 /usr/bin/python

sudo pip install numpy
sudo pip install pandas
bundle install
JEKYLL_ENV=production jekyll serve --host $IP --port $PORT --baseurl ''
```

Edit _.config.yml:

url:                https://dnldxn-gitlab-io-persuses.c9users.io


# Resources

http://launchaco.com/build/

https://www.logojoy.com/
