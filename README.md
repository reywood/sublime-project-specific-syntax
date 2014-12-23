Project Specific Syntax Settings
================================

This package allows syntax settings to be specified per project.

In your `.sublime-project` file, you just need to add a `syntax_override` section, like so.

```json
{
    ...

    "syntax_override": {
        "\\.html$": [ "HTML Underscore Syntax", "HTML (Underscore)" ]
    }
}
```

The `syntax_override` section can contain as many key/value pairs as you like.

The key should be a regular expression that will be matched against the name of the file. Note that the `.` in `.html` has to be escaped to `\.` since it will match any character otherwise. And since this is a JSON string, we need to escape the slash, so we end up with `\\.`.

The value in the key/value pair should be an array containing two or more strings. All but the last string in this array are the names of the package directories containing the syntax file and the last is the name of the syntax. Root around in Sublime Text's directory structure to find files that end with `.tmLanguage`. The names of these files (minus the `.tmLanguage` extension) are what you would use for the last string. Typically, you will only have two strings, a directory name and the syntax file name (minus `.tmLanguage` file extension), but this is dependent on the package's directory structure.
