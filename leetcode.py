import requests


def _parse_daily_response(response):
    """
    Response looks like:
    {
      'data': {
        'activeDailyCodingChallengeQuestion': {
          'date': '2022-04-17',
          'link': '/problems/increasing-order-search-tree/',
          'question': {
            'acRate': 77.39213625240198,
            'likes': 2770,
            'dislikes': 617,
            'stats': '{"totalAccepted": "187.8K", "totalSubmission": "242.8K", "totalAcceptedRaw": 187848, "totalSubmissionRaw": 242845, "acRate": "77.4%"}',
            'difficulty': 'Easy',
            'frontendQuestionId': '897',
            'title': 'Increasing Order Search Tree',
            'titleSlug': 'increasing-order-search-tree',
            'content': '<p>Given the <code>root</code> of a binary search tree, rearrange the tree in <strong>in-order</strong> so that the leftmost node in the tree is now the root of the tree, and every node has no left child and only one right child.</p>\r\n\r\n<p>&nbsp;</p>\r\n<p><strong>Example 1:</strong></p>\r\n<img alt="" src="https://assets.leetcode.com/uploads/2020/11/17/ex1.jpg" style="width: 600px; height: 350px;" />\r\n<pre>\r\n<strong>Input:</strong> root = [5,3,6,2,4,null,8,1,null,null,null,7,9]\r\n<strong>Output:</strong> [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]\r\n</pre>\r\n\r\n<p><strong>Example 2:</strong></p>\r\n<img alt="" src="https://assets.leetcode.com/uploads/2020/11/17/ex2.jpg" style="width: 300px; height: 114px;" />\r\n<pre>\r\n<strong>Input:</strong> root = [5,1,7]\r\n<strong>Output:</strong> [1,null,5,null,7]\r\n</pre>\r\n\r\n<p>&nbsp;</p>\r\n<p><strong>Constraints:</strong></p>\r\n\r\n<ul>\r\n\t<li>The number of nodes in the given tree will be in the range <code>[1, 100]</code>.</li>\r\n\t<li><code>0 &lt;= Node.val &lt;= 1000</code></li>\r\n</ul>',
            'hints': [],
            'topicTags': [
              {
                'name': 'Stack'
              },
              {
                'name': 'Tree'
              },
              {
                'name': 'Depth-First Search'
              },
              {
                'name': 'Binary Search Tree'
              },
              {
                'name': 'Binary Tree'
              }
            ]
          }
        }
      }
    }
    """
    ch = response.get('data', {}).get('activeDailyCodingChallengeQuestion', {})
    q = ch.get('question', {})
    return '{num}. {title}\nRating: 👍 {likes} | 👎 {dislikes}\nDifficulty: {dif}\nAcceptance: {acRate}%'.format(
        num=q.get('frontendQuestionId'),
        title=q.get('title'),
        dif=q.get('difficulty'),
        likes=q.get('likes'),
        dislikes=q.get('dislikes'),
        acRate=q.get('acRate'),
    )


def get_daily():
    response = requests.post(
        'https://leetcode.com/graphql/',
        json={
            'query': "\n    query questionOfToday {\n  activeDailyCodingChallengeQuestion {\n    date\n    link\n    question {\n      acRate\n      likes\n      dislikes\n      stats\n      difficulty\n      frontendQuestionId: questionFrontendId\n      title\n      titleSlug\n      content\n      hints\n      topicTags {\n        name\n      }\n    }\n  }\n}\n    ",
            'variables': {}
        },
    )
    return _parse_daily_response(response.json())
