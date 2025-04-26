# Discord Truth Social Bot - Usage Guide

This guide provides detailed examples of how to use the Discord Truth Social Bot's commands in various scenarios.

## Table of Contents
- [Profile Information](#profile-information)
- [Post Filtering](#post-filtering)
- [Post Monitoring](#post-monitoring)
- [Help Commands](#help-commands)
- [Common Workflows](#common-workflows)

## Profile Information

### Viewing a User's Profile

**Command**: `!ttruth-profile @username`

**Example**:
```
!ttruth-profile @realDonaldTrump
```

**Expected Output**:
```
Profile for @realDonaldTrump:
Name: Donald J. Trump
Bio: 45th President of the United States of America
Location: United States
Following: 284
Followers: 6.38M
Account created: October 21, 2021
```

**Notes**:
- The @ symbol is optional
- If the profile doesn't exist, the bot will inform you
- For profiles without a bio, that field will be empty

## Post Filtering

### Basic Post Filtering

**Command**: `!tfilter-posts @username [keywords] [days]`

**Example 1**: Get recent posts from a user (last 7 days, default)
```
!tfilter-posts @realDonaldTrump
```

**Example 2**: Filter posts containing specific keywords
```
!tfilter-posts @realDonaldTrump election fraud
```

**Example 3**: Filter posts with a phrase (use quotes)
```
!tfilter-posts @realDonaldTrump "Make America Great Again" 14
```

**Example 4**: Specify a different time period (up to 30 days)
```
!tfilter-posts @realDonaldTrump economy 21
```

**Expected Output**:
```
Posts from @realDonaldTrump containing "economy" in the last 21 days:

1. "Our economy was the strongest it has ever been until the China Virus..." - Posted on July 10, 2023
2. "Under my administration, the American economy was thriving..." - Posted on July 5, 2023
3. "The current economy is in shambles. Inflation at 40-year highs..." - Posted on June 28, 2023

Total matching posts: 3
```

**Notes**:
- Only up to 5 most recent matching posts will be shown
- Posts are displayed in reverse chronological order (newest first)
- If no posts match your criteria, the bot will inform you
- A 30-second cooldown applies between searches

## Post Monitoring

### Setting Up Post Monitoring

**Command**: `!tmonitor-posts @username keyword`

**Example**:
```
!tmonitor-posts @realDonaldTrump election
```

**Expected Output**:
```
Now monitoring @realDonaldTrump's posts for keyword: election
You will be notified when new matching posts are found.
```

**When a new matching post is found**:
```
[NEW POST ALERT]
@realDonaldTrump has posted about "election":

"The election infrastructure needs major reforms..."

Posted: Today at 2:15 PM
```

### Checking Monitoring Status

**Command**: `!tmonitoring-status`

**Example**:
```
!tmonitoring-status
```

**Expected Output (if monitoring is active)**:
```
Currently monitoring @realDonaldTrump's posts for keyword: election
Monitoring started: July 15, 2023 at 10:30 AM
Last checked: Today at 3:45 PM
```

**Expected Output (if not monitoring)**:
```
No active monitoring configuration found.
Use !tmonitor-posts @username keyword to start monitoring.
```

### Stopping Monitoring

**Command**: `!tstop-monitoring`

**Example**:
```
!tstop-monitoring
```

**Expected Output**:
```
Monitoring has been stopped.
```

## Help Commands

### General Help

**Command**: `!thelp`

**Example**:
```
!thelp
```

**Expected Output**:
```
Available Commands:
- !ttruth-profile - View a user's profile information
- !tfilter-posts - Filter posts by keywords and date range
- !tmonitor-posts - Start monitoring for posts containing a keyword
- !tstop-monitoring - Stop monitoring posts
- !tmonitoring-status - Check current monitoring status
- !thelp - Show this help message

Type !thelp <command> for more details on a specific command.
```

### Specific Command Help

**Command**: `!thelp <command>` (do not include the command prefix)

**Example**:
```
!thelp filter-posts
```

**Example 2**:
```
!thelp truth-profile  
```

**Expected Output**:
```
Command: !tfilter-posts
Usage: !tfilter-posts @username [keywords] [days]
Description: Filter posts by keywords and date range.

- Use quotes for phrases: !tfilter-posts @user "election fraud" 7
- Or separate keywords: !tfilter-posts @user election fraud 7
- Default is 7 days if not specified
- Maximum 30 days lookback period
- Maximum 5 results per search
- 30 second cooldown between searches
```

## Common Workflows

### Researching Recent Activity

1. Check a user's profile:
   ```
   !ttruth-profile @realDonaldTrump
   ```

2. View their recent posts:
   ```
   !tfilter-posts @realDonaldTrump 14
   ```

3. Filter for specific topics:
   ```
   !tfilter-posts @realDonaldTrump economy inflation
   ```

### Setting Up Continuous Monitoring

1. Start monitoring for specific keywords:
   ```
   !tmonitor-posts @realDonaldTrump election 2024
   ```

2. Check monitoring status periodically:
   ```
   !tmonitoring-status
   ```

3. When done, stop monitoring:
   ```
   !tstop-monitoring
   ```

### Tracking Multiple Topics Sequentially

Since only one monitoring configuration can be active at a time:

1. Start monitoring topic A:
   ```
   !tmonitor-posts @realDonaldTrump economy
   ```

2. When ready to switch topics, stop current monitoring:
   ```
   !tstop-monitoring
   ```

3. Start monitoring topic B:
   ```
   !tmonitor-posts @realDonaldTrump foreign policy
   ```

## Error Handling Examples

### Invalid Username
```
!ttruth-profile @nonexistentuser

Error: Could not find profile for @nonexistentuser. Please check the username and try again.
```

### Rate Limit Exceeded
```
!tfilter-posts @realDonaldTrump election

Error: You've reached the rate limit. Please try again in 23 seconds.
```

### Invalid Lookback Period
```
!tfilter-posts @realDonaldTrump economy 60

Error: Maximum lookback period is 30 days. Please specify a value between 1 and 30.
``` 