# Amazon Data Extract 

```bash
pip install -r requirements.txt
python main.py
scrapy runspider crawl.py -o reviews.csv
```
> Add ASIN number of the products in Asinfeed.csv.
```bash
python visualise.py 
```
![amazon_reviews](reviews.png)

```bash
$ python sentiment.py
> number words in training corpus: 4856
> accuracy: 0.56712
```