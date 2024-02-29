---
layout: post
title:  "Markdown基本语法"
date:   2021-02-10 10:34:15 +0800
categories: markdown
tags: markdown
permalink: /markdown/base-syntax
published: true
publish_file: 2021-02-10-markdown-base-syntax.md
toc: true
---
# Markdown基本语法

## 起源

John Gruber 在2004年创建了Markdown，并与Aaron Swartz合作定义了语法。目标是为了创建一种易读且易写的纯文本格式，并可以转换成XHTML或HTML。


## 语法

此语法翻译自[官方文档][markdown-official-manual] ，英语比较好的可以直接跳转到此网站来学习。

[markdown-official-manual]: https://daringfireball.net/projects/markdown/syntax "Markdown官方文档"

### 概览

#### 哲学

Markdown旨在尽可能地易于阅读和编写。

但是，首先要强调可读性。Markdown格式的文档应以纯文本形式原样发布，而不会看起来像被标签或格式说明所标记。虽然Markdown的语法受到了几种现有的文本到HTML过滤器的影响，包括Setext，atx，Textile，reStructuredText， Grutatext和EtText  ，但Markdown语法的最大灵感来源就是纯文本电子邮件的格式。

为此，Markdown的语法完全由标点符号组成，这些标点符号经过精心选择，以使其看起来像它们的含义。例如，单词周围的星号实际上看起来像*强调*。Markdown列表看起来很像列表。假设您曾经使用过电子邮件，即使是块引用也看起来像是引用的文本段落。

  [1]: http://docutils.sourceforge.net/mirror/setext.html
  [2]: http://www.aaronsw.com/2002/atx/
  [3]: http://textism.com/tools/textile/
  [4]: http://docutils.sourceforge.net/rst.html
  [5]: http://www.triptico.com/software/grutatxt.html
  [6]: http://ettext.taint.org/doc/

#### 内联HTML

Markdown的语法仅用于一个目的: 用作*编写*web页面的格式。

Markdown 不是HTML的替代品，也不会替掉HTML。它的语法非常精简, 对应于HTML标签非常小的子集。 这个想法不是要创建一种使插入HTML标签更容易的语法。HTML标签已经很容易插入了。Markdown的想法是使其易于阅读，编写和编辑文章。HTML*发布的* 格式; Markdown是*编写的*
格式. 因此, Markdown的格式语法仅解决以纯文本形式传达的问题。

对于Markdown语法未涵盖的标记，您只需使用HTML本身的就可以了。 无需在其前添加或定界以表明您已从Markdown切换为HTML；您只需要使用标签即可。

唯一的限制是块级HTML元素-例如`<div>`,
`<table>`, `<pre>`, `<p>`等-必须在前后用空行分离，并且该块的开始和结束标签不应用制表符或空格缩进。 Markdown非常聪明，不会在HTML块级标签周围添加额外的（不需要的）`<p>`标签。

例如，要将HTML表格添加到Markdown文章中：

    This is a regular paragraph.

    <table>
        <tr>
            <td>Foo</td>
        </tr>
    </table>

    This is another regular paragraph.

请注意，Markdown格式语法不会在块级HTML标签中被解析。例如，您不能在HTML块内使用Markdown样式*emphasis*。

HTML行内标签（例如`<span>`，`<cite>`或`<del>` ）可以在Markdown段落，列表项或标题中的任何位置使用。如果需要，甚至可以使用HTML标签替换Markdown格式。例如，如果您希望使用HTML`<a>`或`<img>`标签而不是Markdown的链接或图像语法。

#### 自动转义特殊字符

在HTML中，有两个字符需要特殊处理: `<`和 `&`. 左尖括号用于开始标签; “与”号表示HTML实体。如果要将它们用作文字字符，则必须将它们作为实体转义，例如`&lt;`和 `&amp;`。


＆符出现的频率比较高。 如果要写“ AT＆T”， 你需要写成 '`AT&amp;T`'. 您甚至需要转义URL中的“＆”号。因此，如果您想链接到:

    http://images.google.com/images?num=30&q=larry+bird

您需要将URL编码为：

    http://images.google.com/images?num=30&amp;q=larry+bird

Markdown允许您正常地使用这些字符，并为您进行所有必要的转义。如果将与号用作HTML实体的一部分，则它保持不变。否则将被翻译成`&amp;`。

因此，如果您想在文章中包含版权符号，可以编写：

    &copy;

Markdown将不理会它。但是，如果您写：

    AT&T

Markdown会将其转换为：

    AT&amp;T

