1) Database schema
  -Users
    -Id
    -Name
    -Profile Name
    -Avatar
  -Tweets
    -UserId
    -tweetId
    -tweet date and time
    -tweet content
    -Likes
  -Retweets(bonus)
    -tweetId
    -UserId of original tweeter
    -UserID of retweeter
  -Follower/Followee
   -UserId(followerId)
   -UserId(followeeId)

2) Profile Page
  -Displays user info
  -Followers 
  -Users tweets
    -tweet data
      -# of tweets and retweets

3) Timeline Page
  -Displays tweets of user and all followers by date and time in order
    -tweet data
      -likes and retweets
