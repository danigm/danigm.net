Date: 2019-05-25
Title: EndlessOS dual boot with Fedora
Tags: gnome, work, endless, fedora
Category: blog
Slug: endlessos-dual-boot
Gravatar: 8da96af78e0089d6d970bf3760b0e724

I've a *ThinkPad X1 Yoga*, that's basically a *ThinkPad X1 Carbon 4th* but
with a touch screen with a pencil that works like a wacom tablet.

I've this laptop since 2016. The first thing that I did when I received it
was install a GNU/Linux operating system. I'm a GNU/Linux user since the
year 2000 going through a lot of distributions, Debian, Ubuntu, Archlinux, etc.

When I received this computer I've a customized Archlinux there, and I wanted
to `dd` my harddisk and boot, but I was unable to do that. I didn't know
nothing about UEFI and I was unable to boot the Archlinux installer.

So I decided to go ahead and change my main distribution. I installed Fedora
and almost all the hardware worked so I keep that one and was happy, until
today :P

## OStree, the new way of distribute GNU/Linux

With OStree and flatpak, there's a new way to distribute GNU/Linux, instead of
use directly a package manager and update each package, we can use OStree and
mount the root filesystem as read only and do full OS upgrades without broken
packages and dependencies and so. The operating system go as is and the user
should try hard to break it.

The other great thing about OStree is that it's like a git repository, so you
can have different branches and a history, so you can easily go back and forward,
it's really easy to test the beta and go back without breaking your system.

The main problem is that you *can't* install anything on your OS, you should
use contained apps like flatpak or install by hand, you can't use `apt-get`.
But that's okay for a day to day user, a power user always can `unlock` the OS
and use it as a normal GNU/Linux distribution.

I wanted to try one of these distributions. The logical choice was [Silverblue][2]
because it's a Fedora and I'm using it for three years now, but there's another
option, [EndlessOS][1] is also OStree based, and [I'm working with this OS][3],
so I should give a try and use EndlessOS.

## The EndlessOS install process

Like all the new modern GNU/Linux distros, EOS comes with a easy to use installer,
you only need to boot from the USB and click next until it's done...

<p class="img">
    <a href="/pictures/eos/endless-install-2.jpg">
        <img src="/pictures/eos/endless-install-2.jpg" />
    </a>
</p>

But here we've the first problem. I've more than one partition in my disk:

 * /dev/sda1: UEFI
 * /dev/sda3: Fedora /
 * /dev/sda8: Swap
 * /dev/sda4: Fedora /boot
 * /dev/sda6: /home

I want to keep my Fedora (who knows if something bad happens) and try to use the
same home partition for my new EOS. But the installer only give me the option
to erase all and have a clean system. But that won't stop me.

Let's go back and instead of reformat I will click on *Try Endless OS*:

<p class="img">
    <a href="/pictures/eos/EndlessOS-Installation.png">
        <img src="/pictures/eos/EndlessOS-Installation.png" />
    </a>
</p>

What we need to do, Robert McQueen gave me some directions:

> The constraints for booting Endless are 1) you use our grub, and 2) the root
partition is labelled "ostree"

> So if you have an EFI system, you can copy our EFI binaries into the ESP, and
create a new partition for Endless, then dd the endless ostree filesystem into
it

> Then you should be able to boot, if you add a boot entry for the endless grub
to your firmware, or make it the default (by providing the fallback boot64.efi
or whatever it's called), or chain load it from another Linux loader

## Install EOS with other linux (EFI system)

1. Boot from USB, select try
1. Launch the gnome-disk-utility and prepare a partition. I've not free space,
but I was able resize my Fedora partition and I split in two of the same size,
now I've a new ext4 partition `/dev/sda7` with 25GB.

1. Copy the endless ostree:
```
$ sudo su
# dd if=/dev/mapper/endless/image3 /dev/sda7
```

1. Copy endless grub to EFI. I mounted all partitions in /tmp, the first
partition in `/tmp/sda1` and the EOS efi in the `/tmp/EOS`:
```
# mkdir /tmp/sda1 /tmp/EOS
# mount /dev/sda1 /tmp/sda1
# mount /dev/mapper/endless-image1 /tmp/EOS
# cp -rf /tmp/EOS/EFI/endless/ /tmp/sda1/EFI
```

1. Add the new boot entry:
```
# efibootmgr -c -d /dev/sda -p 1 -L EOS -l \\EFI\\endless\\grubx64.efi
```

1. Set as default boot:
```
# cp /tmp/EOS/EFI/endless/grubx64.efi /tmp/sda1/EFI/Boot/bootx64.efi
```

1. Reboot and create my default user. Then I add my home partition to the `/etc/fstab`
file:

```
UUID=c885e171-1a03-4afb-8519-f9fe26fe92b7 /sysroot/home ext4 defaults 1 2
```

And because the first user in EOS is the shared account, with UID 1000, I've to
change the UID of my user editing the file in `/etc/passwd`. Then I rebooted
again and all works. I've all my flatpak apps installed in the user space working.

So here we're, with a shiny new OS working like a charm:

<p class="img">
    <a href="/pictures/eos/screenshot.png">
        <img src="/pictures/eos/screenshot.png" />
    </a>
</p>

## The EFI and efibootmgr (who needs grub to select the OS?)

I didn't know much about UEFI and I was very impressed about how easy is to
update this from GNU/Linux. There's a tool called `efibootmgr` that does all
the work, and you can mount the partition, that's a FAT32, and put files there.

In my ThinkPad, I can boot directly to the UEFI boot menu pressing F12 during
the boot, and that menu can be changed using the `efibootmgr` so it's not
needed anymore to use the grub2 OS selection interface, I can use the UEFI
menu for that!

This has some disadvantages, if you remove files from the UEFI partition, you
can break the whole boot, so review all before any change.

[1]: https://endlessos.com/
[2]: https://silverblue.fedoraproject.org/
[3]: http://danigm.net/endless.html
