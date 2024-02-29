# Apache Lucene

## 作者
Doug Cutting

## 简介
Apache Lucene 是一个完全用Java编写的高性能，功能齐全的文本搜索引擎库。它是一种适用于几乎所有需要全文搜索（ full-text search）的应用程序的技术，尤其是跨平台搜索。
Apache Lucene是一个可供免费下载的开源项目

[官网]('http://lucene.apache.org' '')

[GitHub]('https://github.com/apache/lucene' '')

[原来的Github]('https://github.com/apache/lucene-solr' '')，现在solr和lucene项目已经分离

[JavaBug导致的LuceneBug]('https://cwiki.apache.org/confluence/display/lucene/JavaBugs' '')
## 功能
Lucene通过简单的API提供强大的功能
- over 800GB/hour on modern hardware
- small RAM requirements -- only 1MB heap
- incremental indexing as fast as batch indexing(增量索引与批量索引一样快)
- index size roughly 20-30% the size of text indexed(索引大小约为索引文本大小的20-30％)

强大，准确，高效的搜索算法
- 排名搜索 - 首先返回最佳结果
- 许多强大的查询类型：短语查询，通配符查询，邻近查询，范围查询等
- 字段（fielded）搜索（例如标题，作者，内容）
- 按任何属性（field）排序
- 使用合并结果进行多索引搜索
- 允许同时更新和搜索
- 灵活的分面，高亮显示，joins和结果分组
- 可插拔排名模型，包括矢量空间模型和Okapi BM25
- 可配置存储引擎（编解码器）
## 什么是全文搜索？
	数据的分类：
	我们生活中的数据总体分为两种：结构化数据和非结构化数据。
　　（1）结构化数据：指具有固定格式或有限长度的数据，如数据库，元数据等。
　　（2）非结构化数据：指不定长或无固定格式的数据，如邮件，word文档等磁盘上的文件
    结构化数据查询方法
		数据库搜索
　　		数据库中的搜索很容易实现，通常都是使用sql语句进行查询，而且能很快的得到查询结果。
　　		因为数据库中的数据存储是有规律的，有行有列而且数据格式、数据长度都是固定的。
	非结构化数据查询方法
		（1）顺序扫描法(Serial Scanning)
　　		所谓顺序扫描，比如要找内容包含某一个字符串的文件，就是一个文档一个文档的看，对于每一个文档，从头看到尾，如果此文档包含此字符串，
			则此文档为我们要找的文件，接着看下一个文件，直到扫描完所有的文件。如利用windows的搜索也可以搜索文件内容，只是相当的慢。
　　	（2）全文检索(Full-text Search)
　　		将非结构化数据中的一部分信息提取出来，重新组织，使其变得有一定结构，然后对此有一定结构的数据进行搜索，从而达到搜索相对较快的目的。
			这部分从非结构化数据中提取出的然后重新组织的信息，我们称之索引。
			例如：字典。字典的拼音表和部首检字表就相当于字典的索引，对每一个字的解释是非结构化的，如果字典没有音节表和部首检字表，
			在茫茫辞海中找一个字只能顺序扫描。然而字的某些信息可以提取出来进行结构化处理，比如读音，就比较结构化，分声母和韵母，
			分别只有几种可以一一列举，于是将读音拿出来按一定的顺序排列，每一项读音都指向此字的详细解释的页数。我们搜索时按结构化的拼音搜到读音，
			然后按其指向的页数，便可找到我们的非结构化数据——也即对字的解释。
			
	　　这种先建立索引，再对索引进行搜索的过程就叫全文检索(Full-text Search)。
	　　虽然创建索引的过程也是非常耗时的，但是索引一旦创建就可以多次使用，全文检索主要处理的是查询，所以耗时间创建索引是值得的。


## 全文检索的应用场景
　　对于数据量大、数据结构不固定的数据可采用全文检索方式搜索，比如百度、Google等搜索引擎、论坛站内搜索、电商网站站内搜索等。

## Lucene实现全文检索的流程
	1. 创建索引
	  >  获得原始文档
		 原始文档是指要索引和搜索的内容。原始内容包括互联网上的网页、数据库中的数据、磁盘上的文件等。Lucene不提供信息采集的类库,需要自己实现。
	  >  创建文档对象
         获取原始内容的目的是为了索引，在索引前需要将原始内容创建成文档（Document），文档中包括一个一个的域（Field），域中存储内容。
		 这里我们可以将磁盘上的一个文件当成一个document，
		 Document中包括一些Field（file_name文件名称、file_path文件路径、file_size文件大小、file_content文件内容）
		 注意：（1）每个Document可以有多个Field
