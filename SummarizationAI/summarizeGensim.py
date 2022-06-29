from content import content
import gensim 
print('gensim Version: %s' % (gensim.__version__))

print('Original Content:')
print(content)
for word_count in [25,50,100]:
    summarized_content = gensim.summarization.summarize(content, word_count=word_count)#ratio=ratio)
    print()
    print('---> Summarized Content (Word Count is %.1f):' % word_count)
    print(summarized_content)