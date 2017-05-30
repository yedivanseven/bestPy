# __bestPy__
A lightning fast and extendable recommendation framework

### Installation
Make a new directory to work in. Clone the repository into that directory or download and extract the tarball in that directory.

### Dependencies
See the _environment.yml_ file. Since nothing particularly fancy is used, slightly older versions of the listed packages might work as well but certainly not `python 2.x`.

### Getting Started
In order to recommend articles from your store to your customers, you first need some data on the past. In particular, we will assume that you can produce some sort of _transaction list_ containing a timestamp, a unique customer-ID and a unique article-ID for every sale. Say we have such a list in a *.csv file that looks like this (note the absence of column headers):
``
1331072795;customer-A2;BlueShirt-M-1749
1331074425;customer-B6;BlueShirt-L-1749
1331306282;customer-B6;BlackSocks-L-365
1331306283;customer-B6;BlackSocks-L-365
1331306313;customer-C5;RedJacket-XL-170
1331306332;customer-C5;WideHat-M-758925
...
``

Then, importing this data into your project can be as simple as ...

``python
from bestpy.datastructures import Transactions

file = '/path/to/your/transaction/file.csv'
data = Transactions.from_csv(file)
``

... and getting a recommendation for a customer can be as pleasant as:
``python
from bestpy import RecommendationBasedOn

recommendation = RecommendationBasedOn(data)
customer = 'customer-A2'
top_five = recommendation.for_one(customer)
for article in top_five:
    print(article)
``
``
'BlackSocks-M-1524'
'RedJacket-L-985'
'GreenJeans-M-568'
'PolkaDotTie-4856'
'OutdoorSandals-42'
``

But there is, of course, much more. With recommendations from the chef.