　　　　　		（2）不同的Document可以有不同的Field
　　　　　		（3）同一个Document可以有相同的Field（域名和域值都相同）
　　　　　		（4）每个文档都有一个唯一的编号，就是文档id。
      >  分析文档
         将原始内容创建为包含域（Field）的文档（document），需要再对域中的内容进行分析，
		 分析的过程是经过对原始文档提取单词、将字母转为小写、去除标点符号、去除停用词等过程生成最终的语汇单元，可以将语汇单元理解为一个一个的单词。
　　	 比如下边的文档经过分析如下：
　　	 原文档内容：
　　		Lucene is a Java full-text search engine. 
　　	 分析后得到的语汇单元：
　　	    lucene、java、full、search、engine
　　     每个单词叫做一个Term，不同的域中拆分出来的相同的单词是不同的term。term中包含两部分一部分是文档的域名，另一部分是单词的内容。
　　	 例如：文件名中包含apache和文件内容中包含的apache是不同的term。	
      >  创建索引
         对所有文档分析得出的语汇单元进行索引，索引的目的是为了搜索，最终要实现只搜索被索引的语汇单元从而找到Document（文档）。	  
		 注意：
		   （1）创建索引是对语汇单元索引，通过词语找文档，这种索引的结构叫倒排索引结构(Inverted index)。
　　　　　	 （2）传统方法是根据文件找到该文件的内容，在文件内容中匹配搜索关键字，这种方法是顺序扫描方法，数据量大、搜索慢。
　　        （3）倒排索引结构是根据内容（词语）找文档，
		   （4）倒排索引结构也叫反向索引结构，包括索引和文档两部分，索引即词汇表，它的规模较小，而文档集合较大。 
	2. 查询索引
	   查询索引也是搜索的过程。搜索就是用户输入关键字，从索引（index）中进行搜索的过程。根据关键字搜索索引，根据索引找到对应的文档，
	   从而找到要搜索的内容。对要搜索的信息创建Query查询对象，Lucene会根据Query查询对象生成最终的查询语法，
	   类似关系数据库Sql语法一样Lucene也有自己的查询语法，比如：“name:lucene”表示查询Field的name为“lucene”的文档信息。
	  > 用户查询接口
		 全文检索系统提供用户搜索的界面供用户提交搜索的关键字，搜索完成展示搜索结果。
　　     比如： 百度搜索
　　     Lucene不提供制作用户搜索界面的功能，需要根据自己的需求开发搜索界面。
      > 创建查询
	    用户输入查询关键字执行搜索之前需要先构建一个查询对象，查询对象中可以指定查询要搜索的Field文档域、查询关键字等，查询对象会生成具体的查询语法，
　　    例如： 语法 “fileName:lucene”表示要搜索Field域的内容为“lucene”的文档
      > 执行查询
	    搜索索引过程：
　　	根据查询语法在倒排索引词典表中分别找出对应搜索词的索引，从而找到索引所链接的文档链表。
	　　比如搜索语法为“fileName:lucene”表示搜索出fileName域中包含Lucene的文档。
	　　搜索过程就是在索引上查找域为fileName，并且关键字为Lucene的term，并根据term找到文档id列表。
	3. 删除索引
	   > 删除全部索引
	   > 指定查询条件删除
	4. 索引库的修改
	   > 更新的原理就是先删除再添加

	
## 倒排索引 

![倒排索引数据结构](../static/images/lucene/lucene.png "倒排索引数据结构")

“倒排索引”是垃圾翻译导致无法见名知意甚至曲解含义的典型代表。
英文原名 Inverted index，大概因为 Invert 有颠倒的意思，就被翻译成了倒排。但是倒排这个名称很容易让人理解为从A-Z颠倒成Z-A。
个人认为翻译成反向索引可能比较合适。一个未经处理的数据库中，一般是以文档ID作为索引，以文档内容作为记录。
而Inverted index 指的是将单词或记录作为索引，将文档ID作为记录，这样便可以方便地通过单词或记录查找到其所在的文档。

 ## Lucene核心类
	> Document
	  一个Lucene Document 是索引中的记录。文档有一个字段列表; 每个字段都有一个名称和一个文本值。
	> Filed
	  文档的Filed子类分别有
		{@link TextField}: {@link Reader} or {@link String} indexed for full-text search
		{@link StringField}: {@link String} indexed verbatim as a single token
		{@link IntPoint}: {@code int} indexed for exact/range queries.
		{@link LongPoint}: {@code long} indexed for exact/range queries.
		{@link FloatPoint}: {@code float} indexed for exact/range queries.
		{@link DoublePoint}: {@code double} indexed for exact/range queries.
		{@link SortedDocValuesField}: {@code byte[]} indexed column-wise for sorting/faceting
		{@link SortedSetDocValuesField}: {@code SortedSet<byte[]>} indexed column-wise for sorting/faceting
		{@link NumericDocValuesField}: {@code long} indexed column-wise for sorting/faceting
		{@link SortedNumericDocValuesField}: {@code SortedSet<long>} indexed column-wise for sorting/faceting
		{@link StoredField}: Stored-only value for retrieving in summary results	
	    
	> Term
	  一个Term是Lucene索引的最小单元
	> Directory
	> IndexReader
	  写索引的类
	> IndexSearcher
	  读索引的类
	> Query
	  查询的公共抽象类，子类分别有
	   TermQuery
       BooleanQuery
       WildcardQuery
       PhraseQuery
       PrefixQuery
       MultiPhraseQuery
       FuzzyQuery
       RegexpQuery
       TermRangeQuery
       PointRangeQuery
       ConstantScoreQuery
       DisjunctionMaxQuery
       MatchAllDocsQuery
	> TopDocs
	  查询命中的对象id集合

