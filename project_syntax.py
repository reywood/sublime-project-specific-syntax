import json
import os.path
import re
import sublime
import sublime_plugin


class ProjectSpecificSyntax(sublime_plugin.EventListener):

    def on_load(self, view):
        filename = view.file_name()
        if not filename:
            return

        syntax = self._get_project_specific_syntax(view, filename)
        if syntax:
            self._set_syntax(view, syntax)

    def _get_project_specific_syntax(self, view, filename):
        project_data = self._resolve_window(view).project_data()

        if not project_data:
            return None

        syntax_settings = project_data.get('syntax_override', {})

        for regex, syntax in syntax_settings.items():
            if re.search(regex, filename):
                return syntax

        return None

    def _set_syntax(self, view, syntax):
        syntax_path = '/'.join(syntax)

        view.set_syntax_file('Packages/{0}.tmLanguage'.format(syntax_path))

        print('Switched syntax to: {0}'.format(syntax_path))

    def _resolve_window(self, view):
        window = view.window()

        if window:
            return window

        return sublime.active_window()


class ProjectSpecificSyntaxToClipboardCommand(sublime_plugin.TextCommand):

    def __init__(self, window):
        super().__init__(window)

    def run(self, edit):
        syntax_path_parts = self._get_syntax_path_parts()

        if not syntax_path_parts:
            sublime.set_clipboard("Unable to create syntax setting")
            return

        syntax_path_json = json.dumps(syntax_path_parts)
        file_regex = self._get_example_file_regex()
        suggested_setting = '"{0}": {1}'.format(file_regex, syntax_path_json)

        sublime.set_clipboard(suggested_setting)

    def _get_syntax_path_parts(self):
        syntax = self.view.settings().get('syntax')

        match = re.search(r'^Packages/(.*)\.tmLanguage$', syntax)

        if not match:
            print('Syntax does not match expected format: {0}'.format(syntax))
            return None

        return match.group(1).split('/')

    def _get_example_file_regex(self):
        file_name = self.view.file_name()

        if file_name:
            ext = os.path.splitext(file_name)[1]
        else:
            ext = '.xyz'

        return '\\\\{0}$'.format(ext)
