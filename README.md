<a href="https://github.com/jajosheni/instaBot/" title="python InstaBot"><img src="https://img.shields.io/badge/python-instaBot-green.svg"></a>
<a href="https://instagram.com/detajist" title="instapage"><img src="https://img.shields.io/badge/follow-instagram-orange.svg"></a>
<a href="https://www.python.org/downloads/release/python-350/" title="use python3.5"><img src="https://img.shields.io/badge/version-python3.5-brightgreen.svg"></a>

<img src="https://instavast.com/wp-content/uploads/2017/09/auto-activity.png">

### Installation Instructions
<table class="tableblock frame-all grid-all spread data-line-12">
<colgroup>
<col style="width: 50%;">
<col style="width: 50%;">
</colgroup>
<thead>
<tr>
<th class="tableblock halign-left valign-top">Step</th>
<th class="tableblock halign-left valign-top">Command</th>
</tr>
</thead>
<tfoot>
<tr>
<td class="tableblock halign-left valign-top"><p class="tableblock">NOTE</p></td>
<td class="tableblock halign-left valign-top"><p class="tableblock"><em>if you are using <strong>pycharm</strong>:  replace getpass.getpass() method with input()</em></p></td>
</tr>
</tfoot>
<tbody>
<tr>
<td class="tableblock halign-left valign-top"><p class="tableblock">1. Fork/Clone/Download this repo</p></td>
<td class="tableblock halign-left valign-top"><p class="tableblock"><code>git clone <a href="https://github.com/jajosheni/instaBot" class="bare">https://github.com/jajosheni/instaBot</a></code></p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p class="tableblock">2. Navigate to the directory</p></td>
<td class="tableblock halign-left valign-top"><p class="tableblock"><code>cd instaBot</code></p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p class="tableblock">3. Install the dependencies</p></td>
<td class="tableblock halign-left valign-top"><p class="tableblock"><code>python setup.py install or pip install -r requirements.txt</code></p></td>
</tr>
<tr>
<td class="tableblock halign-left valign-top"><p class="tableblock">4. Run the app.py script</p></td>
<td class="tableblock halign-left valign-top"><p class="tableblock"><code>python app.py</code></p></td>
</tr>
</tbody>
</table>


#### Use at your own risk
**=====================**

#### 2.2 version upgrades:
  1. Added a new list of 'Albanian' comments and a location check function
     so pics with a location in Albania will get an Albanian comment.
  2. Added 3 text files:
    • followings.txt - to keep track of who was followed (not to follow that account twice)
    • whitelist.txt - whitelisted accounts
    • check.txt - this list is defined by some conditions and will be deleted by `deletelist`
    - CHANGE "YOUR_USERNAME" to your username inside the code.
  3. Added a clear screen command.
  4. Added a nice character art tweak.
  5. Added a `unfollowers` to see a list of who is unfollowing.
  
#### 2.1.2 version upgrades:
  1. Fixed feedlike & explorelike so more than 100 pictures will be auto-liked.
  2. Removed Hashtaglist based auto-following as unnecessary.
  3. Added `profpic` to Spam Comment so you can download anyone's full size profile picture.

#### 2.1.1 version upgrades:

Run: `python spamcomment.py`

SpamComment use & purpose is simple:
  1. Enter hashtag to browse
  2. Enter the word you want to comment
    (ex: #myhashtag)
<br><i>The script will go to some of the pictures under the hashtag entered and comment your #myhashtag;<br>
I've created this so you get some traffic through your unique hashtag.
It's better if you use this with a fake account, so you don't surpass the comment limit on your original account.</i>


#### 2.1 version upgrades:
  1. Made 'automatic' run on a separate thread
  2. Added features like autolike & autocomment to automatic
  3. Improved hashtags and comments list


#### 2.0 version upgrades:

Made most of the features run on other threads.
Added a couple of features like:
  1. Explore pictures autolike
  2. Hashtag pictures autolike
  3. Hashtag pictures autocomment
  4. AUTOMATIC:
      you are prompted for a hashtag then the app smartly selects a picture and follows its likers.


#### 1.1 version upgrades:

Added a couple of features like:
  1. Hashtag based auto-following
  2. Hashtaglist based auto-following
  3. Feed auto-like
  
#### 1.0 version:

  This program was firstly made to unfollow your unfollowers.
  First functions were:
  1. Refresh - to refresh lists
  2. Stats - to see your followers,followings and Unfollowers
  3. Unfollow - to unfollow the accounts not following back
  4. Changeuser - to switch between accounts without having to close the app
  5. Help - to bring up the menu.
  6. Exit.
