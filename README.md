# abook-interactive-add

This script will let you interactively add email addresses to
your [abook][] database.

[abook]: http://abook.sourceforge.net/

I have the following in my `muttrc` file:

    macro index,pager	\\ai '<pipe-message>~/bin/abook-interactive-add<enter>'

If you receive a message that has headers that look like:

    From: bob@example.com
    To: alice@example.com, fred@example.com
    Cc: mallory@example.com

Then piping that to `abook-interactive-add` will produce an
interactive prompt along the lines of:

    [?] Select addresses to add:
     > o bob@example.com
       o alice@example.com
       o fred@example.com
       o malloary@example.com

Use your arrow keys to move the selection up and down, use the space
bar to select, and use the enter key to commit your changes.
