mailrss2google
==============

Find all rss feeds in mac mail and  subscribe them to google reader.

> With OS X Mountain Lion, Apple removed the support of RSS in both Safari and Mail. If you depend on the RSS reader features, look for alternatives before you make the switch to OS X Mountain Lion.

So you may need to get all your collected feeds or transfer them to google reader via some tools if you have upgraded to mountain lion.

If you just want list them, all you need to do is typing these words into your terminal and execute it:
<code>
find ~/Library/Mail/V2/RSS/ -name "Info.plist" |xargs -I{}  grep -A 1 Feed {} | grep string | awk -F'[<>]' '{print $3}'
</code>

But if you need subscribe them to google reader, you may need do this:
<code>
python rsstransfer.py your_google_email
</code>
and input your password.