同样，由于Markdown支持 [内联HTML](#html), 如果您将尖括号用作HTML标签的定界符，则Markdown会将它们视为此类。但是，如果您写：

    4 < 5

Markdown会将其转换为：

    4 &lt; 5

但是，在Markdown代码内部，尖括号和与号始终自动进行编码。这使得使用Markdown编写HTML代码变得容易。

* * *

### 块元素

#### 段落和换行符

段落是一个或多个连续的文本行，由一个或多个空行分隔。（空行是看起来像空行的任何行，仅包含空格或制表符的行被视为空白。）普通段落不应以空格或制表符缩进。

当您确实想使用Markdown插入`<br />`标记时，请以两个或多个空格结束一行，然后键入return。

是的，这需要花费更多的精力来创建`<br />`，但是简单的“每条换行符是一个`<br />`”规则对Markdown不起作用。Markdown的电子邮件样式的[块引用][bq]和多段落[列表项][l] 在经过艰苦的格式化后，效果最佳，并且外观更好。

  [bq]: #blockquote
  [l]:  #list


#### 标题

Markdown 支持两种样式的标题, [Setext][1] 和 [atx][2].

Setext样式的标题使用等号（一级标题）和破折号（二级标题）“加下划线”。例如：

    This is an H1
    =============

    This is an H2
    -------------

任何数量的下划线 `=`或者`-`都可以。

Atx样式的标题在行的开头使用1-6个哈希字符，对应于标题级别1-6。例如：

    # This is an H1

    ## This is an H2

    ###### This is an H6

（可选）您可以“结束” atx样式的标题。这纯粹是装饰性的-如果您认为它看起来更好，则可以使用它。结束的哈希字符甚至数量上不需要跟打开的哈希字符一致。（打开的哈希字符数量的数量确定标题的级别。）：

    # This is an H1 #

    ## This is an H2 ##

    ### This is an H3 ######

#### 块引用

Markdown使用电子邮件样式的`>`字符进行块引用。如果您熟悉在电子邮件中引用文本段落的内容，那么您将知道如何在Markdown中创建块引用。如果将文本用硬包装并在每行行首写一个`>`，则看起来最好：

    > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
    > consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
    > Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    > 
    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
    > id sem consectetuer libero luctus adipiscing.

Markdown可以让您变得懒惰，并且只在硬包装段落的第一行行首放置`>`：

    > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
    consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
    Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
    id sem consectetuer libero luctus adipiscing.

可以通过再添加`>`字符来嵌套块引用：

    > 这是第一层块引用。
    >
    > > 这是嵌套的块引用。
    >
    > 返回第一层块引用。

块引用可以包含其他Markdown元素，包括标题，列表和代码块：

	> ## 这是一个标题
	> 
	> 1.   This is the first list item.
	> 2.   This is the second list item.
	> 
	> Here's some example code:
	> 
	>     return shell_exec("echo $input | $markdown_script");

#### 列表

Markdown 支持有序列表和无序列表。

无序列表使用星号，加号和连字符（可互换）作为列表标记：

    *   Red
    *   Green
    *   Blue

等效于：

    +   Red
    +   Green
    +   Blue

和：

    -   Red
    -   Green
    -   Blue

有序列表使用数字后跟句点：

    1.  Bird
    2.  McHale
    3.  Parish

需要注意的是，用于标记列表的实际数字对Markdown产生的HTML输出没有影响。从上面的列表中产生的HTML是：

    <ol>
    <li>Bird</li>
    <li>McHale</li>
    <li>Parish</li>
    </ol>

如果你在Markdown中像下面这样写列表：

    1.  Bird
    1.  McHale
    1.  Parish

甚至是：

    3. Bird
    1. McHale
    8. Parish

您将获得完全相同的HTML输出。关键是，如果需要，在Markdown中使用从1开始的有序数字，这样源文件中的数字和HTML中输出的数字是匹配的。但是，如果您比较懒的话，就不必这样做。

列表标记通常从左边缘开始，但最多可以缩进三个空格。列表标记后必须跟一个或多个空格或一个制表符。


为了使列表看起来更好，您可以使用缩进的行包装一下：

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
        viverra nec, fringilla in, laoreet vitae, risus.
    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
        Suspendisse id sem consectetuer libero luctus adipiscing.

但是如果你比较懒的话，则不必这样做:

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.

如果列表项用空行分隔，则Markdown会将每一项的内容包装在HTML的`<p>`标签中。例如输入：

    *   Bird
    *   Magic

会得到:

    <ul>
    <li>Bird</li>
    <li>Magic</li>
    </ul>

但是这样的话:

    *   Bird

    *   Magic

会得到:

    <ul>
    <li><p>Bird</p></li>
    <li><p>Magic</p></li>
    </ul>

列表项可能包含多个段落。列表项中的每个后续段落都必须缩进4个空格或一个制表符：

    1.  This is a list item with two paragraphs. Lorem ipsum dolor
        sit amet, consectetuer adipiscing elit. Aliquam hendrerit
        mi posuere lectus.

        Vestibulum enim wisi, viverra nec, fringilla in, laoreet
        vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
        sit amet velit.

    2.  Suspendisse id sem consectetuer libero luctus adipiscing.

如果您缩进后续段落的每一行，这看起来很不错，但是Markdown可以让你更懒一些：

    *   This is a list item with two paragraphs.

        This is the second paragraph in the list item. You're
    only required to indent the first line. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit.

    *   Another item in the same list.

要在列表项中放置一个块引用，需要缩进(一个制表符或者4个空格)块引用的分隔符`>`：

    *   A list item with a blockquote:

        > This is a blockquote
        > inside a list item.

要将代码块放入列表项中，需要将代码块缩进*两次* -8个空格或两个制表符：

    *   A list item with a code block:

            <code goes here>

值得注意的是，可以通过编写如下文本来无意触发有序列表：

    1986. What a great season.

换句话说，在行的开头是一个*数字*。为了避免这种情况，您可以反斜杠转义该句点：

    1986\. What a great season.


#### 代码块

预格式化的代码块用于编写有关编程的源代码。Markdown将代码块包装在`<pre>`和`<code>`标记中。

要在Markdown中生成代码块，只需将代码块的每一行缩进至少4个空格或1个制表符。例如：

    This is a normal paragraph:

        This is a code block.

Markdown将生成：

    <p>This is a normal paragraph:</p>

    <pre><code>This is a code block.
    </code></pre>

在代码块内，`＆`符号和尖括号（`<`和`>`）会自动转换为HTML实体。这使得使用Markdown包含示例HTML源代码变得非常容易-只需粘贴并缩进即可，Markdown将解决对＆字符和尖括号进行编码的麻烦。例如：

        <div class="footer">
            &copy; 2004 Foo Corporation
        </div>

会转换成:

    <pre><code>&lt;div class="footer"&gt;
        &amp;copy; 2004 Foo Corporation
    &lt;/div&gt;
    </code></pre>

代码块中不解析Makrdown语法。例如，星号只是代码块中的文字星号。
这意味着使用Markdown编写Markdown自己的语法也很容易。


#### 水平线

您可以通过在一行上单独放置三个或多个连字符，星号或下划线来生成水平线`<hr />`。如果需要，可以在连字符或星号之间使用空格：

    * * *

    ***

    *****

    - - -

    ---------------------------------------


### 行内元素

#### 超链接

Markdown支持两种超链接样式: *inline* and *reference*.

在两种样式中，链接文本均由[方括号]分隔。

要创inline链接，在链接文本的右方括号后立即使用一组圆括号。在圆括号内，指定URL地址，以及链接的标题，并用引号引起来。例如：

    This is [an example](http://example.com/ "Title") inline link.

    [This link](http://example.net/) has no title attribute.

会被转换成:

    <p>This is <a href="http://example.com/" title="Title">
    an example</a> inline link.</p>

    <p><a href="http://example.net/">This link</a> has no
    title attribute.</p>

样式链接使用第二组方括号，在其中放置您选择的标签以标识该链接：

    See my [About](/about/) page for details.   

Reference样式链接在第二组方括号中输入链接的id：

    This is [an example][id] reference-style link.

您可以选择使用空格来分隔各组括号：

    This is [an example] [id] reference-style link.

然后，在文档中的任何位置，都可以单独在一行上定义这样的链接Id：

    [id]: http://example.com/  "Optional Title Here"

语法:

*   包含链接标识符的方括号（可选，从左边距缩进，最多三个空格）；
*   然后跟着冒号；
*   然后是一个或多个空格（或制表符）；
*   然后是链接的网址；
*   （可选）后跟链接的标题属性，用双引号或单引号引起来，或用括号引起来。

以下三个链接定义是等效的：

	[foo]: http://example.com/  "Optional Title Here"
	[foo]: http://example.com/  'Optional Title Here'
	[foo]: http://example.com/  (Optional Title Here)

**注意:** Markdown.pl 1.0.1中存在一个已知的bug，该bug可防止使用单引号来分隔链接标题。

T链接URL可以选择用尖括号括起来：

    [id]: <http://example.com/>  "Optional Title Here"

您可以将title属性放在下一行，并使用额外的空格或制表符进行填充，这对于较长的URL而言往往看起来更好：

    [id]: http://example.com/longish/path/to/resource/here
        "Optional Title Here"

链接定义仅在Markdown处理期间用于创建链接，并在HTML输出中从文档中删除。

链接定义id可以包含字母，数字，空格和标点符号，但它们不区分大小写。例如，这两个链接：

	[link text][a]
	[link text][A]

是等效的。

在*隐式链接名称*快捷键可以让你忽略的链接，在这种情况下，链接文本本身作为名称的名称。只需使用一组空的方括号-例如，将“ Google”一词链接到google.com网站，您可以简单地编写：

	[Google][]

然后定义链接：

	[Google]: http://google.com/

由于链接名称可能包含空格，因此此快捷方式甚至适用于链接文本中的多个单词：

	Visit [Daring Fireball][] for more information.

然后定义链接：
	
	[Daring Fireball]: http://daringfireball.net/

链接定义可以放在Markdown文档中的任何位置。我倾向于将它们放在使用它们的每个段落之后，但是如果需要，可以将它们全部放在文档的末尾，就像脚注一样。

这是一个实际的参考链接示例：

    I get 10 times more traffic from [Google] [1] than from
    [Yahoo] [2] or [MSN] [3].

      [1]: http://google.com/        "Google"
      [2]: http://search.yahoo.com/  "Yahoo Search"
      [3]: http://search.msn.com/    "MSN Search"

使用隐式链接名称快捷方式，您可以编写：

    I get 10 times more traffic from [Google][] than from
    [Yahoo][] or [MSN][].

      [google]: http://google.com/        "Google"
      [yahoo]:  http://search.yahoo.com/  "Yahoo Search"
      [msn]:    http://search.msn.com/    "MSN Search"

上面的两个示例都将产生以下HTML输出：

    <p>I get 10 times more traffic from <a href="http://google.com/"
    title="Google">Google</a> than from
    <a href="http://search.yahoo.com/" title="Yahoo Search">Yahoo</a>
    or <a href="http://search.msn.com/" title="MSN Search">MSN</a>.</p>

为了进行比较，以下是使用Markdown的链接样式编写的同一段落：

    I get 10 times more traffic from [Google](http://google.com/ "Google")
    than from [Yahoo](http://search.yahoo.com/ "Yahoo Search") or
    [MSN](http://search.msn.com/ "MSN Search").

reference样式的链接并不是要更容易编写。关键是，通过reference样式的链接，您的文档更具可读性。比较上面的示例：使用reference样式的链接，段落本身只有81个字符；而使用inline样式的链接，为176个字符；作为原始HTML，它是234个字符。在原始HTML中，标记多于文本。

借助Markdown的refrence样式链接，源文档与浏览器中呈现的最终输出更加相似。通过允许您将与标记相关的元数据移出该段落，您可以添加链接而不会中断文章的叙述流程。


#### 强调

Markdown将星号（`*`）和下划线（`_`）作为强调标识。用`*`或`_`包裹的文本将带有HTML`<em>`标记；两个`*`或`_`会被HTML`<strong>`标签包裹 。例如，此输入：

    *single asterisks*

    _single underscores_

    **double asterisks**

    __double underscores__

将生成：

    <em>single asterisks</em>

    <em>single underscores</em>

    <strong>double asterisks</strong>

    <strong>double underscores</strong>

您可以使用任何喜欢的样式。唯一的限制是必须使用相同的字符来打开和关闭。

强调可以用在单词的中间：

    un*frigging*believable

但是，如果用`*`或`_`包围空格，它将被视为文字星号或下划线。

要在原本会用作强调定界符的位置产生文字星号或下划线，可以反斜杠对其进行转义：

    \*this text is surrounded by literal asterisks\*


#### 代码

要指出代码的范围，请用反引号（`）将其引起来。与预格式化的代码块不同，这种方式指示正常段落中的代码。例如：

    Use the `printf()` function.

将生成:

    <p>Use the <code>printf()</code> function.</p>

要在代码范围内包含文字反引号字符，可以使用多个反引号作为开始和结束定界符：

    ``There is a literal backtick (`) here.``

将生成:

    <p><code>There is a literal backtick (`) here.</code></p>

围绕代码范围的反引号分隔符可以包含空格-一个在打开之后，一个在关闭之前。
这使您可以将原义的反引号字符放在代码段的开头或结尾：

	A single backtick in a code span: `` ` ``
	
	A backtick-delimited string in a code span: `` `foo` ``

将生成:

	<p>A single backtick in a code span: <code>`</code></p>
	
	<p>A backtick-delimited string in a code span: <code>`foo`</code></p>

通过代码块，“＆”号和尖括号被自动编码为HTML实体，这使得添加示例HTML标签变得容易：

    Please don't use any `<blink>` tags.

将生成:

    <p>Please don't use any <code>&lt;blink&gt;</code> tags.</p>

您可以这样写：

    `&#8212;` is the decimal-encoded equivalent of `&mdash;`.

将生成:

    <p><code>&amp;#8212;</code> is the decimal-encoded
    equivalent of <code>&amp;mdash;</code>.</p>

#### 图片

说实话，很难设计出一种“自然”的语法来将图像放入纯文本文档格式中。

Markdown使用一种类似于链接语法的图像语法，允许两种样式：*inline*和*reference*。.

Inline图像语法如下所示：

    ![Alt text](/path/to/img.jpg)

    ![Alt text](/path/to/img.jpg "Optional title")

语法是:

*   感叹号：`!`;
*   随后是一组方括号，其中包含图像的`alt` 属性文本；
*   后跟一组括号，其中包含图像的URL或路径，以及`title`用双引号或单引号引起来的可选属性。

Reference样式的图像语法如下所示：

    ![Alt text][id]

其中“ id”是已定义图像参考的名称。使用与链接引用相同的语法来定义图像引用：

    [id]: url/to/image  "Optional title attribute"

在撰写本文时，Markdown尚无用于指定图像尺寸的语法。如果这对您很重要，则可以简单地使用常规HTML`<img>`标记。

### 其它

#### 自动链接

Markdown支持为URL和电子邮件地址创建“自动”链接的快捷方式：只需用尖括号将URL或电子邮件地址括起来即可。这意味着如果您想显示URL或电子邮件地址的实际文本，并且还希望将其作为可点击的链接，则可以执行以下操作：

    <http://example.com/>
    
Markdown会将其转换为：

    <a href="http://example.com/">http://example.com/</a>

电子邮件地址的自动链接的工作方式类似，不同之处在于Markdown还将执行一些随机的十进制和十六进制实体编码，以帮助躲避邮件地址收集机器人。例如，

    <address@example.com>

Markdown会将其变为：

    <a href="&#x6D;&#x61;i&#x6C;&#x74;&#x6F;:&#x61;&#x64;&#x64;&#x72;&#x65;
    &#115;&#115;&#64;&#101;&#120;&#x61;&#109;&#x70;&#x6C;e&#x2E;&#99;&#111;
    &#109;">&#x61;&#x64;&#x64;&#x72;&#x65;&#115;&#115;&#64;&#101;&#120;&#x61;
    &#109;&#x70;&#x6C;e&#x2E;&#99;&#111;&#109;</a>

它将在浏览器中呈现为“ address@example.com ”的可点击链接。

（这种实体编码技巧的确会愚弄很多（即使不是大多数）邮件地址收集机器人，但绝对不会愚弄所有。不过总比没有好，但是以这种方式发布的地址最终可能会开始收到垃圾邮件。）

#### 反斜杠转义符

Markdown允许您使用反斜杠转义符来生成文字字符，否则这些文字在Markdown的格式语法中将具有特殊含义。例如，如果您想在单词周围加上文字星号（而不是HTML`<em>`标签），则可以在星号之前使用反斜杠，如下所示：

    \*literal asterisks\*

Markdown为以下字符提供了反斜杠转义：

    \   backslash
    `   backtick
    *   asterisk
    _   underscore
    {}  curly braces
    []  square brackets
    ()  parentheses
    #   hash mark
	+   plus sign
	-   minus sign (hyphen)
    .   dot
    !   exclamation mark


## 扩展

Markdown创建之后由于其简介的语法和高效的编写文档方式，迅速的流行起来。不过由于缺少一些类型的定义（比如 音频和视频的引入），一些网站根据自己的实际场景出现了很多语法的变种：

- [github][]
- [StackOverflow][]
- [SourceForge][]

[github]: <https://stackoverflow.com/editing-help>
[StackOverflow]: <http://sourceforge.net/p/forge/documentation/markdown_syntax/>
[SourceForge]: <http://sourceforge.net/p/forge/documentation/markdown_syntax/>   


因此Markdown算是给了一种思想，一种方便写文章、博客的方式，如果Markdown的语法满足不了你的使用场景，
你也可以自己来扩展他


## 友情链接

[Markdown在线编辑器](https://md.poul.top)
