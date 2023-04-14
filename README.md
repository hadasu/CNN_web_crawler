If you are not familiar with web crawling you may want to read this, 
Web crawling with Python - https://www.scrapingbee.com/blog/crawling-python/, before proceeding.

The CNN web crawler starts scanning from the URLs provided in the main.
The URLs should be a CNN website index or a CNN-related website URL - **it will not work on other websites**.

The crawler goes through all the connected URLs until the depth that is provided in the main and looks for articles.
When the crawler comes across an article it pulls the following information from the article HTML:
author, date_published,  date_modified,  article_section,  URL,  headline,  description,  keywords, and the full text of the article as text.
The information is saved to CNN_Articles.csv for further use.

You can see data analysis and ML using this dataset on Kagel - https://www.kaggle.com/datasets/hadasu92/cnn-articles-after-basic-cleaning.
