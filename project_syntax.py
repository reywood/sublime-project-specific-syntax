import json
import os.path
import re
import sublime
import sublime_plugin


class ProjectSpecificSyntax(sublime_plugin.EventListener):

    def on_load(self, view):
        self._ensure_project_specific_syntax(view)

    def on_post_save(self, view):
        self._ensure_project_specific_syntax(view)

    def _ensure_project_specific_syntax(self, view):
        filename = view.file_name()
        if not filename:
            return

        syntax = self._get_project_specific_syntax(view, filename)
        if syntax:
            self._set_syntax(view, syntax)

    def _get_project_specific_syntax(self, view, filename):
        project_data = _resolve_window(view).project_data()

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


class ProjectSpecificSyntaxToClipboardCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        super().__init__(view)
        self._view = view

    def run(self, edit):
        suggested_setting = self._build_suggested_setting()

        if not suggested_setting:
            sublime.set_clipboard('Unable to create syntax setting')
        else:
            sublime.set_clipboard(suggested_setting)

    def _build_suggested_setting(self):
        suggested_setting = self._build_syntax_setting_for_current_file()
        if not suggested_setting:
            return None

        return self._enclose_in_syntax_override_block_if_not_present_in_settings(suggested_setting)

    def _build_syntax_setting_for_current_file(self):
        syntax_path_parts = self._get_syntax_path_parts()

        if not syntax_path_parts:
            return None

        syntax_path_json = json.dumps(syntax_path_parts)
        file_regex = self._get_example_file_regex_for_current_file()
        return '"{0}": {1}'.format(file_regex, syntax_path_json)

    def _get_syntax_path_parts(self):
        syntax = self.view.settings().get('syntax')

        match = re.search(r'^Packages/(.*)\.(tmLanguage|sublime-syntax)$', syntax)

        if not match:
            print('Syntax does not match expected format: {0}'.format(syntax))
            return None

        return match.group(1).split('/')

    def _enclose_in_syntax_override_block_if_not_present_in_settings(self, suggested_setting):
        if self._is_syntax_override_already_present_in_settings():
            return suggested_setting

        return '"syntax_override": {{\n\t{0}\n}}'.format(suggested_setting)

    def _is_syntax_override_already_present_in_settings(self):
        project_data = _resolve_window(self._view).project_data()
        return 'syntax_override' in project_data

    def _get_example_file_regex_for_current_file(self):
        file_name = self.view.file_name()

        if file_name:
            ext = os.path.splitext(file_name)[1]
        else:
            ext = '.xyz'

        return '\\\\{0}$'.format(ext)


def _resolve_window(view):
    window = view.window()

    if window:
        return window

    return sublime.active_window()
