import csv
import re
import math
from collections import Counter

with open("mega2.csv") as f:
 
    r = csv.reader(f, delimiter='\t')
    rgx = re.compile(r'\b[a-zA-Z]+\b')
    docs = [ (' '.join(re.findall(rgx, x[2])).lower(), ' '.join(re.findall(rgx, x[3])).lower())  \
            for i,x in enumerate(r)]
 
print(docs[0][0],docs[0][1])
print "\n"
print(docs[11][0],docs[11][1])
# print "\n"
# print(docs[2][0],docs[2][1])
# print "\n"
# print(docs[3][0],docs[3][1])
# print "\n"
# print(docs[4][0],docs[4][1])
 
items_t = [ d[0] for d in docs ] # item titlescd    
items_d = [ d[1] for d in docs ] # item descriptions
items_i = range(0, len(items_t)) # item id


#index
def create_inverted_index(corpus):
   idx={}
   for i, document in enumerate(corpus):
       for word in document.split():
           if word in idx:
              if i in idx[word]:
                idx[word][i] += 1
              else:
                  idx[word][i] = 1
           else:
               idx[word] = {i:1}
   return idx

idx = create_inverted_index(items_d)
#print(idx)




def idf(term, idx, n):
    return math.log(float(n) / (1 + len(idx[term])))    


def print_results(results,n, head=True):

   if head:    
       print('\nTop %d from recall set of %d items:' % (n,len(results)))
       for r in results[:n]:
           print('\t%0.2f - %s'%(r[0],items_t[r[1]]))

   else:
       print('\nBottom %d from recall set of %d items:' % (n,len(results)))
       for r in results[-n:]:
           print('\t%0.2f - %s'%(r[0],items_t[r[1]]))
 



# #TF IDF
def get_results_tfidf(qry, idx, n):
  score = Counter()
  
  for term in qry.split():
    print term
    print "\n"
      
      # << IMPLEMENT TF-IDF SCORING >> CODE HERE
 
    if term in idx:
        i = idf(term, idx, n)
        #print i
        for doc in idx[term]:
           # print "doc", doc
            #print "idx[term][doc]", idx[term][doc]
            score[doc] += idx[term][doc] + i
            #print score
 
  results=[]
  for x in [[r[0],r[1]] for r in zip(score.keys(), score.values())]:
      if x[1] > 0:
          results.append([x[1],x[0]])
 
  sorted_results = sorted(results, key=lambda t: t[0] * -1 )
  return sorted_results
 

results = get_results_tfidf('brains hello hi', idx, len(items_t))

#print results
print_results(results,5)