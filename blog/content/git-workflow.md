Date: 2025-11-14 12:00
Title: openSUSE: The new git workflow
Tags: suse, opensuse, git, packaging, python
Slug: git-workflow
Gravatar: 8da96af78e0089d6d970bf3760b0e724
Category: blog

openSUSE is migrating the package source management from **osc** to
**git**. I will try to explain here what it is the "git workflow" in
openSUSE and give some practical information for contributors and
maintainers.

<p class="img">
  <img src="/pictures/opensuse-git.png" />
</p>

You can find some documentation in the [openSUSE wiki](https://en.opensuse.org/openSUSE:Git_Packaging_Workflow)

## Why?

openSUSE uses [Open Build Service](https://openbuildservice.org/) to
store package sources (.spec files and patches). The source control is
similar to [subversion](https://subversion.apache.org/), so you can
_osc checkout_, _osc commit_, _osc log_, etc. to work with any package
source.

I don't know all the reasons to do the change, and different people
will find different reasons, to support the change or to be against
it. I will just write here what I consider a good reason to migrate:

* Almost everyone has moved to git now, so today,
  [git](https://git-scm.com) is the default source code management
  (scm) tool, almost all the people knows about
  [github](https://github.com), so it's good to be "_standard_".
* With the concept of "_cheap_" branches in git, it **could** be
  easier to maintain different versions of the same package, same
  repository, different branches, instead of actual forks.
* Decouple the package source management from build. OBS does a lot of
  things, moving source code and review process to
  [gitea](https://gitea.com) could reduce the complexity (but requires
  some integration).

## From OBS to gitea

All the development happens in [OBS][1], so the
**classic** workflow happens entirely there:

* developer: branch -> checkout -> modify -> commit -> submit request
* maintainer: review -> accept/decline

And everything is integrated in OBS that does the corresponding build
of the sources, checks with services, forward, etc.

The **new** workflow changes almost all the interaction from
[OBS][1] to [gitea][2]. OBS is still
a really important piece of software in the process, but in the new
workflow it's a build backend, so the user interaction will be with
the git repo in [gitea][2].

The new **git workflow** happens in [gitea][2]:

* developer: fork -> clone -> modify -> commit -> push -> pull request
* maintainer: review -> approve/decline

As you may notice, the "_default_" workflow is very similar, the
difference is in the tools, the **classic** workflow occurs in
[build.opensuse.org][1] and the **new** workflow in
[src.opensuse.org][2]. And the tools to work with the
sources are also different, **osc** in the first one and **git** in
the new workflow.

And with this new workflow, there are some bots in gitea that sends
the changes to OBS, so for any pull request created you will have the
build results and approval from the bot if everything is building.

## How to modify a package (leap 16.0)

Notice that you should have a [openSUSE account][3] to work with the
gitea instance, and don't forget to [configure your ssh key][4] to be
able to push using the gitea@src.opensuse.org remote.

So as a contributor, this is the basic workflow to follow to update a
package in openSUSE:

1. Look for the source package in the pool
   ([https://src.opensuse.org/pool](https://src.opensuse.org/pool))
1. Fork it in your user space, click the top right button. Skip this
   step if you have forked before
1. Clone your fork and work on that repo, create a new branch, modify
   the spec file, add new soures, etc. And make sure to update the
   .changes file accordingly, you can still use `osc vc` to do that.
1. You can build locally your package with `osc build`, as usual, but
   you will need to specify the build project:
```
$ git obs meta pull
$ git obs meta set --project openSUSE:Backports:SLE-16.0
$ osc build
```
1. Once you are happy with your changes, you can commit, push to your
   fork and then you can create a Pull Request. The pull request
   should target the **pool** repo and desired product branch. Right
   now you can just target `leap-16.0`, as factory is not migrated
   yet.

## Devel projects

Some devel projects have been migrated now to git, so a similar
workflow is available to modify these packages in Tumbleweed. The
development of these packages is not happening in the _pool_, so you
need to find first the devel project.

There's no simple way to discover the actual package devel source, as
far as I know the easier way is:

1. Look for the devel project of the package in the [Factory list][7],
   (ex python-pytest)
1. Go to the devel project in [OBS](1) (ex [devel:languages:python:pytest](https://build.opensuse.org/project/show/devel:languages:python:pytest))
1. Click on the link [This project is managed in SCM][8]

Once you have located the desired package to modify, the workflow is
similar to what I explained before, but instead of forking from
**pool**, you should fork from the devel project. For example if you
want to modify **python-pytest** you should fork from
[https://src.opensuse.org/python-pytest/python-pytest](https://src.opensuse.org/python-pytest/python-pytest), 
and create the pull request for that repo, to the main branch.

Adding a new package follows a different process that's documented in
the [wiki][6]

## What's migrated?

As I said, the migration is happening right now, so not everything is
migrated. The first project migrated was the Leap 16.0. And we are
slowly migrating some devel projects.

Right now from the python-maintainers team, we've started the
migration of two subprojects:

 * [python-interpreters](https://src.opensuse.org/python-interpreters)
 * [python-pytest](https://src.opensuse.org/python-pytest)

You can find more information about the migration current state in the
wiki: [https://en.opensuse.org/opensuse:obs_to_git#codestream_project_status_table](https://en.opensuse.org/openSUSE:OBS_to_Git#Codestream_Project_Status_table)

[1]: https://build.opensuse.org
[2]: https://src.opensuse.org
[3]: https://idp-portal.suse.com/univention/self-service/#page=createaccount
[4]: https://src.opensuse.org/user/settings/keys
[5]: https://src.opensuse.org/products
[6]: https://en.opensuse.org/openSUSE:OBS_to_Git#How_to_create_a_new_package?
[7]: https://src.opensuse.org/openSUSE/Factory/src/branch/main/pkgs/_meta/devel_packages
[8]: https://src.opensuse.org/python-pytest/_ObsPrj.git#main
