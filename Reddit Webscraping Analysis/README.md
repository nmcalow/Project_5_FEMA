##Description: 

This project is all about understanding Reddit's many twists and turns through webscraping, natural language processing, and model building. To this end I analyzed posts from r/tifu and r/NoStupidQuestions, returning with a perfect model, which I then made less perfect by intentionally removing some key features, and working the model again until it was mostly perfect. 

Data Dictionary: 
| Name           | Use                                                                |
|----------------|--------------------------------------------------------------------|
| subreddit_tifu | 1 for tifu, 0 for NoStupidQuestions                                |
| Id             | Post ID to make sure there were no duplicates                      |
| Author         | Author of the post at hand                                         |
| selftext       | text inside of post, if any                                        |
| title          | Title of post                                                      |
| text           | combination of selftext and title, to feed into the model          |
| line_count     | Total number of times enter was pressed, denoted in the text as /n |


See attached Executive Summary
