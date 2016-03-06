# Text Analysis

**Parsing each article, break the body into sentences and output into XML file.**  
For each articles all processed tags are stored in Doc object. The body is parsed by lines and then tokened by sentences (dot delimiter).
The required arguments are input folder, output file and stopwords file

SGML Parser handles the relevant tags (overriding methods) for attached articles corpus from the Reuters.com domain based SGML file.

**Calculating top frequent words in the whole corpus and prints it to the standard output.**  
Each sentence is parsed as following :
* Tokenized by space  
* Punctuation are removed  
* All the letters are lowered  

All the words are accumulated, except stopwords (if given). Thereafter, The words might be ranked and sorted by their counters.
