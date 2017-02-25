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

# Docker Jekyll Dev Env

```bash
docker run --name jekyll -it --rm ^
-v c:/Users/dnldx/OneDrive/workspace/dnldxn.gitlab.io:/src ^
-p 4000:4000 ^
ruby:2.3 ^
/bin/bash

cd /src
bundle install
JEKYLL_ENV=production jekyll serve --watch --force_polling --incremental --host=0.0.0.0
```

# Docker Python Build Env

```bash
docker run --name python --rm -it ^
-v c:/Users/dnldx/OneDrive/workspace/dnldxn.gitlab.io:/src ^
python:3.6 ^
/bin/bash
```

# Docker Notebook

```bash
docker run --name anaconda -it -p 8888:8888 ^
-v /c/Users/dnldx/Documents/jupyter_notebooks:/opt/notebooks ^
-v /c/Users/dnldx/OneDrive/workspace/dnldxn.gitlab.io/_data:/data ^
continuumio/anaconda3 ^
/bin/bash

conda install jupyter tensorflow keras scikit-learn pandas numpy spacy seaborn -y

/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser
```


# Resources

http://launchaco.com/build/

https://www.logojoy.com/
