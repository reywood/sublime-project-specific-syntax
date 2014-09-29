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

The value in the key/value pair should be an array containing two strings. The first string is the name of the package containing the syntax file and the second is the name of the syntax. Root around in Sublime Text's directory structure to find files that end with `.tmLanguage`. The names of these files (minus the `.tmLanguage` extension) are what you would use for the second string.
