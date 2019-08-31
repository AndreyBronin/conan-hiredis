from conans import ConanFile, tools
from conans.tools import download, untargz
import os

class HiredisConan(ConanFile):
    name = "hiredis"
    version = "0.14.0"
    description = "hiredis is a minimalistic C client library for the Redis database."
    url = "https://github.com/redis/hiredis"
    license = "BSD 3-clause \"New\" or \"Revised\" License"
    FOLDER_NAME = 'hiredis-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "disable_threads": [True, False]}
    default_options = "shared=False", "disable_threads=False"

    def run_bash(self, cmd):
        if self.settings.os == "Windows":
            tools.run_in_windows_bash(self, cmd)
        else:
            self.run(cmd)

    def source(self):
        tarball_name = self.FOLDER_NAME + '.tar.gz'
        download("https://github.com/redis/hiredis/archive/v%s.tar.gz" % (self.version),
                 tarball_name)
        untargz(tarball_name)
        os.unlink(tarball_name)

    def build(self):
        with tools.chdir("hiredis-%s" % self.version) :
            self.run_bash("make")
        
    def package(self):
        self.copy("*.h", dst="include/hiredis", src="%s" % (self.FOLDER_NAME))
        self.copy("*.h", dst="include/hiredis/adapters", src="%s/adapters" % (self.FOLDER_NAME))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.cpp_info.libs = ['hiredis']

