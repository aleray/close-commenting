Close Commenting is a simple text-publishing Django application enabling per paragraph comments.

The idea started about 2 years ago for [Issue Magazine][4]

A demo is available here: [http://closecommenting.stdin.fr/one-possible-scenario-for-a-collective-future.html][1]

Features
========

  - Markdown syntax
  - Dublin Core Metadata embeded in the textual content via the Markdown metadata extension
  - Automatic splitting of the paragraphs (first level HTML tags)
  - Paragraph comments linked to the paragraphs through their MD5 hash. One can edit the text and its non modified paragraphs will still be linked to the existing comments.
  - Threaded comments
  - General comments, Paragraph comments and comment comments

Related projects
================

  - If:book [Comment Press][2]
  - Sopinspace [Co-ment][3]


  [1]: http://closecommenting.stdin.fr/one-possible-scenario-for-a-collective-future.html
  [2]: http://www.futureofthebook.org/commentpress/
  [3]: http://www.co-ment.net/
  [4]: http://www.issue-magazine.net/
