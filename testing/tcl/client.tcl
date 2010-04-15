proc log { f } { puts "read from Jabber: [gets $f]" }

set f [open "| ./xmpp_stdio.py -d toto@gmail.com -l tata@gmail.com -p supertata" RDWR]

fileevent $f readable "log $f"
fconfigure $f -blocking 1 -buffering line

for { set i 0 } { $i < 10 } { incr i } {puts $f "toto$i" }


while { 1 } { update }
