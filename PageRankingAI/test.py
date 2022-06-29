# import subprocess
from urllib.parse import urlparse
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
# from urllib.parse import urlencode
import socket
# from multiprocessing import Queue
import threading
# import getopt
# import sys
import os
import networkx as nx
from bs4 import BeautifulSoup
# import matplotlib

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize': (7, 5), 'figure.dpi': 80})
import threading, queue
import re
import pandas as pd

max_depth = 2
q = queue.Queue()
max_threads=50
to_crawl = queue.Queue()
crawled_urls=[]

# def check_link(url):
#     domain = '.'.join(urlparse(url).netloc.split('.')[-2:])
#     print("Domain is", domain)
#     filetype = urlparse(url).path.split('/')[-1:][0].split('.')[-1:][0]
#     if  (domain == 'politifact.com' and filetype != 'pdf'):
#       return True
#     else:
#       return False

def get_host(url):
  try:
    return socket.gethostbyname(urlparse(url).netloc)
  except:
      pass
  return None

def get_links_from_page(url):
    urllist = []
    try:
      res=urllib2.urlopen(url)
      htmlpage=res.read()
    except:
      return urllist

    try:
      page=BeautifulSoup(htmlpage, features="lxml")
    except:
      return urllist

    refs = page.findAll("a", href=True)
    for a in refs:
      try:
        link = a['href']
        if link[:4] == 'http':
          urllist.append(link)
      except:
        pass
    
    print("Got list", urllist)
    return urllist

def find_links(url_tuple,graph):
    '''Crawls to a given depth using a tuple structure to tag urls with their depth'''
    global crawled_urls, to_crawl, max_depth
    url = url_tuple[0]
    depth = url_tuple[1]
    if (depth < max_depth) :
      links = get_links_from_page(url)
      for link in links:
        '''These two lines create the graph'''
        graph.add_node(link)
        graph.add_edge(url,link)
        '''If the link has not been crawled yet, add it in the queue with additional depth'''
        if link not in crawled_urls:
          to_crawl.put((link, depth+1))
          crawled_urls.append(link)

class crawler_thread(threading.Thread):
    def __init__(self,queue,graph):
      threading.Thread.__init__(self)
      self.to_be_crawled=queue
      self.graph=graph
      while not self.to_be_crawled.empty():
        find_links(self.to_be_crawled.get(), self.graph)

# def draw_graph(graph, graph_file_name):
# 	'''Function to draw the graph and save the files'''
# 	nx.draw(graph,with_labels=False)
# 	nx.write_dot(graph,os.cwd()+graph_file_name+'.dot')
# 	plt.savefig(os.cwd()+graph_file_name+'.png')
 
def calculatePageRank(url):
  print("Getting page rank for", str(url))
  root_url = url

  to_crawl.put((root_url,0))
  crawled_urls.append(root_url)
  ip_list=[]
  graph=nx.Graph()
  graph.add_node(root_url)
  thread_list=[]

  for _ in range(max_threads):
    t = crawler_thread(to_crawl, graph)
    t.daemon=True
    t.start()
    thread_list.append(t)

  for t in thread_list:
    t.join()

  # for url in crawled_urls:
  #   ip_list.append(socket.gethostbyname(urlparse(url).netloc))
  #   ip_set=set(ip_list)
  #   ip_list = [*ip_set, ]

  print("Unique Host: %s " % len(ip_list))
  pagerank = nx.pagerank(graph, alpha=0.85, personalization=None,  weight='weight', dangling=None)
  edgeNumber = graph.number_of_edges()
  nodeNumber = graph.number_of_nodes()
  nodesize=[graph.degree(n)*10 for n in graph]
  pos=nx.spring_layout(graph,iterations=20)

  node_colors = ['g'] + ['r' for _ in range(nodeNumber-1)]

  nx.draw(graph,with_labels=False)
  nx.draw_networkx_nodes(graph,pos,node_size=nodesize,node_color=node_colors)
  nx.draw_networkx_edges(graph,pos)
  plt.figure(figsize=(5,5))
  plt.show()
  # return np.array(len(ip_list), pagerank.get(url), edgeNumber, nodeNumber)
  return pd.Series([pagerank.get(url), edgeNumber, nodeNumber], index=['pagerank','edges', 'nodes'])

url = 'https://www.theatlantic.com/politics/archive/2019/06/2020-democrats-abortion/590701/'
#'https://github.com/RobertSmithers'
# 'https://www.theatlantic.com/politics/archive/2019/06/2020-democrats-abortion/590701/'
print(calculatePageRank(url))