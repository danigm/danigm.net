Date: 2025-10-21 12:00
Title: GNOME Tour in openSUSE and welcome app
Tags: gnome-tour, welcome, suse, gsoc, gnome
Slug: gnome-tour-opensuse
Gravatar: 8da96af78e0089d6d970bf3760b0e724
Category: blog

As a follow up of the [Hackweek 24 project][1], I've continued working
on the gnome-tour fork for openSUSE with custom pages to replace the
welcome application for openSUSE distributions.

## GNOME Tour modifications

All the modifications are on top of [upstream gnome-tour][3] and
stored in the [openSUSE/gnome-tour repo][2]

 * Custom **initial page**

<p class="img">
  <img src="/pictures/gnome-tour-opensuse.png" />
</p>

 * **A new donations page**. In openSUSE we remove the popup from GNOME
   shell for donations, so it's fair to add it in this place.

<p class="img">
  <img src="/pictures/gnome-tour-donation.png" />
</p>

 * **Last page with custom openSUSE links**, this one is the used for
   opensuse-welcome app.

## opensuse-welcome package

The [original opensuse-welcome][4] is a qt application, and this one
is used for all desktop environments, but it's more or less
unmaintained and looking for a replacement, we can use the gnome-tour
fork as the default welcome app for all desktop without a custom app.

To do a minimal desktop agnostic opensuse-welcome application, I've
modified the gnome-tour to also generate a second binary but just with
the last page.

The new opensuse-welcome rpm package is built as a subpackage of
[gnome-tour][5]. This new application is minimal and it doesn't have
lots of requirements, but as it's a gtk4 application, it requires gtk
and libadwaita, and also depends on gnome-tour-data to get the
resoures of the app.

<p class="img">
  <img src="/pictures/opensuse-welcome.png" />
</p>

To improve this welcome app we need to review the translations,
because I added three new pages to the gnome-tour and that specific
pages are not translated, so I should regenerate the .po files for all
languages and upload to [openSUSE Weblate][6] for translations.

[1]: https://danigm.net/hackweek24.html
[2]: https://github.com/openSUSE/gnome-tour
[3]: https://gitlab.gnome.org/GNOME/gnome-tour/
[4]: github.com/openSUSE/openSUSE-welcome
[5]: https://src.opensuse.org/pool/gnome-tour
[6]: https://l10n.opensuse.org/
