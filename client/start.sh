#!/usr/bin/perl -w

use strict;

open(DMESG, "dmesg|") or die "cannot open dmesg: $!\n";

my $device;

while (<DMESG>) {
    if (/(hidraw\d+): .*\[Namtai Wbuzz\]/) {
        $device = $1;
    }
}

if (!defined($device)) {
    die "Cannot find Wireless Buzzer controller\n";
}

exec("sudo ./quizzbuzz.py /dev/$device") or die "$0: cannot start quizbuzz.py: $!\n";

