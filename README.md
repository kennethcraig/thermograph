Raspberry Pi Thermograph <br />
Ken Andrews <br />
2012 <br />

Requirements:<br />
<ul>
<li>lighthttpd</li>
<li>python</li>
<li>sqlite</li>
<li>rrdtool</li>
</ul>

Setup Notes for RPi<br />
<pre>
sudo apt-get install lighttpd rrdtool python
</pre>

Enable CGI on lighttpd:
<pre>
sudo lighttpd-enable-mod cgi
sudo /etc/init.d/lighttpd force-reload
</pre>

edit the following in /etc/lighttpd/conf-available/10-cgi.conf:
<pre>
cgi.assign      = (
#       ".pl"  => "/usr/bin/perl",
        ".py"  => "/usr/bin/python",
)

</pre>