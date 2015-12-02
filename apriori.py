import sys
import pudb


def generate_next_set(set_list, length):
  '''generate C_{i+1} given C_i, i.e. generate next length itemsets'''
  new_list = set([i.union(j) for i in set_list for j in set_list if len(i.union(j)) == length])
  return new_list


def get_transactions_list_itemset(inFile):
  '''Generate itemset and transactions list'''
  itemset = set()
  transactionList = []
  for line in inFile:
    line = line.strip().rstrip(',')
    record = set(line.split(','))
    transactionList.append(record)
    for item in record:
      itemset.add(frozenset([item]))

  return itemset, transactionList


def fetch_min_support_items(itemset, minSupport, transactionList, total_freq_item):
  freq_item = {}
  new_itemset = set()
  L = len(transactionList)

  for i in itemset:
    for t in transactionList:
      if i.issubset(t):
        freq_item[i] = freq_item.get(i, 0) + 1

  for key in freq_item:
    value = freq_item[key]
    if value >= minSupport * L:
      new_itemset.add(key)
      total_freq_item[key] = value

  return new_itemset


def generate_rules(inFile, minConfidence, minSupport):
  total_freq_item = {}
  itemset, transactionList = get_transactions_list_itemset(inFile)
  itemset = fetch_min_support_items(itemset, minSupport, transactionList, total_freq_item)

  k = 2
  while(True):
    itemset = generate_next_set(itemset, k)
    itemset = fetch_min_support_items(itemset, minSupport, transactionList, total_freq_item)
    k = k + 1
    if len(itemset) == 0:
      break

  print total_freq_item
  return 0,0

def print_data(record):
  '''Test: print data'''
  for rec in record:
    print rec

if __name__ == '__main__':
  if len(sys.argv) < 4:
    print '''usage python apriori.py Dataset.csv minSupport minConfidence'''
    sys.exit(0)

  inFile = None
  try:
    inFile = open(sys.argv[1], 'rU')
    [minSupport, minConfidence] = map(float, sys.argv[2:4])
  except Exception as e:
    print e
    sys.exit(0)
  # pudb.set_trace()
  items, rules = generate_rules(inFile, minConfidence, minSupport)