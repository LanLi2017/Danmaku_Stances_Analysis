import os
import shlex

from nltk.parse.corenlp import CoreNLPServer, CoreNLPParser

# import stanza
# # zh/ zh-hans
# nlp = stanza.Pipeline('zh', processors='tokenize,pos', use_gpu=True, pos_batch_size=3000) # Build the pipeline, specify part-of-speech processor's batch size
# title = nlp("中国人为什么不能选择安乐死?") # Run the pipeline on the input text
# print(title) # Look at the result

# set up the client
from stanfordnlp.server import CoreNLPClient
#
# import stanfordnlp
# nlp = stanfordnlp.Pipeline()
# doc = nlp("Barack Obama was not born in Hawaii")
# print(doc)

from stanfordnlp.server import CoreNLPClient


text = "Barack Obama was not born in Hawaii."


# set up the client
with CoreNLPClient(annotators=['tokenize','ssplit','pos','depparse'], timeout=60000, memory='16G') as client:
    # submit the request to the server
    ann = client.annotate(text)

    # get the first sentence
    sentence = ann.sentence[0]

    # get the dependency parse of the first sentence
    dependency_parse = sentence.basicDependencies

    #print(dir(sentence.token[0])) #to find all the attributes and methods of a Token object
    #print(dir(dependency_parse)) #to find all the attributes and methods of a DependencyGraph object
    #print(dir(dependency_parse.edge))

    #get a dictionary associating each token/node with its label
    token_dict = {}
    for i in range(0, len(sentence.token)) :
        token_dict[sentence.token[i].tokenEndIndex] = sentence.token[i].word

    #get a list of the dependencies with the words they connect
    list_dep=[]
    for i in range(0, len(dependency_parse.edge)):

        source_node = dependency_parse.edge[i].source
        source_name = token_dict[source_node]

        target_node = dependency_parse.edge[i].target
        target_name = token_dict[target_node]

        dep = dependency_parse.edge[i].dep

        list_dep.append((dep,
            str(source_node)+'-'+source_name,
            str(target_node)+'-'+target_name))
    print(list_dep)


# res = []
# for t in title_dep:
#     print(t)
#     print(t.treepositions())
#     print(t.treepositions('leaves'))
#     pos = t.treepositions('leaves')
#     #(NN 中国人)
#     # print(t[0,0,0,0])
#     # (AD 为什么)
#     # print(t[0,0,1,0,0])
#     # (AD 不)
#     # print(t[0,0,1,1,0])
#     # (VV 能)
#     # print(t[0,0,1,2,0])
#     # (VV 选择)
#     # print(t[0,0,1,2,1,0])
#     # (PU ？)
#     idxs = []
#     for p in pos:
#         index = t.treepositions().index(p)
#         idx = index-1
#         idxs.append(t.treepositions()[idx])
#     for id in idxs:
#         res.append(t[id])
#
# subjects = []
# for r in res:
#     if r.label() == 'NN':
#         subjects.append(r.leaves())
# print(subjects)