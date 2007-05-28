#!/usr/bin/env python2.3
import sys, tempfile, os, shutil
import unittest
import logging

sys.path.insert(0, '..')
from zeroinstall.injector import trust, basedir, autopolicy, namespaces
from zeroinstall.injector import model, iface_cache, cli, download, writer, distro
from zeroinstall.zerostore import Store; Store._add_with_helper = lambda *unused: False
from zeroinstall import support

dpkgdir = os.path.join(os.path.dirname(__file__), 'dpkg')

class BaseTest(unittest.TestCase):
	def setUp(self):
		self.config_home = tempfile.mktemp()
		self.cache_home = tempfile.mktemp()
		self.cache_system = tempfile.mktemp()
		self.gnupg_home = tempfile.mktemp()
		os.environ['GNUPGHOME'] = self.gnupg_home
		os.environ['XDG_CONFIG_HOME'] = self.config_home
		os.environ['XDG_CACHE_HOME'] = self.cache_home
		os.environ['XDG_CACHE_DIRS'] = self.cache_system
		reload(basedir)
		assert basedir.xdg_config_home == self.config_home
		iface_cache.iface_cache.__init__()

		os.mkdir(self.config_home, 0700)
		os.mkdir(self.cache_home, 0700)
		os.mkdir(self.cache_system, 0500)
		os.mkdir(self.gnupg_home, 0700)

		if os.environ.has_key('DISPLAY'):
			del os.environ['DISPLAY']
		namespaces.injector_gui_uri = os.path.join(os.path.dirname(__file__), 'test-gui.xml')

		logging.getLogger().setLevel(logging.WARN)

		download._downloads = {}

		self.old_path = os.environ['PATH']
		os.environ['PATH'] = dpkgdir + ':' + self.old_path

		distro.host_distribution = distro.DebianDistribution(dpkgdir)
	
	def tearDown(self):
		shutil.rmtree(self.config_home)
		support.ro_rmtree(self.cache_home)
		shutil.rmtree(self.cache_system)
		shutil.rmtree(self.gnupg_home)

		os.environ['PATH'] = self.old_path
