# Win-Price-Estimation
This is a win price estimation model in Real-Time Biddiing System by NCTU ADSL lab.

# Required Python Library
  [scikit-learn](http://scikit-learn.org/stable/), [scipy](https://www.scipy.org/), [mpmath](http://mpmath.org/)

# Dataset

[iPinYou dataset] (http://data.computational-advertising.org/)

  * Season2: 2013/6/6~2013/6/12

  * Season3: 2013/10/19~2013/10/27

# Library
   * [dbFeatureHasher](./dbFeatureHasher): [sklearn FeatureHasher](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html)
   * [ftrlProximal](./ftrlProximal):Use [Ftrl-Proximal](https://www.eecs.tufts.edu/~dsculley/papers/ad-click-prediction.pdf) to predict CTR for each bid request. 


# Competitor
  [Wush Chi-Hsuan Wu, Mi-Yen Yeh, and Ming-Syan Chen. Predicting Winning Price in Real Time Bidding with Censored Data](http://www0.cs.ucl.ac.uk/staff/w.zhang/rtb-papers/win-price-pred.pdf). In KDD, 2015.
  
  https://github.com/wush978/KDD2015wpp
  
# Code
  * [win_price_model] (./win_price_model)
    * [preprocess.py] (./win_price_model/preprocess.py)
        * (1) Get data from source dataset (ipinyou.contest.dataset)
        * (2) Sort the data with timestamp
        * (3) Predict CTR by [Ftrl_proximal](./ftrlProximal)
        * (4) Generate simulated data with different simulated ratio
        * (5) Filter the data with the winning price equal to zero
        * (6) Pickle the dataset with [FeatureHasher](./dbFeatureHasher)
    * [simulated_1_6] (./win_price_model/simulated_1_6)
      * simulated ratio: 0.167 (1/6)
    * [simulated_2_6] (./win_price_model/simulated_2_6)
      * simulated ratio: 0.333 (2/6)
    * [simulated_3_6] (./win_price_model/simulated_3_6)
      * simulated ratio: 0.5   (3/6)
      * [maxOfAll](./win_price_model/simulated_3_6/maxOfAll/season2): initialize the theta with max(winning price, bidding price)
      * [meanOfAll](./win_price_model/simulated_3_6/meanOfAll/season2):initialize the theta with the mean of all data (win bid: winning price, lose bid: bidding price)
      * [meanOfwin](./win_price_model/simulated_3_6/meanOfwin/season2):initialize the theta with the mean of win data
      * [varWL](./win_price_model/simulated_3_6/varWL/season2):initialize the theta with variance(.)/mean(.) of all data (win bid: winning price, lose bid: bidding price)
    * [simulated_4_6] (./win_price_model/simulated_4_6)
      * simulated ratio: 0.667 (4/6)
    * [simulated_5_6] (./win_price_model/simulated_5_6)
      * simulated ratio: 0.833 (5/6)
