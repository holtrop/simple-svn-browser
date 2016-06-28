# Simple SVN Browser

Simple SVN Browser is a very simple Subversion repository browser implemented
with Python3/GTK3.
It was implemented to have a very basic GUI for browsing repositories from
Linux.
It works by wrapping the `svn` command-line interface.
This made development much faster.
As a side-effect, you'll need to have your Subversion credentials cached for
any repository you browse.
Simple SVN Browser has no mechanism to accept credentials.

## Installation

```bash
pip3 install --user git+git://github.com/holtrop/simple-svn-browser.git
```

## Uninstallation

```bash
pip3 uninstall simplesvnbrowser
```

## Usage

```bash
simple-svn-browser [working-copy-path-or-repository-url]
```

If invoked without any argument, the URL of the current working copy in the
current directory (if present) will be used.

## License

Simple SVN Browser is licensed under the [zlib license](LICENSE).

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
