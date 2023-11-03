Date: 2023-11-03
Title: Updating GNOME shell extensions to GNOME 45
Tags: gnome, work, suse, linux, javascript
Category: blog
Slug: gnome-45-extensions
Gravatar: 8da96af78e0089d6d970bf3760b0e724

<img src="/pictures/GNOME45.webp" width="100%" />

The new version of the [GNOME desktop][5] was released [more than one month][6]
ago. It takes some time to arrive to the final user, because distributions
should integrate, tests and release the new desktop, and that's not something
simple, and it should integrate in the distribution release planning.

So right now, it's possible that there's just a few people with the latest
version of the desktop right now, just people with rolling release distros or
people using testing versions of mayor distributions.

This is one of the reasons because a lot of gnome-shell extensions aren't
updated to work with the latest version of GNOME, even after a few months,
because even developers doesn't have the latest version of the desktop and
it's not something "easy" to install, without a virtual machine or something
like that. Even if the update is just a change in the metadata.json, there
should be someone to test the extension, and even someone to request this
update, and that will happen once the mayor distributions release a new
version.

I'm using Tumbleweed, that's a rolling release and GNOME 45 is here just after
the official release, but of course, a lot of extensions are not working, and
in the infamous list of non working extensions there where the three that I'm
[maintaining right now][1]:

 * [mute-spotify-ads][7], extension to mute the spotify app when it's playing ads.
 * [calc][8], a simple calculator in the alt+F2 input.
 * [hide-minimized][9], hide minimized windows from alt+tab and overview.

<p class="img">
    <img src="/pictures/GNOME45-desktop.webp" />
</p>

## The correct way

The correct way to maintain and update a gnome-shell extension should be to
test and update "before" the official release of GNOME. It should be something
easy for me, using Tumbleweed I can just add the [GNOME Next][10] repository,
install the new desktop when it's in beta stage, and update the extension
there.

But that's something that require an active maintainership... And right now
what I do is to update the extensions when they are broken for me, so just when
I need them, and that's after I get the new desktop and I find some time to
update.

I know that's not the correct way and this produces a bad experience for other
people using the extensions, but this is the easier thing to do for me. Maybe
in the future I can do it correctly, and provide a tested update before the
official release, maybe using snapper to be able to go back to stable, without
the need of using virtual machines.

## Update your extension to GNOME 45

The update to GNOME 45 was a bit more complex than previous ones. This version
of the shell and gjs change a lot of things, so the migration it's not just to
add a new number to the metadata.json, but requires incompatible changes, so
extensions that works for GNOME 45 won't work for previous versions and
vice versa.

But the people working in gnome-shell does a great work documenting and there's
a really nice guide about [how to upgrade your extension][4].

The most important part is the import section, that now it has a different syntax.

```
// Before GNOME 45
const Main = imports.ui.main;

// GNOME 45
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
```

And some changes in the extension class, that now can inherit from existing
ones to provide common usage, like preferences window:

```
import Adw from 'gi://Adw';

import {ExtensionPreferences, gettext as _} from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

export default class MyExtensionPreferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        window._settings = this.getSettings();

        const page = new Adw.PreferencesPage();

        const group = new Adw.PreferencesGroup({
            title: _('Group Title'),
        });
        page.add(group);

        window.add(page);
    }
}
```

[1]: https://extensions.gnome.org/accounts/profile/danigm
[2]: https://wiki.gnome.org/Projects/GnomeShell/Extensions
[3]: https://gjs.guide/extensions/development/creating.html#gnome-extensions-tool
[4]: https://gjs.guide/extensions/upgrading/gnome-shell-45.html
[5]: https://www.gnome.org/
[6]: https://foundation.gnome.org/2023/09/20/introducing-gnome-45/
[7]: https://github.com/danigm/spotify-ad-blocker
[8]: https://github.com/danigm/gnome-shell-calculator
[9]: https://github.com/danigm/hide-minimized
[10]: https://build.opensuse.org/project/show/GNOME:Next
