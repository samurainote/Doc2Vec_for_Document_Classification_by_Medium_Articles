# Doc2Vec for Document Classification by Medium Articles
## Doc2Vecを用いたMedium記事に対する文章分類
![](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs40537-018-0139-2/MediaObjects/40537_2018_139_Fig8_HTML.png)

## Introduction

Doc2Vec is a technology that vectorizes documents of arbitrary length, and can obtain distributed document embeddings for sentences and texts.And also it does not depend on a specific task, various application methods such as the following can be considered.

Since fixed-length vectors are often used for input in machine learning models, they are often preprocessed in advance by Doc2Vec into input vectors.
Although there have been techniques for making fixed-length small vectors such as Bag-of-words and LDA in the past, using Doc2Vec has been reported to boast superior performance over previous techniques

## Technical Preferences

| Title | Detail |
|:-----------:|:------------------------------------------------|
| Environment | MacOS Mojave 10.14.3 |
| Language | Python |
| Library | scikit-learn, Numpy, matplotlib, Pandas, Seaborn, Genism|
| Dataset | [ Original Data ](https://medium.com/) |
| Algorithm | Collaborative Filtering, Singular Value Decomposition |

## References

- [A gentle introduction to Doc2Vec](https://medium.com/scaleabout/a-gentle-introduction-to-doc2vec-db3e8c0cce5e)
- [Multi-Class Text Classification with Doc2Vec & Logistic Regression](https://towardsdatascience.com/multi-class-text-classification-with-doc2vec-logistic-regression-9da9947b43f4)
- [models.doc2vec – Doc2vec paragraph embeddings](https://radimrehurek.com/gensim/models/doc2vec.html)
- [Doc2Vecの仕組みとgensimを使った文書類似度算出チュートリアル](https://deepage.net/machine_learning/2017/01/08/doc2vec.html)
- [fastTextとDoc2Vecのモデルを作成してニュース記事の多クラス分類の精度を比較する](https://qiita.com/kazuki_hayakawa/items/ca5d4735b9514895e197)
