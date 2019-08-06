"""
MIT License

Copyright (c) 2019 Nxt Games, LLC
Written by Jordan Maxwell 
08/06/2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from panda3d import core

class StatCollector(core.PStatCollector):
    """
    Custom wrapper for the PStatCollector
    """

    def start(self):
        """
        Custom wrapper for the collector start
        """

        if not EngineAnalysis.get_collecting():
            return

        return core.PStatCollector.start(self)

    def stop(self):
        """
        Custom wrapper for the collector stop
        """

        if not EngineAnalysis.get_collecting():
            return

        return core.PStatCollector.stop(self)

def AnalysisWrapperDecorator(function):
    """
    Wraps a function in a PStatsCollector
    """

    def do_pstat(*args, **kargs):
        collector_name = "Debug:%s" % function.__name__
        pstat = EngineAnalysis.get_collector(collector_name)

        pstat.start()
        returned = function(*args, **kargs)
        pstat.stop()

        return returned
    
    do_pstat.__name__ = function.__name__
    do_pstat.__dict__ = function.__dict__
    do_pstat.__doc__ = function.__doc__

    return do_pstat

analyze = AnalysisWrapperDecorator

class EngineAnalysis(object):
    """
    Management object for engine analysis and reporting
    """

    collectors = {}
    collecting = core.ConfigVariableBool('collect-stats', __debug__).value

    @classmethod
    def get_client(cls):
        """
        Retrieves the global pstats client object
        """

        return core.PStatClient.get_global_pstats()

    @classmethod
    def get_collecting(cls):
        """
        Retrieves the collecting state
        """

        return cls.collecting

    @classmethod
    def set_collecting(cls, state):
        """
        Sets the collecting state
        """

        cls.collecting = state

    @classmethod
    def connect(cls, hostname='', port=-1):
        """
        Connects to a PStats Server instance
        """

        if core.PStatClient.is_connected():
            return False

        return core.PStatClient.connect(hostname, port)

    @classmethod
    def disconnect(cls, hostname, port):
        """
        Disconnected from a PStats Server instance
        """

        if not core.PStatClient.is_connected():
            return False

        core.PStatClient.disconnect()
        return True

    @classmethod
    def add_collector(cls, collector_name, collector_instance):
        """
        Adds a new collector instance to the collection
        """

        if collector_name in cls.collectors:
            return False

        cls.collectors[collector_name] = collector_instance
        return True

    @classmethod
    def get_collector(cls, collector_name):
        """
        Retrieves a collector instance. Otherwise returns a new collector
        if one does not already exist
        """

        if collector_name in cls.collectors:
            return cls.collectors[collector_name]
        else:
            collector = StatCollector(collector_name)
            cls.collectors[collector_name] = collector
        
        return collector