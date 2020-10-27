# Copyright 2020 William Ro. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ====-==============================================================-==========
"""A class that provides utilities to show information in terminal.
"""
from sys import stdout


DEFAULT_PROMPT = '>>'


class Console(object):

  def __init__(self, buffer_size=0):
    # Public variables
    self.buffer_size = buffer_size
    assert isinstance(buffer_size, int) and buffer_size >= 0
    # Private variables
    self._buffer = []

  # region : Properties

  @property
  def buffer(self):
    return self._buffer

  @property
  def buffer_string(self):
    return '\n'.join(self._buffer)

  # endregion : Properties

  # region : Private Methods

  def _add_to_buffer(self, line):
    assert isinstance(line, str)
    if self.buffer_size == 0: return
    assert self.buffer_size > 0
    self._buffer.append(line)
    if len(self._buffer) > self.buffer_size: self._buffer.pop(0)

  # endregion : Private Methods
  
  # region : Public Methods

  def show_status(self, status, prompt=None):
    """Shows status following the specified prompt.
    :param status: content to be shown.
    :param prompt: The leading symbol, usually '>>' by default.
    """
    if prompt is None: prompt = DEFAULT_PROMPT
    # The type of status should not be restricted
    assert isinstance(prompt, str)
    line = '{} {}'.format(prompt, status)
    print(line)
    self._add_to_buffer(line)

  # endregion : Public Methods

  # region : Static Methods

  @staticmethod
  def disable_logging(pkg_name):
    """Suppress the annoying logging information in terminal.
    :param pkg_name: Name of the package producing the unwanted log.
                     e.g., 'tensorflow'
    """
    assert isinstance(pkg_name, str)
    import logging
    logging.getLogger(pkg_name).disabled = True

  # endregion : Static Methods


if __name__ == '__main__':
  pass