## Lucene文件
[官方描述文档](https://lucene.apache.org/core/8_11_1/core/org/apache/lucene/codecs/lucene87/package-summary.html#package.description '')


### Definitions
The fundamental concepts in Lucene are index, document, field and term.
- An index contains a sequence of documents.
- A document is a sequence of fields.
- A field is a named sequence of terms.
- A term is a sequence of bytes.


### Segment 
A segment is very simply a section of the index. The idea is that you can add documents to the index that's currently being served by creating a new segment with only new documents in it. This way, you don't have to go to the expensive trouble of rebuilding your entire index frequently in order to add new documents to the index.

A Lucene segment is part of an Index. Each segment is composed of several index files. If you look inside any of these files, you will see that it holds 1 or more [Lucene documents](https://lucene.apache.org/core/8_11_1/core/org/apache/lucene/codecs/lucene87/package-summary.html#package.description '').

```
+- Index 5 ------------------------------------------+
|                                                    |
|  +- Segment _0 ---------------------------------+  |
|  |                                              |  |
|  |  +- file 1 -------------------------------+  |  |
|  |  |                                        |  |  |
|  |  | +- L.Doc1-+  +- L.Doc2-+  +- L.Doc3-+  |  |  |
|  |  | |         |  |         |  |         |  |  |  |
|  |  | | field 1 |  | field 1 |  | field 1 |  |  |  |
|  |  | | field 2 |  | field 2 |  | field 2 |  |  |  |
|  |  | | field 3 |  | field 3 |  | field 3 |  |  |  |
|  |  | |         |  |         |  |         |  |  |  |
|  |  | +---------+  +---------+  +---------+  |  |  |
|  |  |                                        |  |  |
|  |  +----------------------------------------+  |  |
|  |                                              |  |
|  |                                              |  |
|  |  +- file 2 -------------------------------+  |  |
|  |  |                                        |  |  |
|  |  | +- L.Doc4-+  +- L.Doc5-+  +- L.Doc6-+  |  |  |
|  |  | |         |  |         |  |         |  |  |  |
|  |  | | field 1 |  | field 1 |  | field 1 |  |  |  |
|  |  | | field 2 |  | field 2 |  | field 2 |  |  |  |
|  |  | | field 3 |  | field 3 |  | field 3 |  |  |  |
|  |  | |         |  |         |  |         |  |  |  |
|  |  | +---------+  +---------+  +---------+  |  |  |
|  |  |                                        |  |  |
|  |  +----------------------------------------+  |  |
|  |                                              |  |
|  +----------------------------------------------+  |
|                                                    |
|  +- Segment _1 (optional) ----------------------+  |
|  |                                              |  |
|  +----------------------------------------------+  |
+----------------------------------------------------+
```


### Summary of File Extensions
|名称|文件后缀|描述|
|-|-|-|
|Segments File| segments_N| Sotres information about a commit point|
|Lock File    | write.lock| The Write lock prevents multiple IndexWriters from writing to the same file|
|Segment info | .si       | Stores metadata about a segment|
|Compound file| .cfs,.cfe | An optional "virtual" file consisting of all the other index files for systems that frequently run out of file handles|
|Fields		  | .fnm      | Stores information about the fields|
|Field Index  | .fdx      | Contains pointers to field data|
|Field Data   | .fdt      | The stored fields for documents|
|Field Meta   | .fdm      | extension of stored fields meta|
|Term Dictionary| .tim    | The term dictionary.stores term info|
|Term index   | .tip      | The index into the Term Dictionary|
|Frequencies  | .doc      | Contains the list of docs which contain each term along with frequency|
|Positions    | .pos      | Stores position information about where a term occurs in the index|
|Payloads     | .pay      | Stores additional per-position metadata information such as character offsets and user payloads|
|Norms        | .nvd,.nvm | Encodes length and boost factors for docs and fields|
|Per-Document Values|.dvd,.dvm|Encodes additional scoring factors or other per-document information|
|Term Vector Index|.tvx   | Stores offset into the document data file|
|Term Vector Data| .tvd   | Contains term vector data|
|Live documents | .liv    | Info about what documents are live|
|Point values| .dii,.dim  | Holds Indexed points,if any|



### 代码


