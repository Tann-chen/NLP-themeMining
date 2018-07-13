import pytextrank
import sys

path_in = "input/in.json"
path_stage1 = "test_data/s1.json"
path_stage2 = "test_data/s2.json"
path_stage3 = "test_data/s3.json"
# stage1 : generate graph
with open(path_stage1, 'w') as file:
    json_iterator = pytextrank.json_iter(path_in)
    for g in pytextrank.parse_doc(json_iterator):
        file.write("%s\n" % pytextrank.pretty_print(g._asdict()))
        #print(pytextrank.pretty_print(g))

# stage2 : key words
graph, ranks = pytextrank.text_rank(path_stage1)
pytextrank.render_ranks(graph, ranks)
with open(path_stage2, 'w') as file:
    for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
        file.write("%s\n" % pytextrank.pretty_print(rl._asdict()))
        #print(pytextrank.pretty_print(rl))

# # stage3 : summarize sentence
kernel = pytextrank.rank_kernel(path_stage2)
with open(path_stage3, 'w') as file:
    for s in pytextrank.top_sentences(kernel, path_stage1):
        file.write(pytextrank.pretty_print(s._asdict()))
        file.write("\n")
        #print(pytextrank.pretty_print(s._asdict()))

# stage4 : summarize based on most significant sentence & keywords
phrases = ", ".join(set([p for p in pytextrank.limit_keyphrases(path_stage2, phrase_limit=12)]))
sent_iter = sorted(pytextrank.limit_sentences(path_stage3, word_limit=150), key=lambda x: x[1])
s = []

for sent_text, idx in sent_iter:
    s.append(pytextrank.make_sentence(sent_text))

graf_text = " ".join(s)
print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
