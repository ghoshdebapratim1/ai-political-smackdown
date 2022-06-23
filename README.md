# Screenshots

![Home Page](https://github.com/ghoshdebapratim1/ai-political-smackdown/blob/main/app/static/img/scrnsht1.png)

![Model Page](https://github.com/ghoshdebapratim1/ai-political-smackdown/blob/main/app/static/img/scrnsht2.png)

### About us

We are a group of high school students who are working together to create a website to simulate political debates.

Our group members are:

Nishant Perla    
Faiza Shah    
Aryaman Gupta  
Joanne Zhang  
Petter Potts  
And our mentor, Deb Ghosh

### How to Use

Download all the files under our `app` folder, including the HTML and Python files.

- app/
  - **main.py**
  - **utils.py**
  - templates/
    - **writer_home.html**
    - **Write-your-story-with-AI.html**
  - static/
    - **img/** 
    - **js/**
    - **css/**
  - model/
    - To download the model we are using, make a copy of the files in this google drive folder:
      https://drive.google.com/drive/folders/1CbwEE4dkv4n1ab1u83LWGONhVAZ4ITYf?usp=sharing

### Technical Stack

We used python on the cocalc server for the majority of the project. This included the data scraping and cleaning. In addition, we used Google Collab to train our models.

The base models we used were **GPT-2**, **distilgpt-2**, and **GPT-neo**, along with **aitextgen** to help train it.

### Dataset

For our dataset, we originally used one from Kaggle. However, this wasn't sufficient, so we also scraped comments from Reddit.

After cleaning the Reddit comments, we combined them with a Hugging Face dataset that contained hyper\-partisan articles.

### Type of Model

For both the conservative and liberal models, we used **GPT\-neo**, as it the most advanced model.

we played around with **GPT-2** and **distilgpt-2**, and while they took less time to train, the **neo** model gave better results.

### Libraries Used

We used pandas, numpy, and re for cleaning our data. In addition, we used flask for our backend coding, and nltk for some processing steps.

